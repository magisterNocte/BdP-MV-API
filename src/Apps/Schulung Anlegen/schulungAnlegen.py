
import pathlib

from decouple import config
from openpyxl import load_workbook
from Tools.APITools import Nami
from Tools.EditUser import EditUser

# variables
path = str(pathlib.Path(__file__).parent.resolve())
username = config("MVUSERNAME")
password = config("PASSWORD")


config = []
nami = Nami(config)
nami.auth(username, password)

tempUser = EditUser(nami, "yannik", "menge")
#tempUser.schulungAnlegen(17, "yAnnik", "MenGe", "2022-12-11")
tempUser.taetigkeitAnlegen(193, "Leviatan 077222", 253, "2022-12-11")
