from Tools.APITools import Nami
from Tools.Utility import Utility


class UserInfo():
    @staticmethod
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
            return "ERROR: compareUserDataToInput"

    @staticmethod
    def getUserIDAndData(nami, user, vorname, name):
        try:
            if user == []:
                return ["ERROR: No user!"]
            id = UserInfo.compareUserDataToInput(user, vorname, name)
            if isinstance(id, int) == True:
                return [id, nami.userById(id)]
            return [id]
        except:
            return ["ERROR: getUserID"]

    @staticmethod
    def getUserEfZInfo(nami, user):
        try:
            return Nami.fuehrungsZeugnisInfo(nami, user)[0]["entries_erstelltAm"]
        except:
            return "ERROR: Kein efz Eintrag!"

    @staticmethod
    def userTätigkeit(nami, userId, filterList, dateToCompare=0):
        for i in nami.taetigkeit(userId):
            for x in Utility.getIDsFromCsvAsList(filterList):
                if not x in i['entries_taetigkeit']:
                    continue
                if i["entries_aktivBis"] != "":
                    if not Utility.checkValidDate(i["entries_aktivBis"], dateToCompare):
                        continue
                return i['entries_taetigkeit']
        return "ERROR: keine Tätigkeit (ERROR)"
