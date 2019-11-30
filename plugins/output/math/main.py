import math

def equal(inp, rpack):
	inp = inp.replace("mal", "*").replace("durch", "/").replace("minus", "-").replace("plus", "+").replace("hoch", "**").replace("pi", str(math.pi)).replace("sqrt", "math.sqrt").replace("wurzel", "math.sqrt")
	inp = inp.replace("^", "**").replace(":", "/").replace("²", "**2").replace("³", "**3").replace(" ", "")
	try:
		return str(eval(inp))
	except:
		print("Die Berechnung konnte nicht abgeschlossen werden")



info = "Dieses Plugins kann einfache Berechnungen durchführen"
