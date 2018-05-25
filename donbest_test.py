# donbest_test.py

# built-ins
import os, time, random
from datetime import datetime
# testing libs
from pytest import fixture, raises, mark
# API wrapper
import donbest

@fixture(scope="module")
def donbest_client():
    DONBEST_API_TOKEN = os.environ.get('DONBEST_API_TOKEN', None)
    return donbest.Donbest(token=DONBEST_API_TOKEN)

@fixture()
def random_test_ids():

    def get_ids(endpoint):
        d = donbest_client()
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
def sport_keys():
    return {
        'id': str,
        'name': str,
        'abbreviation': str,
        'information': str
    }

@fixture
def league_keys():
    keys = sport_keys()
    keys['sport'] = donbest.Sport
    return keys

@fixture
def team_keys():
    return {
        'id': str,
        'name': str,
        'abbreviation': str,
        'full_name': str,
        'information': str,
        'league': donbest.League,
        'rotation': int,
        'side': str
    }

@fixture
def location_keys():
    return {
        'id': str, 
        'name': str,
        'description': str,
        'abbreviation': str,
        'stadium_type': str,
        'surface_type': str,
        'seating_capacity': int,
        'elevation': int,
        'city': donbest.City
    }

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
def sportsbook_keys():
    return {
        'id': str,
        'name': str,
        'abbreviation': str,
    }

@fixture
def line_keys():
    return {
        'event': donbest.Event,
        'away_rot': int,
        'home_rot': int,
        'time': datetime,
        'period_id': int,
        'period': str,
        'type': str,
        'sportsbook': str,
        'no_line': bool,
        'ps': donbest.PointSpread,
        'money': donbest.MoneyLine,
        'total': donbest.Total,
        'team_total': donbest.TeamTotal,
        'display_away': str,
        'display_home': str
    }

@fixture
def event_keys():
    # Responsible only for returning the test data
    return {
        'id': str,
        'season': str,
        'date': datetime,
        'opentime': datetime,
        'name': str,
        'event_type': str,
        'event_state': str,
        'time_changed': bool,
        'neutral': bool,
        'game_number': int,
        'group': donbest.Group,
        'live': bool,
        'league': donbest.League,
        'location': donbest.Location,
        'participants': list
    }

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
        'period': str,
        'period_id': int,
        'away_score_ext': str,
        'home_score_ext': str,
        'period_summary': list
    }

def test_missing_api_token():
    with raises(donbest.APITokenMissingError):
        donbest_client = donbest.Donbest(token=None)

def test_bad_endpoint(donbest_client):
    with raises(donbest.EndpointNotSupportedError):
        bad_endpoint = donbest_client.scores()

def test_invalid_params(donbest_client):
    with raises(donbest.InvalidParametersError):
        bad_endpoint = donbest_client.odds()

@mark.parametrize("endpoint", [
    ("schedule"),
    ("current_schedule"),
    ("schedule_inplay")
])
def test_schedules(donbest_client, random_test_ids, event_keys, endpoint):
    """Tests an API call to get info about the score of a event"""
    schedule = donbest_client[endpoint]()
    assert type(schedule) == list
    events_count = len(schedule)
    assert events_count > 0
    keys = event_keys

    def validate_resource(resource):
        assert isinstance(resource, donbest.Event)
        for key, value in keys.items():
            assert hasattr(resource, key)
            if resource[key] is not None:
                assert isinstance(resource[key], value)
            if key == 'participants':
                assert len(resource[key]) >= 2

    for resource in schedule:
        validate_resource(resource)

@mark.parametrize("endpoint,class_type,keys", [
    ("location", donbest.Location, location_keys),
    ("sport", donbest.Sport, sport_keys),
    ("league", donbest.League, league_keys),
    ("team", donbest.Team, team_keys),
    ("sportsbook", donbest.Sportsbook, sportsbook_keys),
    ("score", donbest.Score, score_keys)
])
def test_lookup_feeds(donbest_client, random_test_ids, endpoint, class_type, keys):

    def validate_resource(resource):
        assert isinstance(resource, class_type)
        for key, value in keys().items():
            assert hasattr(resource, key)
            if resource[key] is not None:
                assert isinstance(resource[key], value)

    feed = donbest_client[endpoint]()
    assert isinstance(feed, list)
    for resource in feed:
        validate_resource(resource)

    test_ids = random_test_ids(endpoint)
    for test_id in test_ids:
        resource = donbest_client[endpoint](id=test_id)
        validate_resource(resource)

@mark.parametrize("endpoint", [
    ("odds"),
    ("open"),
    ("close")
])
def test_odds(donbest_client, league_ids, endpoint, line_keys):

    def validate_resource(resource):
        assert isinstance(resource, donbest.Line)
        for key, value in keys.items():
            assert hasattr(resource, key)
            if resource[key] is not None:
                assert isinstance(resource[key], value)

    for test_id in league_ids:
        try:
            lines = donbest_client[endpoint](league_id=test_id)
            assert type(lines) == list
            keys = line_keys
            for resource in lines:
                validate_resource(resource)
        except (donbest.ConnectionClosedError, donbest.EmptyResponseError) as e:
            pass