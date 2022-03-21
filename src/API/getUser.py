import csv
import pathlib
from operator import itemgetter

from decouple import config
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter

from API.APITools import Console as c
from API.APITools import Nami

# variables


class UserIDAndData(object):
    path = str(pathlib.Path(__file__).parent.resolve())
    bundesTaetigkeitIDs = [
        """
    Liste aller Bundestätigkeiten IDs in der MV
    """
        "(100)",
        "(107)",
        "(108)",
        "(109)",
        "(111)",
        "(112)",
        "(114)",
        "(116)",
        "(138)",
        "(139)",
        "(140)",
        "(141)",
        "(142)",
        "(152)",
        "(163)",
        "(165)",
        "(166)",
        "(174)",
        "(175)",
        "(184)",
        "(187)",
        "(10,028)",
        "(10,035)",
        "(10,036)",
        "(10,037)",
        "(10,038)",
        "(10,039)",
        "(10,046)",
        "(10,047)",
        "(10,051)",
        "(10,053)",
        "(10,577)",
        "(10,651)",
        "(10,663)"
    ]
    bulaTätigkeitenIDs = [
        "(10,049)",
        "(10,061)",
        "(10,050)",
        "(10,058)",
        "(10,059)",
        "(10,060)",
        "(10,577)",
        "(10,651)",
        "(10,652)",
        "(10,663)",
        "(10,035)",
        "(10,036)",
        "(10,037)",
        "(10,038)",
        "(10,039)",
        "(10,040)",
        "(10,041)",
        "(10,042)",
        "(10,043)",
        "(10,044)",
        "(10,045)",
        "(10,046)",
        "(10,047)",
        "(10,048)",
        "(10,033)",
        "(10,053)",






    ]

    def compareUserDataToInput(user, vorname, nachname):
        returnVar = []
        try:
            if len(user) == 1:

                return user[0]["entries_id"]
            for i in user:
                if i["entries_vorname"] == vorname and i["entries_nachname"] == nachname:
                    returnVar.append(i["entries_id"])
                if i["entries_vorname"] != vorname:
                    returnVar.append("ERROR: Fehler beim Vorname!")
                if i["entries_nachname"] != nachname:
                    returnVar.append("ERROR: Fehler beim Nachname!")

            if len(returnVar[0]) != 1:
                return "ERROR : Mehr als ein user mit dem gleichen Namen"
            return returnVar[0]

        except:
            return ["ERROR: compareUserDataToInput"]

    def getUserIDAndData(nami, user, vorname, name):
        try:
            if user == []:
                return ["ERROR: No user!"]
            id = UserIDAndData.compareUserDataToInput(user, vorname, name)
            if isinstance(id, int) == True:
                return [id, nami.userById(id)]
            return [id]
        except:
            return ["ERROR: getUserID"]

    def getUserEfZInfo(nami, user):
        try:
            return Nami.fuehrungsZeugnisInfo(nami, user)[0]["entries_erstelltAm"]
        except:
            return "ERROR: Kein efz Eintrag!"

    def stammesIdToLV(stammesID):

        match stammesID[-6:-4]:
            case "01":
                return ["Baden-Württemberg", "BaWü"]
            case "02":
                return ["Bayern", "Bayern"]
            case "03":
                return ["Berlin/Brandenburg", "BBB"]
            case "04":
                return ["Bremen", "Bremen"]
            case "05":
                return ["Hessen", "Hessen"]
            case "06":
                return ["Mecklenburg-Vorpommern", "Mecklenburg-Vorpommern"]
            case "07":
                return ["Niedersachsen", "NDS"]
            case "08":
                return ["Nordrein-Westfalen", "NRW"]
            case "09":
                return ["Rheinland-Pfalz/Saar", "RPS"]
            case "10":
                return ["Sachsen", "Sachsen"]
            case "11":
                return ["Sachsen-Anhalt", "Sachsen-Anhalt"]
            case "12":
                return ["Schleswig-Holsten/Hamburg", "SHHH"]
            case "13":
                return ["Thüringen", "Thüringen"]
            case "14":
                return ["BUND", "BUND"]

    def plzZuBundesland(plz):
        f = open(UserIDAndData.path + '\data\plzListe.csv')
        plzCsv = csv.DictReader(f, delimiter=';')
        for item in plzCsv:
            if item["ï»¿PLZ"] == plz:
                return item["Bundesland"]

    def userFunktion(nami, userId, filterList):

        try:
            for i in nami.taetigkeit(userId):
                for x in filterList:
                    if x in i['entries_taetigkeit']:
                        return i['entries_taetigkeit']
            return "keine Tätigkeit (ERROR)"

        except:
            return "ERROR: Fehler bei den tätigkeiten"

    def schulungAnlegen(nami, userID):
        nami.schulungAnlegen()
