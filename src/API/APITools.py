# docs: https://doku.dpsg.de/display/NAMI/Service+Architektur

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


class Nami(object):

    def __init__(self, config):
        self.s = requests.Session()
        self.config = {
            'server': 'https://mv.meinbdp.de',
            'auth_url': '/ica/rest/nami/auth/manual/sessionStartup',
            'search_url': '/ica/rest/api/1/2/service/nami/search/result-list'
        }
        self.config.update(config)

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

    def user(self, mitglied_vorname, mitglied_nachname, method='GET'):
        url = f'https://mv.meinbdp.de/ica/rest/nami/search-multi/result-list?_dc=1636399371787&searchedValues=%7B%22vorname%22%3A%22{mitglied_vorname}%22%2C%22nachname%22%3A%22{mitglied_nachname}%22%2C%22spitzname%22%3A%22%22%2C%22mitgliedsNummber%22%3A%22%22%2C%22mglWohnort%22%3A%22%22%2C%22alterVon%22%3A%22%22%2C%22alterBis%22%3A%22%22%2C%22mglStatusId%22%3Anull%2C%22funktion%22%3A%22%22%2C%22mglTypeId%22%3A%5B%5D%2C%22organisation%22%3A%22%22%2C%22tagId%22%3A%5B%5D%2C%22bausteinIncludedId%22%3A%5B%5D%2C%22zeitschriftenversand%22%3Afalse%2C%22searchName%22%3A%22%22%2C%22taetigkeitId%22%3A%5B%5D%2C%22untergliederungId%22%3A%5B%5D%2C%22mitAllenTaetigkeiten%22%3Afalse%2C%22withEndedTaetigkeiten%22%3Afalse%2C%22ebeneId%22%3Anull%2C%22grpNummer%22%3A%22%22%2C%22grpName%22%3A%22%22%2C%22gruppierung1Id%22%3Anull%2C%22gruppierung2Id%22%3Anull%2C%22gruppierung3Id%22%3Anull%2C%22gruppierung4Id%22%3Anull%2C%22gruppierung5Id%22%3Anull%2C%22gruppierung6Id%22%3Anull%2C%22inGrp%22%3Afalse%2C%22unterhalbGrp%22%3Afalse%2C%22privacy%22%3A%22%22%2C%22searchType%22%3A%22MITGLIEDER%22%7D&page=1&start=0&limit=10'

        r = self.s.request(method, url)

        return self._check_response(r)

    def taetigkeit(self, mglid, method='GET'):
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

    def schulungAnlegen(self, mglied, schulung, method="POST"):
        payload = {
            "baustein": None,
            "bausteinId": 17,
            "mitglied": "Menge, Yannik",
            "vstgTag": "2022-03-19T00:00:00",
            "vstgName": "",
            "veranstalter": "",
            "lastModifiedFrom": None
        }
        url = f'ttps://mv.meinbdp.de/ica/rest/nami/mitglied-ausbildung/filtered-for-navigation/mitglied/mitglied/57755'
        r = self.s.post(url, data=payload)
        if r.status_code != 200:
            raise ValueError('mod failed')
        return self.s


class Console():
    def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                         (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
        # Print New Line on Complete
        if iteration == total:
            print()
