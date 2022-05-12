from Tools.UserInfo import UserInfo


class EditUser:
    def __init__(self, nami, vorname, nachname):
        self.user = nami.user(vorname, nachname)
        self.mglied = UserInfo.getUserIDAndData(
            nami, self.user, vorname, nachname)[0]
        self.nami = nami
        self.vorname = vorname
        self.nachname = nachname

    def schulungAnlegen(self, schulungsId,  datum,alterNativerName=""):
        self.nami.schulungAnlegen(
            self.mglied, schulungsId, self.vorname, self.nachname, datum, alterNativerName)

    def taetigkeitAnlegen(self, taetigkeitsId, gruppierungsName, gruppierungsID, aktivVon, aktivBis=None):
        self.nami.taetigkeitAnlegen(
            self.mglied, taetigkeitsId, gruppierungsName, gruppierungsID, aktivVon, aktivBis)
    # gruppierungsID,
