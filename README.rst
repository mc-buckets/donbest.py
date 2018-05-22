Donbest.py is an easy-to-use and fully-functional Python wrapper for the `Don Best Sports Data API. <http://xml.donbest.com/v2/home>`_

Installation
------------

Donbest.py is available for download through the Python Package Index (PyPi). You can install it right away using pip or easy_install.

.. code:: bash

    pip install "donbest"

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
    >>> first_event = schedule[0]
    >>> first_event
    <Event id=806300, season=regular, date=None, opentime=2018-09-07 00:20:00+00:00, name=Atlanta Falcons vs Philadelphia Eagles, event_type=None, event_state=circled, time_changed=False, neutral=False, game_number=1, group=<Group id=515449, name=None, description=NFL WEEK 1 (REGULAR SEASON) - Thursday, September 6th, type=event, type_id=1>, participants=[<Team id=11, name=Atlanta Falcons, abbreviation=atlanta, full_name=None, information=None, league=None, rotation=451, side=away>, <Team id=2, name=Philadelphia Eagles, abbreviation=philadelphia, full_name=None, information=None, league=None, rotation=452, side=home>], league=<League id=1, name=NFL, abbreviation=None, information=None, sport=<Sport id=1, name=Football, abbreviation=None, information=None>>, location=<Location id=680, name=Lincoln Financial Field, description=None, abbreviation=None, stadium_type=None, surface_type=None, seating_capacity=None, elevation=None, city=None>, live=True, event_state_id=10>

    # Available attributes:
    first_event.id
    first_event.season
    first_event.date
    first_event.opentime
    first_event.name
    first_event.event_type
    first_event.event_state
    first_event.time_changed
    first_event.neutral
    first_event.game_number
    first_event.group
    first_event.participants
    first_event.league
    first_event.location
    first_event.live


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

Full list of live scores

.. code:: pycon

    >>> db.score()
    [<Score id=818854, league_id=12, away_rot=8205, home_rot=8206, away_score=5, home_score=6, description=None, time=2018-05-22 13:14:09+00:00, period=Set 2, period_id=332, away_score_ext=None, home_score_ext=None, period_summary=[{'name': 'Set 1', 'description': ' ', 'time': datetime.datetime(2018, 5, 22, 12, 36, 26, tzinfo=<UTC>), 'period_id': '331', 'scores': [{'rot': '8205', 'value': '6'}, {'rot': '8206', 'value': '2'}]}, {'name': 'Set 2', 'description': ' ', 'time': datetime.datetime(2018, 5, 22, 13, 14, 9, tzinfo=<UTC>), 'period_id': '332', 'scores': [{'rot': '8205', 'value': '5'}, {'rot': '8206', 'value': '6'}]}]>, 
    <Score id=818855, league_id=12, away_rot=8207, home_rot=8208, away_score=2, home_score=4, description=None, time=2018-05-22 13:13:49+00:00, period=Set 2, period_id=332, away_score_ext=None, home_score_ext=None, period_summary=[{'name': 'Set 1', 'description': ' ', 'time': datetime.datetime(2018, 5, 22, 12, 47, 34, tzinfo=<UTC>), 'period_id': '331', 'scores': [{'rot': '8207', 'value': '6'}, {'rot': '8208', 'value': '7'}]}, {'name': 'Set 2', 'description': ' ', 'time': datetime.datetime(2018, 5, 22, 13, 13, 49, tzinfo=<UTC>), 'period_id': '332', 'scores': [{'rot': '8207', 'value': '2'}, {'rot': '8208', 'value': '4'}]}]>,
    ....]

Lines
~~~~

Returns a list of opening odds, live odds, and closing odds for competitions and propositions by league. `League id is a required parameter for all of the Lines endpoints`

Opening Odds (NBA):

.. code:: pycon

    >>> db.open(league_id=3)
    [<Line event=<Event id=817069, season=None, date=2018-05-23 01:05:00+00:00, opentime=None, name=None, event_type=None, event_state=None, time_changed=None, neutral=None, game_number=None, group=None, participants=None, league=None, location=None, live=None>, away_rot=505, home_rot=506, time=2018-05-21 02:20:48+00:00, period_id=1, period=FG, type=open, sportsbook=347, ps={'away_spread': Decimal('9.00'), 'away_price': -110, 'home_spread': Decimal('-9.00'), 'home_price': -110}, money={'away_money': 350, 'home_money': -450, 'draw_money': 0}, total={'total': Decimal('224.00'), 'over_price': -110, 'under_price': -110}, team_total=None, display={'away': '224', 'home': '-9'}, no_line=false>, 
    <Line event=<Event id=817069, season=None, date=2018-05-23 01:05:00+00:00, opentime=None, name=None, event_type=None, event_state=None, time_changed=None, neutral=None, game_number=None, group=None, participants=None, league=None, location=None, live=None>, away_rot=505, home_rot=506, time=2018-05-21 02:35:41+00:00, period_id=2, period=1H, type=open, sportsbook=347, ps={'away_spread': Decimal('5.00'), 'away_price': -110, 'home_spread': Decimal('-5.00'), 'home_price': -110}, money={'away_money': 215, 'home_money': -265, 'draw_money': 0}, total={'total': Decimal('114.00'), 'over_price': -105, 'under_price': -115}, team_total=None, display={'away': '114u15', 'home': '-5'}, no_line=false>,
    .....]

Live Odds (NBA):

.. code:: pycon

    >>> db.odds(league_id=3)
    <Line event=<Event id=730182, season=None, date=2017-10-20 19:00:00+00:00, opentime=None, name=None, event_type=None, event_state=None, time_changed=None, neutral=None, game_number=None, group=None, participants=None, league=None, location=None, live=None>, away_rot=12359, home_rot=12360, time=2017-10-06 07:59:01+00:00, period_id=1, period=FG, type=previous, sportsbook=347, ps=None, money=None, total={'total': Decimal('48.50'), 'over_price': -125, 'under_price': 105}, team_total=None, display={'away': '48%BD-130', 'home': '48%BD%2B110'}>, 
    <Line event=<Event id=730182, season=None, date=2017-10-20 19:00:00+00:00, opentime=None, name=None, event_type=None, event_state=None, time_changed=None, neutral=None, game_number=None, group=None, participants=None, league=None, location=None, live=None>, away_rot=12359, home_rot=12360, time=2017-10-12 18:20:54+00:00, period_id=1, period=FG, type=current, sportsbook=347, ps=None, money=None, total={'total': Decimal('48.50'), 'over_price': -130, 'under_price': 110}, team_total=None, display={'away': '48%BD-130', 'home': '48%BD%2B110'}, no_line=false>]
    .....]

Lookup feeds
~~~~

Teams:

Returns a list of Teams covered by Don Best Sports `/v2/team`

.. code:: pycon

    >>> db.team()
    [<Team id=6, name=Green Bay, abbreviation=GB, full_name=Green Bay Packers, information=nfc - north, league=<League id=1, name=NFL, abbreviation=None, information=None, sport=None>, rotation=None, side=None>,
    <Team id=7, name=Detroit, abbreviation=DET, full_name=Detroit Lions, information=nfc - north, league=<League id=1, name=NFL, abbreviation=None, information=None, sport=None>, rotation=None, side=None>,
    .....]

Leagues:

Returns a list of Leagues covered by Don Best Sports `/v2/league`

.. code:: pycon

    >>> db.league()
    [<League id=1, name=NFL, abbreviation=NFL, information=None, sport=<Sport id=1, name=Football, abbreviation=FB, information=None>>, 
    <League id=2, name=Ncaaf div I-A, abbreviation=CFB, information=None, sport=<Sport id=1, name=Football, abbreviation=FB, information=None>>, 
    <League id=3, name=NBA, abbreviation=NBA, information=None, sport=<Sport id=2, name=Basketball, abbreviation=BK, information=None>>,
    .....]

Sportsbooks:

Returns a list of Sports Books covered by Don Best Sports `/v2/sportsbook`

.. code:: pycon

    >>> db.sportsbook()
    [<Sportsbook id=396, name=SportsBettingOL, abbreviation=SBOL>, 
    <Sportsbook id=453, name=Casablanca, abbreviation=casa>, 
    <Sportsbook id=412, name=Bet365 InPlay, abbreviation=B365IP>, 
    <Sportsbook id=461, name=Hotel NV, abbreviation=HOTELNV>, 
    <Sportsbook id=468, name=Consensus 2, abbreviation=CONS2>,
    .....]

Sports:

Returns a list of Sports covered by Don Best Sports `/v2/sport`

.. code:: pycon

    >>> db.sport()
    [<Sport id=0, name=Unkown, abbreviation=UN, information=None>, 
    <Sport id=1, name=Football, abbreviation=FB, information=None>, 
    <Sport id=2, name=Basketball, abbreviation=BK, information=None>, 
    <Sport id=3, name=Baseball, abbreviation=BB, information=None>, 
    <Sport id=4, name=Hockey, abbreviation=HK, information=None>, 
    .....]

Locations:

Returns a list of Stadium and Arenas for all competitions in the schedule feed. `/v2/location`

.. code:: pycon

    >>> db.location()
    <Location id=524, name=Knott Arena, description=None, abbreviation=None, stadium_type=None, surface_type=None, seating_capacity=0, elevation=0, city=<City id=0, name=None, country=None, postalCode=None, state=None>>, 
    <Location id=525, name=Charles L. Sewall Center, description=None, abbreviation=None, stadium_type=None, surface_type=None, seating_capacity=0, elevation=0, city=<City id=0, name=None, country=None, postalCode=None, state=None>>, 
    <Location id=526, name=Pope Physical Education Center, description=None, abbreviation=None, stadium_type=None, surface_type=None, seating_capacity=0, elevation=0, city=<City id=0, name=None, country=None, postalCode=None, state=None>>, 
    <Location id=527, name=Skyhawk Arena, description=None, abbreviation=None, stadium_type=None, surface_type=None, seating_capacity=0, elevation=0, city=<City id=0, name=None, country=None, postalCode=None, state=None>>,
    .....]

Miscellaneous
~~~~~~~~~~~~~

By default, donbest.py will return parsed python objects. If you’d like
the raw XML response for a request, just pass in
``parse_response=False``.

.. code:: pycon

    >>> response = db.schedule_inplay(parse_response=False)
    >>> response
    b'<?xml version="1.0" encoding="utf-8"?>\n<don_best_sports><id>schedule_inplay</id><updated>2018-05-22T13:16:32+0</updated><schedule><sport id="1" name="Football">....

Donbest.py maps 1-1 to the Don Best Sports API (e.g., db.one.two.three() will
send a request to “http://xml.donbest.com/v2/one/two/three”). For more
information on all methods and usage, please read the `Don Best Sports API documentation. <http://xml.donbest.com/v2/home>`_

.. _license-licenselicense-imagelicense-url:

License |License|
-----------------

MIT License. See `LICENSE <license-url>`__ for details.