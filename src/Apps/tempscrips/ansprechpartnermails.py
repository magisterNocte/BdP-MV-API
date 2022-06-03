import logging
import pathlib

from decouple import config
from openpyxl import load_workbook
from Tools.APITools import Nami

logging.basicConfig(level=logging.ERROR)
# variables
path = str(pathlib.Path(__file__).parent.resolve())
username = config("MVUSERNAME")
password = config("PASSWORD")


config = []
nami = Nami(config)
nami.auth(username, password)

# excel init
sourceWb = load_workbook(path + "\data\sourceData.xlsx")
sourceWs = sourceWb.active


for i in range(2, sourceWs.max_row + 1):
    if not sourceWs["A" + str(i)].value:
        continue
    print(sourceWs["A" + str(i)].value)
    try:
        sourceWs["O" + str(i)] = ",".join(i["entries_email"] for i in nami.search(
            {"taetigkeitId": [10648], "gruppierung3Id": [int(sourceWs["A" + str(i)].value)]}, 10))
    except:
        sourceWs["O" + str(i)] = "Error"
    try:
        sourceWs["P" + str(i)] = ",".join(i["entries_email"] for i in nami.search(
            {"taetigkeitId": [148, 170], "gruppierung3Id": [int(sourceWs["A" + str(i)].value)]}, 10))
    except:
        sourceWs["P" + str(i)] = "Error"


sourceWb.save(path + "\\data\\sourceData.xlsx")
