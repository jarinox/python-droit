# main.py - math plugin for python-droit
# Copyright 2019 Jakob Stolze
#
#
# This file is part of python-droit.
#
# python-droit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# python-droit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with python-droit.  If not, see <http://www.gnu.org/licenses/>.


import math

def equal(inp, rpack):
	inp = inp.replace("mal", "*").replace("durch", "/").replace("minus", "-").replace("plus", "+").replace("hoch", "**").replace("pi", str(math.pi)).replace("sqrt", "math.sqrt").replace("wurzel", "math.sqrt")
	inp = inp.replace("^", "**").replace(":", "/").replace("²", "**2").replace("³", "**3").replace(" ", "")
	try:
		return str(eval(inp))
	except:
		print("Die Berechnung konnte nicht abgeschlossen werden")



info = "Dieses Plugins kann einfache Berechnungen durchführen"
