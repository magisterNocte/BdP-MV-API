import pathlib

from API.APITools import Nami
from API.getUser import UserIDAndData as UID
from decouple import config
from openpyxl import load_workbook

# variables
path = str(pathlib.Path(__file__).parent.resolve())
username = config("USER")
password = config("PASSWORD")


config = []
nami = Nami(config)
nami.auth(username, password)

# excel init
sourceWb = load_workbook(path + "\data\data.xlsx")
sourceWs = sourceWb.active


def fillInExcel(userDetails, thisRow):

    try:
        if isinstance(userDetails[0], int) == True:

            sourceWs["C" + thisRow] = userDetails[1]["strasse"]
            sourceWs["D" + thisRow] = userDetails[1]["plz"] + \
                " " + userDetails[1]["ort"]
            sourceWs["E" + thisRow] = "m" if userDetails[1]["geschlecht"] == "männlich" else "w"
            sourceWs["F" +
                     thisRow] = UID.plzZuBundesland(userDetails[1]["plz"])
            sourceWs["G" + thisRow] = "E"
            sourceWs["H" + thisRow] = UID.userFunktion(
                nami, userDetails[0], UID.bulaTätigkeitenIDs)[0:-8]
            sourceWs["I" +
                     thisRow] = UID.stammesIdToLV(userDetails[1]["gruppierung"])[1]
            sourceWs["J" + thisRow] = UID.getUserEfZInfo(nami, userDetails[0])
        else:
            sourceWs["C" + thisRow] = userDetails[0]
    except:
        sourceWs["C" + thisRow] = "ERROR: Fehler beim Excel ausfüllen!"


thisRow = 1
for row in sourceWs.iter_rows():

    try:
        vornameTemp = sourceWs["A" + str(thisRow)].value.strip().split()[0]
        nachnameTemp = sourceWs["B" + str(thisRow)].value.strip()
        print(vornameTemp, nachnameTemp)
        user = nami.user(vornameTemp, nachnameTemp)
        userDetails = UID.getUserIDAndData(
            nami, user, vornameTemp, nachnameTemp)

        fillInExcel(userDetails, str(thisRow))

    except:
        sourceWs["C" + str(thisRow)] = "ERROR!"

    thisRow += 1


sourceWb.save(path + "\data\data.xlsx")
