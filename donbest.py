# donbest.py
# -*- coding: utf-8 -*-

# built-ins
import os
from datetime import datetime
from io import BytesIO
import xml.etree.ElementTree as etree
from collections import Counter
from decimal import Decimal
# 3rd party dependencies
import requests


class APITokenMissingError(Exception):
    pass


class EndpointNotSupportedError(Exception):
    pass


class MissingEndpointError(Exception):
    pass


class MissingParametersError(Exception):
    pass


class EmptyResponseError(Exception):
    pass


class ConnectionClosedError(Exception):
    pass


class BaseDonbestResponse(object):
    """Base object containing methods and attributes that
    other generated objects will inherit and use to set
    their own attributes.
    """

    # Lists of fields returned in Don Best API responses
    # that should be converted to a specific python type
    DATE_FIELDS = ["updated", "time", "date", "opentime"]
    INT_FIELDS = ["game_number", "rot", "seating_capacity",
                  "elevation", "away_rot", "home_rot", "period_id",
                  "home_score", "away_score", "home_price", "away_price",
                  "away_money", "home_money", "draw_money", "over_price",
                  "under_price", "away_over_price", "home_over_price",
                  "away_under_price", "home_under_price", "game_number"
                  ]
    DECIMAL_FIELDS = ["away_spread", "home_spread", "total",
                      "away_total", "home_total"
                      ]
    BOOLEAN_FIELDS = ["time_changed", "neutral", "live"]
    DATE_FORMATS = ["%Y-%m-%dT%H:%M:%S+0", "%Y-%m-%dT%H:%M:%S+0000"]

    def __init__(self, node, donbest):
        super().__init__()
        self.node = node
        self._donbest = donbest

    def __getitem__(self, key):
        value = getattr(self, key)
        return value

    @staticmethod
    def cast_value(key, value):
        """Sets returned values to proper types so they can
        be more easily interacted with when integrating
        the library into other python code.
        """
        if value == "" or value == " " or value is None:
            v = None
        else:
            if key in BaseDonbestResponse.DATE_FIELDS:
                for fmat in BaseDonbestResponse.DATE_FORMATS:
                    try:
                        v = datetime.strptime(value, fmat)
                    except ValueError as e:
                        pass
            elif key in BaseDonbestResponse.INT_FIELDS:
                v = int(value)
            elif key in BaseDonbestResponse.DECIMAL_FIELDS:
                v = Decimal(value)
            elif key in BaseDonbestResponse.BOOLEAN_FIELDS:
                if str.lower(value) == 'true':
                    v = True
                elif str.lower(value) == 'false':
                    v = False
            else:
                v = value
        return v

    def to_dict(self):
        """Returns object as a python dictionary.
        This method is overwritten in other objects
        where the dictionary needs to be nested.
        """
        data = vars(self)
        data.pop('node')
        data.pop('_donbest')
        return data

    # Returns list of XML tags that appear more 
    # than once as children of the specified element.
    def _get_duplicate_children(self, element):
        children = list(element)
        tags = [child.tag for child in children]
        dupes = [tag for tag, count in Counter(tags).items() if count > 1]
        return dupes

    # Returns list of XML elements that are
    # children of the specific element with
    # duplicates removed.
    def _get_single_children(self, element):
        dupes = self._get_duplicate_children(element)
        children = [child for child in list(element) if child.tag not in dupes]
        singles = [child for child in children if len(child) == 0]
        return singles

    # Sets a single class attribute from 
    # a single XML element. Attribute name is
    # set to element.tag and the attribute 
    # value is set to element.text
    def _setattr_from_text(self, element):
        tag = element.tag
        value = element.text
        if tag != 'link':
            v = self.cast_value(tag, value)
            setattr(self, tag, v)
        else:
            pass

    # Sets class attributes to the key, value pairs 
    # returned from a single XML element.
    def _setattr_from_attributes(self, element):
        for k, v in element.attrib.items():
            if 'link' not in k:
                v = self.cast_value(k, v)
                setattr(self, k, v)

    # Sets class attributes from non-dupe children
    # of the specific XML element.
    def _setattr_from_single_children(self, element, use_tag=True):
        singles = self._get_single_children(element)
        for child in singles:
            if not child.attrib:
                self._setattr_from_text(child)
            else:
                if "link" in child.attrib.keys():
                    child.attrib.pop("link")
                    pass
                if use_tag and len(child.attrib.keys()) > 0:
                    for k, v in child.attrib.items():
                        v = self.cast_value(k, v)
                        child.attrib[k] = v
                    setattr(self, child.tag, child.attrib)
                else:
                    self._setattr_from_attributes(child)

    # Sets class attributes from duplicate children
    # which is handled differently than the single
    # use case.
    def _setattr_from_dupe_children(self, element, take_first=False):
        dupes = self._get_duplicate_children(element)
        for d in dupes:
            children = element.findall(d)
            if take_first:
                self._setattr_from_text(children[0])

    # Returns all non-internal attributes
    # for an easier readout of each class.
    def __repr__(self):
        attr_dict = self.__dict__.items()
        strings = []
        for key, value in attr_dict:
            if key == '_donbest' or key == 'node':
                pass
            else:
                s = "{}={}".format(key, value)
                strings.append(s)
        s = ", ".join(strings)
        name = self.__class__.__name__
        representation = '''<{} {}>'''.format(name, s)
        return representation

class Sport(BaseDonbestResponse):
    """Returns a Sport"""
    def __init__(self, node, donbest):
        super().__init__(node=node, donbest=donbest)
        self.id = None
        self.name = None
        self.abbreviation = None
        self.information = None
        self._setattr_from_attributes(self.node)
        self._setattr_from_single_children(self.node)

class League(BaseDonbestResponse):
    """Returns a League"""
    def __init__(self, node, donbest):
        super().__init__(node=node, donbest=donbest)
        self.id = None
        self.name = None
        self.abbreviation = None
        self.information = None
        self.sport = None
        self._setattr_from_attributes(self.node)
        self._setattr_from_single_children(self.node)

    @classmethod
    def from_xml_collection(cls, node, sport, donbest):
        """Create a new League instance from an XML
        response that includes a Sport object
        """
        l = cls(node=node, donbest=donbest)
        l.sport = sport
        return l

class Team(BaseDonbestResponse):
    """Returns a Team"""
    def __init__(self, node, donbest):
        super().__init__(node=node, donbest=donbest)
        self.id = None
        self.name = None
        self.abbreviation = None
        self.full_name = None
        self.information = None
        self.league = None
        self.rotation = None
        self.side = None
        self._setattr_from_attributes(self.node)
        self._setattr_from_single_children(self.node)

    @classmethod
    def from_xml_collection(cls, node, league, donbest):
        """Creates a new Team instance from the 
        donbest.team() lookup feed XML response.
        """
        l = cls(node=node, donbest=donbest)
        l.league = league
        return l

    @classmethod
    def from_participant_node(cls, node, rotation, side, donbest):
        """Creates a new Team instance from 'participant'
        XML nodes returned in the schedule and current_schedule 
        XML responses.
        """
        l = cls(node=node, donbest=donbest)
        l.rotation = rotation
        l.side = side
        return l

    @classmethod
    def from_inplay_participant_node(cls, node, donbest):
        """Creates a new Team instance from 'participant'
        XML nodes returned in the schedule_inplay XML response.
        """
        l = cls(node=node, donbest=donbest)
        l.id = l.team_id
        delattr(l, "team_id")
        return l

class Location(BaseDonbestResponse):
    """Returns a Location"""
    def __init__(self, node, donbest):
        super().__init__(node=node, donbest=donbest)
        self.id = None
        self.name = None
        self.description = None
        self.abbreviation = None
        self.stadium_type = None
        self.surface_type = None
        self.seating_capacity = None
        self.elevation = None
        self.city = None
        self._setattr_from_attributes(self.node)
        self._setattr_from_single_children(self.node)

    @classmethod
    def from_xml_collection(cls, node, city, donbest):
        """Creates a new Location instance from the 
        donbest.location() lookup feed XML response.
        """
        l = cls(node=node, donbest=donbest)
        l.city = city
        return l

class City(BaseDonbestResponse):
    """"Returns a City"""
    def __init__(self, node, donbest):
        super().__init__(node=node, donbest=donbest)
        self.id = None
        self.name = None
        self.country = None
        self.postalCode = None
        self.state = None
        self._setattr_from_attributes(self.node)
        self._setattr_from_single_children(self.node)

class Sportsbook(BaseDonbestResponse):
    """"Returns a Sportsbook"""
    def __init__(self, node, donbest):
        super().__init__(node=node, donbest=donbest)
        self.id = None
        self.name = None
        self.abbreviation = None
        self._setattr_from_attributes(self.node)
        self._setattr_from_single_children(self.node)
        self._setattr_from_dupe_children(self.node, take_first=True)

class PointSpread(BaseDonbestResponse):
    """Returns a PointSpread"""
    def __init__(self, node, donbest):
        super().__init__(node=node, donbest=donbest)
        self.away_spread = None
        self.home_spread = None
        self.away_price = None
        self.home_price = None
        self._setattr_from_attributes(self.node)

class MoneyLine(BaseDonbestResponse):
    """Returns a MoneyLine"""
    def __init__(self, node, donbest):
        super().__init__(node=node, donbest=donbest)
        self.away_money = None
        self.home_money = None
        self.draw_money = None
        self._setattr_from_attributes(self.node)

class Total(BaseDonbestResponse):
    """Returns a Total"""
    def __init__(self, node, donbest):
        super().__init__(node=node, donbest=donbest)
        self.total = None
        self.over_price = None
        self.under_price = None
        self._setattr_from_attributes(self.node)

class TeamTotal(BaseDonbestResponse):
    """Returns a TeamTotal"""
    def __init__(self, node, donbest):
        super().__init__(node=node, donbest=donbest)
        self.away_total = None
        self.away_over_price = None
        self.away_under_price = None
        self.home_total = None
        self.home_over_price = None
        self.home_under_price = None
        self._setattr_from_attributes(self.node)

class Line(BaseDonbestResponse):
    """Returns a Line"""
    def __init__(self, node, donbest):
        super().__init__(node=node, donbest=donbest)
        self.event = None
        self.away_rot = None
        self.home_rot = None
        self.time = None
        self.period_id = None
        self.period = None
        self.type = None
        self.sportsbook = None
        self.ps = None
        self.money = None
        self.total = None
        self.team_total = None
        self.display_away = None
        self.display_home = None
        self._setattr_from_attributes(self.node)

    @classmethod
    def from_xml_collection(cls, node, event, donbest):
        """Creates a new Line instance from the 
        donbest.odd(), donbest.open(), and
        donbest.close() lookup feeds XML responses.
        """
        l = cls(node=node, donbest=donbest)
        l.event = event
        ps = l.node.find(".//ps")
        money = l.node.find(".//money")
        total = l.node.find(".//total")
        team_total = l.node.find(".//team_total")
        display = l.node.find(".//display")

        if ps is not None:
            l.ps = PointSpread(ps, donbest=donbest)
        if money is not None:
            l.money = MoneyLine(money, donbest=donbest)
        if total is not None:
            l.total = Total(total, donbest=donbest)
        if team_total is not None:
            l.team_total = TeamTotal(team_total, donbest=donbest)
        if display is not None:
        	l.display_home = display.attrib["home"]
        	l.display_away = display.attrib["away"]

        return l

class Group(BaseDonbestResponse):
    """"Returns a Group"""
    def __init__(self, node, donbest):
        super().__init__(node=node, donbest=donbest)
        self.id = None
        self.name = None
        self._setattr_from_attributes(self.node)

class Event(BaseDonbestResponse):
    """Returns an Event"""
    def __init__(self, node, donbest):
        super().__init__(node=node, donbest=donbest)
        self.id = None
        self.season = None
        self.date = None
        self.opentime = None
        self.name = None
        self.event_type = None
        self.event_state = None
        self.time_changed = None
        self.neutral = None
        self.game_number = None
        # maybe make this it's own object
        self.group = None
        self.participants = None
        # self.sport = None
        self.league = None
        self.location = None
        self.live = None
        self._setattr_from_attributes(self.node)
        self._setattr_from_single_children(self.node)

    @classmethod
    def from_full_xml_collection(cls, node, league, group, donbest):
        """Creates a new Event instance from the 
        donbest.schedule() and donbest.current_schedule() 
        lookup feed XML responses.
        """
        e = cls(node=node, donbest=donbest)
        e.league = league
        e.group = group
        e.location = Location(e.node.find(".//location"), donbest=e)

        participants = e.node.findall(".//participant")
        if participants is not None:
            parts = []
            for p in participants:
                if p.find(".//team") is not None:
                    if "rotation_number" in p.attrib.keys():
                        rot = p.attrib["rotation_number"]
                    elif "rot" in p.attrib.keys():
                        rot = p.attrib["rot"]
                    if "side" in p.attrib.keys():
                        side = p.attrib["side"]
                    t = p.find(".//team")
                    team = Team.from_participant_node(
                        node=t, rotation=rot, side=side, donbest=e)
                    parts.append(team)
                elif "name" in p.attrib.keys():
                    parts.append(p.attrib)
            e.participants = parts

        return e

    @classmethod
    def from_inplay_xml_collection(cls, node, league, group, donbest):
        """Creates a new Event instance from the 
        donbest.schedule_inplay() lookup feed XML responses.
        """
        e = cls(node=node, donbest=donbest)
        e.league = league
        e.group = group
        e.location = Location(e.node.find(".//location"), donbest=e)

        participants = e.node.findall(".//participant")
        if participants is not None:
            parts = []
            for p in participants:
                team = Team.from_inplay_participant_node(node=p, donbest=e)
                parts.append(team)
            e.participants = parts

        return e

    def get_lines(self):
        league_id = self.league_id
        event_id = self.id
        return self._donbest.odds(league_id=league_id, event_id=event_id)

    def get_score(self):
        pass

class Period(BaseDonbestResponse):
    """Returns a Period"""
    def __init__(self, node, donbest):
        super().__init__(node=node, donbest=donbest)
        self.name = None
        self.description = None
        self.time = None
        self.period_id = None
        self.scores = None
        self._setattr_from_attributes(self.node)

    @classmethod
    def from_period_summary(cls, node, donbest):
        """Creates a new Period instance from the
        period XML nodes returned in the donbest.score()
        API response.
        """
        p = cls(node, donbest=donbest)
        scores = p.node.findall(".//score")
        if scores is not None:
            score_list = [score.attrib for score in scores]
        p.scores = score_list

        return p

class Score(BaseDonbestResponse):
    """Returns a Score"""
    def __init__(self, node, donbest):
        super().__init__(node=node, donbest=donbest)
        self.id = None
        self.league_id = None
        self.away_rot = None
        self.home_rot = None
        self.away_score = None
        self.home_score = None
        self.description = None
        self.time = None
        self.period = None
        self.period_id = None
        self.away_score_ext = None
        self.home_score_ext = None
        self.period_summary = None
        self._setattr_from_attributes(self.node)
        self._setattr_from_single_children(self.node, use_tag=False)

    @classmethod
    def from_xml_collection(cls, node, donbest):
        """Creates a new Score instance from the 
        donbest.score() XML response.
        """
        s = cls(node=node, donbest=donbest)
        period_summary = s.node.find(".//period_summary")
        periods = period_summary.findall(".//period")
        if periods is not None:
            p_list = []
            for period in periods:
                p = Period.from_period_summary(period, donbest=donbest)
                p_list.append(p)
        s.period_summary = p_list
        return s

class Donbest(object):
    """"Main object that interacts with the Donbest API.
    Handles request and response routing and manages
    the HTTP session via the requests library.
   	"""
    BASE_URL = 'http://xml.donbest.com/v2/'

    ENDPOINTS = ["schedule", "odds", "current_schedule",
                 "schedule_inplay", "team", "sport",
                 "league", "location", "sportsbook",
                 "odds", "close", "open", "score"
                 ]

    def __init__(self, token):
        super().__init__()
        if not token:
            raise APITokenMissingError(
                "All methods require an API token. See "
                "http://xml.donbest.com/v2/ "
                "for more info on how to request an API token from "
                "Donbest"
            )
        else:
            self.token = token
            self._session = requests.Session()
            self._session.params = {"token": self.token}

    def __getattr__(self, endpoint):
        if endpoint not in self.ENDPOINTS:
            raise EndpointNotSupportedError(
                "The endpoint you tried is "
                "not supported or does not exist "
                "please visit http://xml.donbest.com/v2/home "
                "for more info on what endpoints are supported"
            )
        else:
            self.endpoint = endpoint
            return self

    def __getitem__(self, endpoint):
        if endpoint not in self.ENDPOINTS:
            raise EndpointNotSupportedError(
                "The endpoint you tried is "
                "not supported or does not exist "
                "please visit http://xml.donbest.com/v2/home "
                "for more info on what endpoints are supported"
            )
        else:
            self.endpoint = endpoint
            return self

    def __call__(self, *args, **kwargs):
        if self.endpoint is None:
            raise MissingEndpointError(
                "You must use an endpoint when calling the API "
                "please visit http://xml.donbest.com/v2/home "
                "for more info on what endpoints are supported"
            )
        else:
            url = "{}{}/".format(self.BASE_URL, self.endpoint)
            parse_response = kwargs.get('parse_response', True)
            # Check to see if an individual resource
            # was requested and if so, append it to
            # the url.
            request_contains_id = False
            for key, value in kwargs.items():
                if 'id' in key:
                    url = "{}{}/".format(url, value)
                    request_contains_id = True

            if self.endpoint in ["odds", "open", "close"] and not request_contains_id:
            	raise MissingParametersError(
            		"Don Best can only return odds per league."
            		"Please include a league id in your request."
            		"For example, league_id=3 for NBA odds."
            		)

            # TODO: add support for 'last timestamp' param
            # attempt to make the request
            try:
                r = self._session.get(url)
                r.raise_for_status()
                if "error" in r.request.url:
                    raise ConnectionClosedError(
                        "Donbest is throwing an unauthorized request error"
                        "which may mean they just don't have any data"
                        "to respond to the request with")
            except Exception as e:
                raise e

            if parse_response:
                response = BytesIO(r.content)
                if response.getbuffer().nbytes == 0:
                    raise EmptyResponseError(
                        "The response from the API came back empty."
                    )
                else:
                    node = etree.parse(response)

                # The schedule feeds contain upcoming scheduled competitions
                # and propositions for the next several days. These feeds do
                # not contain competitions that have already been played prior
                # to the current day.
                if self.endpoint in ["schedule", "current_schedule", "schedule_inplay"]:
                    schedule = []
                    for s in node.findall(".//sport"):
                        sport = Sport(s, donbest=self)
                        for l in s.findall(".//league"):
                            league = League.from_xml_collection(
                                l, sport=sport, donbest=self)
                            for g in l.findall(".//group"):
                                group = Group(g, donbest=self)
                                for e in l.findall(".//event"):
                                    if self.endpoint == "schedule_inplay":
                                        event = Event.from_inplay_xml_collection(
                                            e, league=league, group=group, donbest=self)
                                    else:
                                        event = Event.from_full_xml_collection(
                                            e, league=league, group=group, donbest=self)
                                    schedule.append(event)
                    return schedule

                # Live scores feeds contain the state of the live competition,
                # current scores and period summary. Donbest ensures that their
                # period scores are correct without using 3rd party providers
                # which means their scores are live and accurate.
                if self.endpoint == "score":
                    all_scores = []
                    for s in node.findall(".//event"):
                        score = Score.from_xml_collection(s, donbest=self)
                        all_scores.append(score)
                    if "id" in kwargs:
                        return all_scores[0]
                    else:
                        return all_scores

                # Lines feed contains current odds set by market making
                # Sports Books for major North American and European sports.
                if self.endpoint in ["odds", "open", "close"]:
                    lines = []
                    for e in node.findall(".//event"):
                        event = Event(node=e, donbest=self)
                        for l in e.findall(".//line"):
                            line = Line.from_xml_collection(
                                node=l, event=event, donbest=self)
                            lines.append(line)
                    if len(lines) == 0:
                        raise EmptyResponseError(
                            "The response from the API came back empty."
                        )
                    else:
                        return lines

                # Tracks changes to an event including time/date change,
                # rain delay as well as start, final and halftime.
                if self.endpoint == "event_state":
                    pass

                ### LOOK UP FEEDS ###

                # A list of Stadium and Arenas for all competitions in
                # the schedule feed
                if self.endpoint == "location":
                    all_locations = []
                    for l in node.findall(".//location"):
                        city = City(l.find(".//city"), donbest=self)
                        location = Location.from_xml_collection(
                            l, city=city, donbest=self)
                        all_locations.append(location)
                    if "id" in kwargs:
                        return all_locations[0]
                    else:
                        return all_locations

                # A list of Sports covered by Don Best Sports
                if self.endpoint == "sport":
                    all_sports = []
                    for s in node.findall(".//sport"):
                        sport = Sport(s, donbest=self)
                        all_sports.append(sport)
                    if "id" in kwargs:
                        return all_sports[0]
                    else:
                        return all_sports

                # A list of Leagues covered by Don Best Sports
                if self.endpoint == "league":
                    all_leagues = []
                    for l in node.findall(".//league"):
                        sport = Sport(l.find(".//sport"), donbest=self)
                        league = League.from_xml_collection(
                            l, sport=sport, donbest=self)
                        all_leagues.append(league)
                    if "id" in kwargs:
                        return all_leagues[0]
                    else:
                        return all_leagues

                # A list of Teams covered by Don Best Sports
                if self.endpoint == "team":
                    all_teams = []
                    if 'id' in kwargs:
                        league = League(node.find(".//league"), donbest=self)
                        team = Team.from_xml_collection(
                        	node.find(".//team"), league=league,
                        	donbest=self)
                        return team
                    else:
                        for s in node.findall(".//sport"):
                            sport = Sport(s, donbest=self)
                            for l in s.findall(".//league"):
                                league = League.from_xml_collection(
                                    l, sport=sport, donbest=self)
                                teams = l.findall(".//team")
                                for t in teams:
                                    team = Team.from_xml_collection(
                                        t, league=league, donbest=self)
                                    all_teams.append(team)
                        return all_teams

                # A list of Sports Books covered by Don Best Sports
                if self.endpoint == "sportsbook":
                    all_sportsbooks = []
                    for l in node.findall(".//sportsBook"):
                        book = Sportsbook(l, donbest=self)
                        all_sportsbooks.append(book)
                    if "id" in kwargs:
                        return all_sportsbooks[0]
                    else:
                        return all_sportsbooks

            else:
                return(r.content)
