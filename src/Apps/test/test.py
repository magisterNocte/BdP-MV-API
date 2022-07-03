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

print(",".join(i["entries_email"] for i in nami.search(
    {"taetigkeitId": [10648], "gruppierung3Id": 474
     }, 9999)))
print(",".join(i["entries_email"] for i in nami.search(
    {"taetigkeitId": [148], "gruppierung3Id": 474

     }, 9999)))
print(",".join(i["entries_email"] for i in nami.search(
    {"taetigkeitId": [170], "gruppierung3Id": 474
     }, 9999)))
