import csv
from datetime import datetime, timedelta

import Data


class Utility:
    @staticmethod
    def formatDate(date):
        newDate = date[8:10] + "." + date[5:7] + "." + date[0:4]
        return newDate

    @staticmethod
    def checkValidDate(date, dayOffsetDays=0):
        datetime_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        if not date:
            return True
        if datetime.now() + timedelta(days=dayOffsetDays) > datetime_obj:
            return False
        return True

    @staticmethod
    def plzZuBundesland(plz):
        with open(Data.dataPath + '\\plzListe.csv') as f:

            plzCsv = csv.DictReader(f, delimiter=';')
            for item in plzCsv:
                if item["ï»¿PLZ"] == plz:
                    return item["Bundesland"]

            return "ERROR: PLZ zu Bundesland geht nicht"

    @staticmethod
    def stammesIdToLV(stammesID):
        match str(stammesID)[-6:-4]:
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

    @staticmethod
    def getIDsFromCsvAsList(filename):
        with open(f'{Data.dataPath}\\{filename}', encoding='utf-8-sig') as f:
            idCSV = csv.reader(f)
            idList = map(lambda x:  f'({x[0]})', list(idCSV))
        return list(idList)
