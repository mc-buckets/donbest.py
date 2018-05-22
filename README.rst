
|header image|

|build badge| |MIT license|

Donbest.py is an easy-to-use Python wrapper for the `Don Best Sports Data API. <http://xml.donbest.com/v2/home>`_

Installation
------------

Donbest.py is available for download through the Python Package Index (PyPi). You can install it right away using pip or easy_install.

.. code:: bash

    pip install donbest

Usage
-----


To get started, you're going to need to get your Don Best API token from the `token generator <http://xml.donbest.com/v2/token>`_ on the Don Best website. Once you've got that, you're ready to go. In order to be able to generate a token you need to have an account with Don Best. You can get an account by contacting them. 

.. code:: pycon

    >>> import donbest
    >>> db = donbest.Donbest(api_token)

Once you've done this, you can now use the ``db`` object to make calls to the Don Best API. Here are some examples:

Event Schedule
~~~~~~

In-play schedule:

Returns a list of the upcoming scheduled competitions and propositions for the next several days. Does not return competitions that have already been played prior to the current day.

.. code:: pycon

    >>> schedule = db.schedule_inplay()
    >>> event = schedule[0]
    >>> event
    <Event id=806300, season=regular, date=None, opentime=2018-09-07 00:20:00+00:00, name=Atlanta Falcons vs Philadelphia Eagles, event_type=None, event_state=circled, time_changed=False, neutral=False, game_number=1, group=<Group id=515449, name=None, description=NFL WEEK 1 (REGULAR SEASON) - Thursday, September 6th, type=event, type_id=1>, participants=[<Team id=11, name=Atlanta Falcons, abbreviation=atlanta, full_name=None, information=None, league=None, rotation=451, side=away>, <Team id=2, name=Philadelphia Eagles, abbreviation=philadelphia, full_name=None, information=None, league=None, rotation=452, side=home>], league=<League id=1, name=NFL, abbreviation=None, information=None, sport=<Sport id=1, name=Football, abbreviation=None, information=None>>, location=<Location id=680, name=Lincoln Financial Field, description=None, abbreviation=None, stadium_type=None, surface_type=None, seating_capacity=None, elevation=None, city=None>, live=True, event_state_id=10>

    # Available Event attributes:
    event.id
    event.season
    event.date
    event.opentime
    event.name
    event.event_type
    event.event_state
    event.time_changed
    event.neutral
    event.game_number
    event.group
    event.group.id
    event.group.name
    event.group.type
    event.group.type_id
    event.live

    ## See Team section to view what attributes are 
    ## available on the items returned in the list of
    ## participants
    event.participants

    ## See League section for what attributes
    ## are available on League objects
    event.league

    ## See Location section for what attributes
    ## may be available on Location objects
    event.location

Full schedule:

Either of the commands below return the full schedule of upcoming events including competitions and propositions months in the future.

.. code:: pycon

    >>> db.schedule()
    >>> db.current_schedue()
    [<Event id=819810, .... >,
    <Event id =819811, .... >,
    ........................]

Scores
~~~~~

Returns a list containing the state of the live competition, current scores and period summary. Don Best ensures that their period scores are correct without using 3rd party providers which means that the scores are live and accurate.

Live scores:

.. code:: pycon

    >>> scores = db.score()
    >>> score = scores[0]
    <Score id=818854, league_id=12, away_rot=8205, home_rot=8206, away_score=6, home_score=7, description=FINAL, time=2018-05-22 14:18:26+00:00, period=FINAL, period_id=0, away_score_ext=None, home_score_ext=None, period_summary=[<Period name=Set 1, description=END-, time=2018-05-22 12:36:26+00:00, period_id=331, scores=[{'rot': '8205', 'value': '6'}, {'rot': '8206', 'value': '2'}]>, <Period name=Set 2, description=END-, time=2018-05-22 13:27:28+00:00, period_id=332, scores=[{'rot': '8205', 'value': '6'}, {'rot': '8206', 'value': '7'}]>, <Period name=Set 3, description=END-, time=2018-05-22 14:18:26+00:00, period_id=333, scores=[{'rot': '8205', 'value': '6'}, {'rot': '8206', 'value': '7'}]>]>

    # Available Score attributes:
    ## The Score id is the id of the event it relates to...they are the same value
    score.id
    score.league_id
    score.away_rot
    score.home_rot
    score.away_score
    score.home_score
    score.description
    score.time
    score.period
    score.period_id
    score.away_score_ext
    score.home_score_ext

    for period in score.period_summary:
        period.name
        period.description
        period.time_changed
        period.id
        for score in period.scores:
            score["rot"]
            score["value"]

Lines
~~~~

Returns a list of opening odds, live odds, and closing odds for competitions and propositions by league. *League id is a required parameter for all of the Lines endpoints*

Opening Odds (NBA):

.. code:: pycon

    >>> nba_lines = db.open(league_id=3)
    >>> line = nba_lines[0]
    <Line event=<Event id=817069, season=None, date=2018-05-23 01:05:00+00:00, opentime=None, name=None, event_type=None, event_state=None, time_changed=None, neutral=None, game_number=None, group=None, participants=None, league=None, location=None, live=None>, away_rot=505, home_rot=506, time=2018-05-22 21:11:47+00:00, period_id=1, period=FG, type=previous, sportsbook=347, ps=<PointSpread away_spread=8.00, home_spread=-8.00, away_price=-110, home_price=-110>, money=<MoneyLine away_money=330, home_money=-430, draw_money=0>, total=<Total total=226.50, over_price=-110, under_price=-110>, team_total=<TeamTotal away_total=109.00, away_over_price=-110, away_under_price=-110, home_total=117.50, home_over_price=-110, home_under_price=-110>, display_away=226%BD, display_home=-8%BD>

    # Available Line attributes:
    line.event
    line.away_rot
    line.home_rot
    line.time
    line.period_id
    line.period
    line.type
    line.sportsbook
    line.display_home
    line.display_away
    line.ps
    line.ps.away_spread
    line.ps.home_spread
    line.ps.away_price
    line.ps.home_price
    line.money
    line.money.away_money
    line.money.home_money
    line.money.draw_money
    line.total
    line.total.total
    line.total.over_price
    line.total.under_price
    line.team_total
    line.team_total.away_total
    line.team_total.away_over_price
    line.team_total.away_under_price
    line.team_total.home_total
    line.team_total.home_over_price
    line.team_total.home_under_price

Live Odds and Closing Odds (NBA):

.. code:: pycon

    >>> db.odds(league_id=3)
    >>> db.close(league_id=3)


Teams
~~~~~~~~~~~~~

Returns a list of Teams covered by Don Best Sports */v2/team*

.. code:: pycon

    >>> teams = db.team()
    >>> team = teams[0]
    <Team id=1, name=Washington, abbreviation=WAS, full_name=Washington Redskins, information=nfc - east, league=<League id=1, name=NFL, abbreviation=None, information=None, sport=<Sport id=1, name=Football, abbreviation=None, information=None>>, rotation=None, side=None>>

    # Available Team attributes:
    team.id
    team.name
    team.abbreviation
    team.full_name
    team.information
    team.league
    team.rotation
    team.side

Leagues
~~~~~~~~~~~~~

Returns a list of Leagues covered by Don Best Sports */v2/league*

.. code:: pycon

    >>> leagues = db.league()
    >>> league = leagues[0]
    <League id=1, name=NFL, abbreviation=NFL, information=None, sport=<Sport id=1, name=Football, abbreviation=FB, information=None>

    # Available League attributes
    league.id
    league.name
    league.abbreviation
    league.information
    league.sport

Sportsbooks
~~~~~~~~~~~~~

Returns a list of Sports Books covered by Don Best Sports */v2/sportsbook*

.. code:: pycon

    >>> sportsbooks = db.sportsbook()
    >>> sportsbook = sportsbooks[0]
    <Sportsbook id=276, name=5D Reduced Juice, abbreviation=5DReduced>

    # Available Sportsbook attributes:
    sportsbook.id
    sportsbook.name
    sportsbook.abbreviation

Sports
~~~~~~~~~~~~~

Returns a list of Sports covered by Don Best Sports */v2/sport*

.. code:: pycon

    >>> sports = db.sport()
    >>> sport = sports[1]
    <Sport id=1, name=Football, abbreviation=FB, information=None>

    # Available Sports attributes:
    sport.id
    sport.name
    sport.abbreviation
    sport.information

Locations
~~~~~~~~~~~~~

Returns a list of Stadium and Arenas for all competitions in the schedule feed. */v2/location*

.. code:: pycon

    >>> locations = db.location()
    >>> location = locations[0]
    <Location id=1, name=Wilson Stadium, description=None, abbreviation=None, stadium_type=None, surface_type=None, seating_capacity=75339, elevation=0, city=<City id=2, name=Buffalo, country=USA, postalCode=14127, state=NY>>

    # Available Location attributes:
    location.id
    location.name
    location.description
    location.abbreviation
    location.stadium_type
    location.surface_type
    location.seating_capacity
    location.elevation
    location.city
    location.city.id
    location.city.name
    location.city.country
    location.city.postalCode
    location.city.state

Miscellaneous
~~~~~~~~~~~~~

By default, donbest.py will return parsed python objects. If you’d like the raw XML response for a request, just pass in ``parse_response=False``.

.. code:: pycon

    >>> response = db.schedule_inplay(parse_response=False)
    >>> response
    b'<?xml version="1.0" encoding="utf-8"?>\n<don_best_sports><id>schedule_inplay</id><updated>2018-05-22T13:16:32+0</updated><schedule><sport id="1" name="Football">....

In most cases, the values of the object attributes are returned as the type you would expect (e.g. dates are returned as native python datetime objects). The main scenario in which this differs is for the unique 'id' of each object. All unique ids are returned as strings. Here is the quote from the Don Best API documentation that suggests this approach.

    Note: The Don Best Sports API exposes identifiers for uniquely identifiable objects such as Events, Teams and Sports
    Books. These IDs should always be treated as opaque strings, rather than integers of any specific type. The format of
    the IDs can change over time, so relying on the current format may cause you problems in the future

Donbest.py maps 1-1 to the Don Best Sports API (e.g., db.one.two.three() will
send a request to “http://xml.donbest.com/v2/one/two/three”). However, the library does not currently support the *event_state* or *market_list* endpoint. It also does not support the Don Best Streaming Message API since that requires your IP to be whitelisted, which makes it harder to test.

For more information on all methods and usage, please read the `Don Best Sports API documentation. <http://members.donbest.com/integration/index.html>`_


License |MIT License|
-----------------

MIT License. See `LICENSE <LICENSE>`__ for details.

TODO
-----------------
* Add support for the `/v2/event_state/` endpoint
* Add support for the `lastquery` request parameter
* Add option to have all objects return as properly formatted nested dictionaries

.. |header image| image:: https://s3.amazonaws.com/random-images-for-github/donbest.png
.. |MIT license| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
.. |build badge|  image:: https://travis-ci.com/mamcmanus/donbest.svg?token=43sVQ9sXnXzhgBns7vWu&branch=master
   :target: https://travis-ci.com/mamcmanus/donbest
