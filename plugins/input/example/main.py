# main.py - example plugin for python-droit
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



# Define the behavior of the block
rcountAdd = True        # add 1 to rcount?
rcountIs = False        # set rcount to a specific value?
rcountIsValue = 0       # value of rcount to set (if rcountIs == True)
ranking = False         # improve the ranking of this block?
var = False             # returns this block variables?
brk = False             # perform a break?


# Code your block here
def block(userinput, k, options, rpack=None):
	return [(userinput[k] in options.split(",")), ""]
