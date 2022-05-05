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
username = config("USER")
password = config("PASSWORD")


config = []
nami = Nami(config)
nami.auth(username, password)
