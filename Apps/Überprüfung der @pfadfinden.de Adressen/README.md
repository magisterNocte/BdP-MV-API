Anwendung zur Überprüfung der @pfadfinden.de Email Adressen

0. Einen MV Zugriff mit Rechten alle Accounts zu sehen in der userconf.py eintragen
1. Liste mit allen Email Adressen von Outlook exportieren
2. Datei in Excel als "outlook_data.xlsx" im "data" Ordner abspeichern.
3. outlookconverter.p< ausführen
4. Es wird erstellt...
    - eine übersichtbare Tabelle aller Daten
    - eine Tabelle mit allen Weiterleitungen
    - eine Tabelle mit allen Postfächern
    - eine Tabelle mit allen Adressen die nicht nach Personen benannt wurden
5. Überprüfung der @pfadfinden.de Adressen.py ausführen.
6. In den Tabellen werden ergänzt...
    - die letzte Tätigkeit auf Bundesebene
    - das Datum, wann sie beendet wurde
7. Fehlermeldungen in der Tabelle
    - kein Datum bedeutet, dass die Tätigkeit noch nicht beendet ist
    - ERROR1 bedeutet, dass der user nicht in der MV ist
    - "keine Bundestätigkeit" und das Datum "0000-00-00" bedeutet dass der user keine Bundestätigkeit in der MV stehen hat

Die Funktion looped durch alle user in einer Tabelle und ergänzt die letzte Tätigkeit auf Bundesebene und das Datum, wann sie beendet wurde
