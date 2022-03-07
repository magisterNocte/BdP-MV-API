import pathlib

from API.APITools import Console as c
from API.APITools import Nami
from decouple import config

username = config("USER")
password = config("PASSWORD")


config = []
nami = Nami(config)
nami.auth(username, password)


print(Nami.fuehrungsZeugnis(nami, "57755"))

print(Nami.user(nami, "yannik", "menge"))
