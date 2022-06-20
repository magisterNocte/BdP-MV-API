import logging
import pathlib

from decouple import config
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
from Tools.APITools import Nami
from Tools.UserInfo import UserInfo as UserInfo

logging.basicConfig(level=logging.INFO)
# variables
path = str(pathlib.Path(__file__).parent.resolve())
username = config("MVUSERNAME")
password = config("PASSWORD")


config = []
nami = Nami(config)
nami.auth(username, password)

user = nami.search({"mitgliedsNummber": "57755"}, 10)  # API Call

# die ersten zwei Stellen der StammesID stehen für den LV, 07 ist Niedersachsen
if user[0]["entries_gruppierung"][-6:-4] == "07":
    print("Dieser User ist in einem Stamm aus Niedersachsen")


https: // mv.meinbdp.de/ica/rest/nami/search-multi/result-list?_dc = 1655278973138 & searchedValues = {"mitgliedsNummber": "57755""inGrp": True, "searchType": "MITGLIEDER"} & page = 1 & start = 0 & limit = 10
