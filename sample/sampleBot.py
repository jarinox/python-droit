import core as droit

running = True

dda = droit.parseDDA("german-sample.dda")      # Zuweißungen werden aus einer Datei eingelesen

while(running):
    try:
        eingabe = input("Geben Sie etwas ein: ")                 # Nutzereingabe einlesen
        eingabeVorbereitet = droit.prepareInput(eingabe)        # Nutzereingabe wird für den Computer leserlich gemacht
        zuweissungen = droit.useRules(dda, eingabeVorbereitet)  # Es wird eine passende Zuweißung gesucht
        if(zuweissungen != []):                                                               # Falls ein Ergebnis gefunden wird...
            variablen = droit.createVariables(inpVars=zuweissungen[0][1], userinput=eingabe)  # Erstelle Variablen
            ausgabe = droit.formatOut(zuweissungen[0][0], variablen)                          # Berechne die Ausgabe aus
            print(ausgabe)                                                                    # Gebe die Ausgabe aus
        else:                                                                                 # ...sonst
            print("Darauf kenne ich leider keine Antwort!")                                   # Gib eine Standartantwort aus
    except KeyboardInterrupt:                                    # Falls STRG+C gedrückt
        running = False                                          # Beende die Schleife uns schließe das Programm

