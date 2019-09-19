# Droit Database Script
Droit Database Script (DDS) einfache aber leistungsstarke Skriptsprache für Frage-zu-Antwort Datenbanken von Bots. Normalerweiße werden DDS in Droit Database (.dda) Datein gespeichert.

## Struktur
Ein DDS besitzt eine einfache Struktur: `EINGABEBLOCKS!argumente->AUSGABEBLOCKS!argumente`

### Regeln
1. Jede Zeile ist eine neue Regel.
2. Ein- und Ausgabeblöcke werden mit `->` getrennt.
3. Blöcke werden mit einem Doppelpunkt getrennt.
4. Blockname und Argumente werden mit einem Ausrufezeichen getrennt.
5. Argumente von Inputblöcken weden klein geschrieben - bots die DDS nutzen sind nicht case-sensitive.
6. In Ausgabeblöcke werde Ausrufezeichen durch `&arz;` und Doppelpunkte mit `&dpp;` ersetzt.
7. Blöcke, die eine Variable deklarieren, definieren den Variablenname nach einem Stern.
8. Zeilen ohne `->` weden wie Kommentare behandelt und ignoriert

### Blöcke
Es gibt verschiedene Blöcke - manche Blöcke werden von verschiedenen Programmen und Portierungen nicht unterstützt. Dies ist eine Sammlung der grundlegenden Blöcke.

#### TEXT (input)
Eines der durch Kommas getrennten Wörter, die als Argument gegeben sind, muss in der Nutzereingabe enthalten sein.
Usage: `TEXT!wort1,wort2,wort3`

#### NOTX (input)
Keines der durch Kommas getrennten Wörter, die als Argument gegeben sind, darf in der Nutzereingabe enthalten sein. Dies wird hauptsächlich dafür benutzt, um Verneinungen zu erkennen und zu umgehen.
Usage: `NOTX!nein,nicht`

#### SRTX (input)
Einer der durch Kommas getrennten Sätze, die als Argument gegeben sind, muss in der Nutzereingabe enthalten sein. Dieser Block kann nicht mit anderen Blöcken kombiniert werden. Wenige ältere Versionen verwenden `STRICTTEXT` anstelle von `SRTX`.
Usage: `SRTX!dies ist ein beispiel`

#### INP (input)
Platzhalter für ein einzelnes Wort. Argumente sind optional - wenn gegeben beschränken sie die möglichen Eingaben.
Usage: `INP*varname!`
or: `INP*varname!montag,dienstag,mittwoch,donnerstag,freitag`

#### INP2 (input)
Platzhalter für ein mehrere Wörter. Argumente sind optional - wenn gegeben beschränken sie die möglichen Eingaben. Dieser Block muss der Letzte der Inputblöcke sein.
Usage: `INP2*varname!`
or: `INP2*varname!erster möglicher satz,ebenfalls möglich`

#### TEXT (output)
Gibt den als Argument gegebenen Text zurück. Wenn man Ausrufezeichen oder Doppelpunkte benutzen will, muss man diese durch `&arz;` und `&dpp;` ersetzen.
Usage: `TEXT!Dies ist eine Antwort`

#### VAR (output)
Gibt den Wert einer Variable zurück. In manchen Fällen kann dieser Block auch auf Variablen der Plugins zugreifen. Meistens kann man damit auf Variablen, die mit dem `INP/INP2` Block definiert wurden über `inp.varname` zugreifen. Andere übliche Variablen sind `global.username`, `global.date` and `global.time`.
Usage: `VAR!typ.varname`

#### EVAL (output)
Über diesen Block kann man auf output-plugins zugreifen. Man kann Variablen, die mit dem `INP/INP2` Block definiert wurden, übergeben. 
Usage: `EVAL!plugin.funktion(*varname1, *varname2, ...)`

### Plugins
Plugins ermöglichen es, Droit ohne großen Aufwand um bestimmte Funktionen zu erweitern.  
Details zur Programmierung von Plugins für python-droit findet man hier.  
**Ordnerstruktur:**  
``` no-highlight
plugins  
....... input  
....... ....... example  
....... ....... ....... main.py  
....... ....... ....... main.php
....... output  
....... ....... example  
....... ....... ....... main.py  
....... ....... ....... main.php 
```

#### Eingabe Plugins
Input-plugins befinden sich in einem namensgebenden Unterordner von `plugins/input`. Dieser Ordnername gibt den Namen des mit dem Plugin erschaffenen Blocks an.
Usage: `EXAMPLE!dies ist ein argument`


#### Ausgabe Plugins
Augabe Plugins werden über den EVAL Block aufgerufen (siehe oben).


## Beispiel
``` no-highlight
TEXT!wie:TEXT!geht:TEXT!es:TEXT!dir->TEXT!Mit geht es gut
SRTX!wie geht es dir->TEXT!Mir geht es gut
TEXT!Ich:TEXT!bin:INP*name!->TEXT!Hallo :VAR!inp.name
TEXT!berechne :INP2*term!->VAR!term:TEXT! = :EVAL!math.equal(*inp.term)
TEXT!ich:TEXT!mag,liebe:TEXT!dich:NOTX!nicht->TEXT!Ich mag dich auch
```
