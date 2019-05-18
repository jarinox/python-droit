# THE DROIT PROJECT
# This is the TEXT block ported to a plugin called EXAMPLE
#
# Copyright 2018-2019 Jakob Stolze


# Define the behavior of the block
rcountAdd = True        # add 1 to rcount?
rcountIs = False        # set rcount to a specific value?
rcountIsValue = 0       # value of rcount to set (if rcountIs == True)
ranking = False         # improve the ranking of this block?
var = False             # returns this block variables?
brk = False             # perform a break?


# Code your block here
def block(userinput, k, options):
	return [(userinput[k] in options.split(",")), ""]
