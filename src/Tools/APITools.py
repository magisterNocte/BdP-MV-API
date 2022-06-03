# docs: https://doku.dpsg.de/display/NAMI/Service+Architektur

import json
import urllib.parse

import requests
from decouple import config


class NamiResponseTypeError(Exception):
    pass


class NamiResponseSuccessError(Exception):
    """
    This is being raised when the response 'success' field is not True
    """
    pass


class NamiHTTPError(Exception):
    pass


class Nami():

    def __init__(self, config):
        self.s = requests.Session()
        self.config = {
            'server': 'https://mv.meinbdp.de',
            'auth_url': '/ica/rest/nami/auth/manual/sessionStartup',
            'search_url': '/ica/rest/api/1/2/service/nami/search/result-list'
        }
        self.config.update(config)

    def __del__(self):
        self.s.close()

    def auth(self, username, password):
        payload = {
            'Login': 'API',
            'username': username,
            'password': password
        }

        url = "%s%s" % (self.config['server'], self.config['auth_url'])
        r = self.s.post(url, data=payload)
        if r.status_code != 200:
            raise ValueError('authentication failed')

        return self.s

    def _check_response(self, response):
        if response.status_code != requests.codes.ok:  # pylint: disable=E1101
            raise NamiHTTPError('HTTP Error. Status Code: %s' %
                                response.status_code)

        rjson = response.json()
        if not rjson['success']:
            raise NamiResponseSuccessError(
                'succes state from NAMI was %s %s' % (rjson['message'], rjson))
        return rjson['data']

    # generelle search funktion
    def search(self, parameter: dict, limit: 1):

        parameter["searchType"] = "MITGLIEDER"
        parameter["inGrp"] = True
        search_value = json.dumps(parameter)
        search_values = urllib.parse.quote(search_value)
        limit = int(limit)
        start = 0
        page = 1

        url = f'https://mv.meinbdp.de/ica/rest/nami/search-multi/result-list?_dc=1652274221216&searchedValues={search_values}&page={page}&start={start}&limit={limit}'
        r = self.s.request('GET', url)

        return self._check_response(r)

    # GET requests

    def user(self, mitglied_vorname, mitglied_nachname, method='GET'):
        url = f'https://mv.meinbdp.de/ica/rest/nami/search-multi/result-list?_dc=1636399371787&searchedValues=%7B%22vorname%22%3A%22{mitglied_vorname}%22%2C%22nachname%22%3A%22{mitglied_nachname}%22%2C%22spitzname%22%3A%22%22%2C%22mitgliedsNummber%22%3A%22%22%2C%22mglWohnort%22%3A%22%22%2C%22alterVon%22%3A%22%22%2C%22alterBis%22%3A%22%22%2C%22mglStatusId%22%3Anull%2C%22funktion%22%3A%22%22%2C%22mglTypeId%22%3A%5B%5D%2C%22organisation%22%3A%22%22%2C%22tagId%22%3A%5B%5D%2C%22bausteinIncludedId%22%3A%5B%5D%2C%22zeitschriftenversand%22%3Afalse%2C%22searchName%22%3A%22%22%2C%22taetigkeitId%22%3A%5B%5D%2C%22untergliederungId%22%3A%5B%5D%2C%22mitAllenTaetigkeiten%22%3Afalse%2C%22withEndedTaetigkeiten%22%3Afalse%2C%22ebeneId%22%3Anull%2C%22grpNummer%22%3A%22%22%2C%22grpName%22%3A%22%22%2C%22gruppierung1Id%22%3Anull%2C%22gruppierung2Id%22%3Anull%2C%22gruppierung3Id%22%3Anull%2C%22gruppierung4Id%22%3Anull%2C%22gruppierung5Id%22%3Anull%2C%22gruppierung6Id%22%3Anull%2C%22inGrp%22%3Afalse%2C%22unterhalbGrp%22%3Afalse%2C%22privacy%22%3A%22%22%2C%22searchType%22%3A%22MITGLIEDER%22%7D&page=1&start=0&limit=10'

        r = self.s.request(method, url)

        return self._check_response(r)

    def userTaetigkeit(self, mglid, method='GET'):
        url = "%s/ica/rest/nami/zugeordnete-taetigkeiten/filtered-for-navigation/gruppierung-mitglied/mitglied/%s/flist?_dc=1636459771397&page=1&start=0&limit=20" % (
            self.config['server'], mglid)
        r = self.s.request(method, url)
        return self._check_response(r)

    def taetigkeitById(self, mglid, taetigkeitId, method='GET'):
        url = "%s/ica/rest/nami/zugeordnete-taetigkeiten/filtered-for-navigation/gruppierung-mitglied/mitglied/%s/flist?_dc=1636459771397&page=1&start=0&limit=20/%s" % (
            self.config['server'], mglid, taetigkeitId)
        r = self.s.request(method, url)
        return self._check_response(r)

    def fuehrungsZeugnisInfo(self, mglied, method='GET'):
        url = "%s/ica/rest/nami/mitglied-sgb-acht/filtered-for-navigation/empfaenger/empfaenger/%s/flist?_dc = 1646639062672 & page = 1 & start = 0 & limit = 10" % (
            self.config['server'], mglied)
        r = self.s.request(method, url)
        return self._check_response(r)

    def userById(self, mglied, method="GET"):

        url = f'https://mv.meinbdp.de/ica/rest/nami/mitglied/filtered-for-navigation/gruppierung/gruppierung/253/{mglied}?_dc=1647435214372'
        r = self.s.request(method, url)
        return self._check_response(r)

    def userMitTätigkeit(self, tätigkeitID, method='GET'):
        url = f'https://mv.meinbdp.de/ica/rest/nami/search-multi/result-list?_dc=1652274221216&searchedValues=%7B%22taetigkeitId%22%3A%5B{tätigkeitID}%5D%2C%22searchType%22%3A%22MITGLIEDER%22%7D&page=1&start=0&limit=9999'
        r = self.s.request(method, url)

        return self._check_response(r)

    def userSchulung(self, mglied, method='GET'):
        url = f'https://mv.meinbdp.de/ica/rest/nami/mitglied-ausbildung/filtered-for-navigation/mitglied/mitglied/{mglied}/flist?_dc=1654165754686&page=1&start=0&limit=40'
        r = self.s.request(method, url)

        return self._check_response(r)

    # POST requests

    def schulungAnlegen(self, mglied, schulungsId, vorname, nachname, datum, alterNativerName):  # mglied, schulung
        payload = {
            'baustein': None,
            'bausteinId': schulungsId,  # TODO: liste mit schulungsbausteinsids herrausfinden
            'mitglied': f'{nachname.lower().capitalize()}, {vorname.lower().capitalize()}',
            'vstgTag': f'{datum}T00:00:00',
            'vstgName': alterNativerName,
            'veranstalter': '',
            'lastModifiedFrom': None
        }
        url = f"https://mv.meinbdp.de/ica/rest/nami/mitglied-ausbildung/filtered-for-navigation/mitglied/mitglied/{mglied}"
        r = self.s.post(url, json=payload)
        if r.status_code != 200:
            print(r.status_code)
            raise ValueError('mod failed')
        return self.s

    def taetigkeitAnlegen(self, mglied, taetigkeitsId, gruppierungsName, gruppierungsID, aktivVon, aktivBis=None):
        payload = {
            'aktivBis': f'{aktivBis}T00:00:00',
            'aktivVon': f'{aktivVon}T00:00:00',
            'beitragsArtId': None,
            'caeaGroupForGfId': None,
            'caeaGroupId': None,
            'gruppierung': gruppierungsName,
            'gruppierungId': gruppierungsID,
            'taetigkeitId': taetigkeitsId,
            'untergliederungId': None

        }

        url = f"https://mv.meinbdp.de/ica/rest/nami/zugeordnete-taetigkeiten/filtered-for-navigation/gruppierung-mitglied/mitglied/{mglied}"
        r = self.s.post(url, json=payload)
        if r.status_code != 200:
            print(r.status_code)
            raise ValueError('mod failed')
        return self.s
