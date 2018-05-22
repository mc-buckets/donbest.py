# donbest_test.py

import datetime
import os
from donbest import (Donbest, Event, Sport, League, Team, Location, City,
                     Sportsbook, Line, APITokenMissingError,
                     EndpointNotSupportedError, EmptyResponseError,
                     ConnectionClosedError, Score)
from pytest import fixture, raises, mark
from datetime import datetime
import vcr
import time
import random


@fixture(scope="module")
def don():
    DONBEST_API_TOKEN = os.environ.get('DONBEST_API_TOKEN', None)
    return Donbest(token=DONBEST_API_TOKEN)


@fixture()
def random_test_ids():

    def get_ids(endpoint):
        d = don()
        feed = d[endpoint]()
        ids = []
        for f in feed:
            ids.append(f.id)
        random.shuffle(ids)
        return ids[:3]

    return get_ids


@fixture
def league_ids():
    return [1, 2, 3, 4, 5, 7, 13]


@fixture
def score_keys():
    # Responsible only for returning the test data
    return {
        'id': str,
        'league_id': str,
        'away_rot': int,
        'home_rot': int,
        'away_score': int,
        'home_score': int,
        'description': str,
        'time': datetime,
        'period': str
    }


@fixture
def event_keys():
    # Responsible only for returning the test data
    return {
        'id': str,
        'season': str,
        'name': str,
        'event_state': str,
        'time_changed': bool,
        'live': bool,
        'league': League,
        'location': Location,
        'participants': list
    }


@fixture
def sport_and_league_keys():
    return {
        'id': str,
        'name': str,
        'abbreviation': str,
        'information': str,
    }


@fixture
def league_keys():
    keys = sport_and_league_keys()
    keys['sport'] = Sport
    return keys


@fixture
def team_keys():
    return {
        'league': League,
        'id': str,
        'name': str,
        'abbreviation': str,
        'full_name': str,
        'information': str
    }


@fixture
def location_keys():
    return {'id': str, 'name': str}


@fixture
def city_keys():
    return {
        'id': str,
        'name': str,
        'state': str,
        'country': str,
        'postalCode': int
    }


@fixture
def location_keys_ext():
    keys = location_keys()
    keys['city'] = str
    keys['description'] = str
    keys['stadium_type'] = str
    keys['surface_type'] = str
    keys['seating_capacity'] = int
    keys['elevation'] = int
    keys['city'] = City
    return keys


@fixture
def sportsbook_keys():
    return {
        'id': str,
        'name': str,
        'abbreviation': str
    }


@fixture
def line_keys():
    return {
        'event': Event,
        'away_rot': int,
        'home_rot': int,
        'time': datetime,
        'period_id': int,
        'period': str,
        'type': str,
        'sportsbook': str
    }


def test_missing_api_token():
    with raises(APITokenMissingError):
        don = Donbest(token=None)


def test_bad_endpoint(don):
    with raises(EndpointNotSupportedError):
        bad_endpoint = don.scores()


@vcr.use_cassette('vcr_cassettes/schedules.yml', filter_query_parameters=['token'], record_mode='new_episodes')
@mark.parametrize("endpoint", [
    ("schedule"),
    ("current_schedule"),
    ("schedule_inplay")
])
def test_schedules(don, random_test_ids, event_keys, endpoint):
    """Tests an API call to get info about the score of a event"""
    schedule = don[endpoint]()
    assert type(schedule) == list
    events_count = len(schedule)
    assert events_count > 0
    keys = event_keys

    def validate_resource(resource):
        assert isinstance(resource, Event)
        for key, value in keys.items():
            assert hasattr(resource, key)
            if resource[key] is not None:
                assert isinstance(resource[key], value)
            if key == 'participants':
                assert len(resource[key]) >= 2

    for resource in schedule:
        validate_resource(resource)


@vcr.use_cassette('vcr_cassettes/lookups.yml', filter_query_parameters=['token'], record_mode='new_episodes')
@mark.parametrize("endpoint,class_type,keys", [
    ("location", Location, location_keys),
    ("sport", Sport, sport_and_league_keys),
    ("league", League, league_keys),
    ("team", Team, team_keys),
    ("sportsbook", Sportsbook, sportsbook_keys),
    ("score", Score, score_keys)
])
def test_lookup_feeds(don, random_test_ids, endpoint, class_type, keys):

    def validate_resource(resource):
        assert isinstance(resource, class_type)
        for key, value in keys().items():
            assert hasattr(resource, key)
            if resource[key] is not None:
                assert isinstance(resource[key], value)

    feed = don[endpoint]()
    assert isinstance(feed, list)
    for resource in feed:
        validate_resource(resource)

    test_ids = random_test_ids(endpoint)
    for test_id in test_ids:
        resource = don[endpoint](id=test_id)
        validate_resource(resource)


@vcr.use_cassette('vcr_cassettes/lines.yml', filter_query_parameters=['token'], record_mode='new_episodes')
@mark.parametrize("endpoint", [
    ("odds"),
    ("open"),
    ("close")
])
def test_odds(don, league_ids, endpoint, line_keys):

    def validate_resource(resource):
        assert isinstance(resource, Line)
        for key, value in keys.items():
            assert hasattr(resource, key)
            if resource[key] is not None:
                assert isinstance(resource[key], value)

    for test_id in league_ids:
        try:
            lines = don[endpoint](league_id=test_id)
            assert type(lines) == list
            keys = line_keys
            for resource in lines:
                validate_resource(resource)
        except (ConnectionClosedError, EmptyResponseError) as e:
            pass
