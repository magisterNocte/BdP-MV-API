import pathlib
from operator import itemgetter

from decouple import config
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter

from API.APITools import Console as c
from API.APITools import Nami

# variables

class UserIDAndData(object):
    def compareUserDataToInput(user,vorname,nachname):
        try:
            if len(user) == 1:

                return user[0]["entries_id"]
            for i in user:
                if i["entries_vorname"]== vorname and i["entries_nachname"] == nachname:
                    return i["entries_id"]
                if i["entries_vorname"] != vorname:
                    errorMessage = "ERROR: Fehler beim Vorname!"
                if i["entries_nachname"] != nachname:
                    errorMessage = "ERROR: Fehler beim Nachname!"
            return errorMessage

        except:
            return ["ERROR: compareUserDataToInput"]
        



    def getUserIDAndData(nami, user, vorname, name):
        try:
            if user == []:
                return ["ERROR: No user!"]
            id = UserIDAndData.compareUserDataToInput(user,vorname,name)
            if isinstance (id,int) == True:
                return [id, nami.userById(id)]
            return [id]
        except:
            return ["ERROR: getUserID"]

        

    def stammesIdToLV(stammesID):
    
        match stammesID[-6:-4]:
            case "01":
                return ["Baden-Württemberg","BaWü"]
            case "02":
                return ["Bayern","Bayern"]
            case "03":
                return ["Berlin/Brandenburg","BBB"]
            case "04":
                return ["Bremen","Bremen"]
            case "05":
                return ["Hessen","Hessen"]
            case "06":
                return ["Mecklenburg-Vorpommern","Mecklenburg-Vorpommern"]
            case "07":
                return ["Niedersachsen","NDS"]
            case "08":
                return ["Nordrein-Westfalen","NRW"]
            case "09":
                return ["Rheinland-Pfalz/Saar","RPS"]
            case "10":
                return ["Sachsen","Sachsen"]
            case "11":
                return ["Sachsen-Anhalt","Sachsen-Anhalt"]
            case "12":
                return ["Schleswig-Holsten/Hamburg","SHHH"]
            case "13":
                return ["Thüringen","Thüringen"]
            case "14":
                return ["BUND", "BUND"]
                    
        


