import pathlib

from API.APITools import Console as c
from API.APITools import Nami
from decouple import config

username = config("USER")
password = config("PASSWORD")


config = []
nami = Nami(config)
nami.auth(username, password)


print(Nami.fuehrungsZeugnisInfo(nami, "57755")[0]["entries_erstelltAm"])

