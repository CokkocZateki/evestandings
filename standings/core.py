try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from eveapi import EVEAPIConnection
from jinja2 import Environment, PackageLoader

STANDINGS_ALLIANCE = 0
STANDINGS_CORPORATION = 1


class Standings(object):
    """Grabs the latest Standings from the EVE API and outputs them into a nice template format"""

    def __init__(self, keyid, vcode):
        self.eveapi = EVEAPIConnection().auth(keyID=keyid, vCode=vcode)
        self.standings_type = type

    @staticmethod
    def _parse_list(standingslist, output):
        for row in standingslist:
            level = float(row['standing'])
            if level > 5:
                type = 'Excellent'
            elif level > 0:
                type = 'Good'
            elif level >= -5:
                type = 'Bad'
            elif level >= -10:
                type = 'Terrible'
            else:
                type = 'Neutral'

            if row['contactTypeID'] == 16159:
                rowtype = 'Alliance'
            elif row['contactTypeID'] == 2:
                rowtype = 'Corporation'
            else:
                rowtype = 'Character'

            output[type].append((rowtype, row['contactID'], row['contactName'], row['standing']))

    def _get_standings(self):
        if hasattr(self, '_standings_cache'):
            return self._standings_cache
        res = self.eveapi.corp.ContactList()
        standings = OrderedDict((x, []) for x in ['Excellent', 'Good', 'Neutral', 'Bad', 'Terrible'])
        self._parse_list(res.allianceContactList, standings)
        self._parse_list(res.corporateContactList, standings)
        for x in ['Excellent', 'Good', 'Neutral', 'Bad', 'Terrible']:
            standings[x] = sorted(standings[x], key=lambda v: -int(v[3]))
        self._standings_cache = standings
        return standings

    def render_template(self, template):
        env = Environment(loader=PackageLoader('standings', 'templates'))
        template = env.get_template(template)
        return template.render(standings=self._get_standings())

    def html(self):
        return self.render_template('standings_list.html')

    def text(self):
        return self.render_template('standings_list.txt')
