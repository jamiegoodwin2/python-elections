"""
Classes that structure the data provided by AP.
"""

class Candidate(object):
    """
    A choice for voters in a race.
    
    In the presidential race, a person, like Barack Obama.
    In a ballot measure, a direction, like Yes or No.
    """
    def __init__(self, first_name=None, middle_name=None, last_name=None,
                 abbrev_name=None, suffix=None, use_suffix=False, 
                 ap_natl_number=None, ap_polra_number=None, ap_race_number=None,
                 combined_id=None, party=None, vote_total=None, ap_pol_number=None,
                 vote_total_percent=None, is_winner=None, is_runoff=None):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.abbrev_name = abbrev_name
        self.suffix = suffix
        self.use_suffix = use_suffix
        self.ap_natl_number = ap_natl_number
        self.ap_polra_number = ap_polra_number
        self.ap_race_number = ap_race_number
        self.ap_pol_number = ap_pol_number
        self.combined_id = combined_id
        self.party = party
        self.is_winner = is_winner
        self.is_runoff = is_runoff
        self.vote_total = vote_total
        self.vote_total_percent = vote_total_percent

    def __unicode__(self):
        if not self.last_name in ('Yes', 'No'):
            return u'%s %s' % (self.first_name, self.last_name)
        else:
            return u'%s' % self.last_name

    def __repr__(self):
        return u'<Candidate: %s>' % self.__unicode__()


class Race(object):
    """
    A contest being decided by voters choosing between candidates.
    
    For example:
    
        * The presidential general election
        * The governorship of Maine
        * Proposition 8 in California
    
    """
    def __init__(self, ap_race_number=None, office_name=None, office_description=None,
                 office_id=None, seat_name=None, seat_number=None, scope=None,
                 date=None, num_winners=None, party=None, uncontested=None):
        self.ap_race_number = ap_race_number
        self.office_name = office_name
        self.office_description = office_description
        self.office_id = office_id
        self.seat_name = seat_name
        self.seat_number = seat_number
        self.scope = scope
        self.date = date
        self.num_winners = num_winners
        self.party = party
        self.uncontested = uncontested
        self._candidates = {}
        self._state_results = {}

    @property
    def state_results(self):
        return self._state_results.values()

    @property
    def candidates(self):
        return self._candidates.values()

    def add_candidate(self, candidate):
        self._candidates.update({candidate.ap_polra_number: candidate})

    def get_name(self):
        name = ''
        if self.scope == 'L':
            if self.office_descrip:
                name = u'%s %s - %s' % (self.office_name, self.seat_name, self.office_descrip)
            else:
                name = u'%s %s' % (self.office_name, self.seat_name)
        else:
            if self.office_name == "Proposition":
                num = self.seat_name.split('-')[0].strip()
                name = "%s %s" % (self.office_name, num)
            else:
                name = u'%s' % self.office_name
        return name
    name = property(get_name)

    def __unicode__(self):
        return u'%s' % self.name

    def __repr__(self):
        return u'<Race: %s>' % self.__unicode__()


class ReportingUnit(object):
    """
    An area or unit that groups votes into a total.
    
    For instance, a state, a congressional district, a county.
    """
    def __init__(self, ap_number=None, name=None, abbrev=None, fips=None,
                 precincts_total=None, num_reg_voters=None):
        self.ap_number = ap_number
        self.name = name
        self.abbrev = abbrev
        self.fips = fips
        self.precincts_total = precincts_total
        self.num_reg_voters = num_reg_voters
        self._results = {}

    @property
    def results(self):
        return self._results.values()

    def results_for_race(self, race):
        if isinstance(race, Race):
            race = race.ap_race_number
        return [o for o in self._results.values() if o.race.ap_race_number == race]

    def update_result(self, result):
        self._results[result.candidate.ap_polra_number] = result

    @property
    def is_state(self):
        return self.fips == '00000'

    def __unicode__(self):
        name = self.name
        if self.is_state:
            name = '%s (state)' % name
        return name

    def __repr__(self):
        return u'<ReportingUnit: %s>' % self.__unicode__()


class Result(object):
    """
    The actual vote count for a candidate in a race in a particular reporting unit.
    
    Also, the percent reporting.
    """
    def __init__(self, race=None, candidate=None,
                 reporting_unit=None, vote_total=None, precincts_reporting=None,
                 precincts_reporting_percent=None):
        self.race = race
        self.candidate = candidate
        self.reporting_unit = reporting_unit
        self.vote_total = vote_total
        self.precincts_reporting = precincts_reporting
        self.precincts_reporting_percent = precincts_reporting_percent

    def __unicode__(self):
        return u'%s, %s, %s' % (self.candidate, self.reporting_unit,
                                self.vote_total)

    def __repr__(self):
        return u'<Result: %s>' % self.__unicode__()


