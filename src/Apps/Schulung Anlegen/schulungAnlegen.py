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


UID.schulungAnlegen()
