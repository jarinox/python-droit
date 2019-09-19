
# Tutorial: Erster Bot mit python-droit

## Einführung
Droit ist ein einfaches und mächtiges Werkzeug um Bots zu erstellen. Es existieren verschiedene Versionen von Droit in verschiedenen Programmiersprachen - sie alle benutzen den [Droit Database Script](https://github.com/jaybeejs/python-droit/blob/master/docs/Droit%20Database%20Script.md). Diese Skriptsprache definiert Fragen und zugehörige Antworten. Diese Zuweisungen sind jedoch dynamisch, sodass eine Zuweißung auf verschiedene Eingaben zutreffen kann. Genauso sind für die selbe Eingabe verschiedene Ausgaben möglich.

In diesem Tutorial wollen wir einen einfachen Assistenten schreiben, mit dem wir uns unterhalten können und der kleine Aufgaben für uns erledigt. Dazu verwenden wir die Programmiersprache Python (Version 3) und das python-droit Module.

Viel Spaß beim Programmieren!


## Installation
Lade dir python-droit herunter.

    git clone https://github.com/jaybeejs/python-droit.git

Nun musst du das Verzeichnis `python-droit` in `pydroit` umbenennen.

    mv python-droit pydroit

Dein Programm, das python-droit nutzen soll, muss nun im übergeordneten Ordener platziert werden.

## Minimaler Bot
Ein minimaler Bot für Droit macht das folgende:
- Nutzereingabe lesen
- Droit Database Script (DDS) einlesen
- DDS nach passender Zuweißung durchsuchen
- Antwort berechnen
- Antwort ausgeben

Der Code sieht so aus:

```
from pydroit import core as droit

running = True

while(running):
    try:
        eingabe = input("Geben Sie etwas ein: ")                 # Nutzereingabe einlesen
        eingabe-vorbereitet = droit.prepareInput(eingabe)        # Nutzereingabe wird für den Computer leserlich gemacht
        dda = droit.parseDDA("dateiname-der-datenbank.dda")      # Zuweißungen werden aus einer Datei eingelesen
        zuweissungen = droit.useRules(dda, eingabe-vorbereitet)  # Es wird eine passende Zuweißung gesucht
        if(zuweissungen != []):                                                               # Falls ein Ergebnis gefunden wird...
            variablen = droit.createVariables(inpVars=zuweissungen[0][1], userinput=eingabe)  # Erstelle Variablen
            ausgabe = droit.formatOut(zuweissungen[0][0], variablen)                          # Berechne die Ausgabe aus
            print(ausgabe)                                                                    # Gebe die Ausgabe aus
        else:                                                                                 # ...sonst
            print("Darauf kenne ich leider keine Antwort!")                                   # Gib eine Standartantwort aus
    except KeyboardInterrupt:                                    # Falls STRG+C gedrückt
        running = False                                          # Beende die Schleife uns schließe das Programm
```


Damit dieser Bot funktioniert, benötigen wir eine DDS Datei. Für den Anfang kannst du dir eine vorgefertigte Datei hier [herunterladen](http://localhost:3000/droit/general-resources/src/branch/master/DDS/german-sample.dda).


## Eigener DDS Script

Die erste Methode um dem Bot weiter Funktionen hinzuzufügen ist, die .dda Datei (mit dem DDS) zu erweitern.
Hilfreich um die Skriptsprache zu lernen ist die [Dokumentation zum Droit Database Script](https://github.com/jaybeejs/python-droit/blob/master/docs/Documentation.md). Diese Dokumentation ist sehr hilfreich - du kannst immer zu ihr zurückkehren und die Funktionsweiße des DDS nachschlagen.

Wir wollen nun das `math` Plugin von python-droit ansprechen. Der DDS Script sieht so aus:

``` no-highlight
TEXT!berechne:INP2*formel!->VAR!inp.formal:TEXT! = :EVAL!math.equal(*inp.formel)
```

Diese Zuweißung sagt das folgende aus:
- Die Eingabe muss das Wort "berechne" enthalten
- Alle darauffolgenden Zeichen werden eingelesen und in der Variable `formel` gespeichert
- Die Ausgabe beginnt mit der in die Variable eingelesenen Formel
- Daran wird das `=` Zeichen gehängt
- Das Plugin `math` berechnet nun das Ergebnis und hängt es hinter das `=` Zeichen

