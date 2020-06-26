# console.py - io - printing to console
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)


def output(text):
	print(text)

def binaryQuestion(question):
	answer = ""
	while(answer != "Y" and answer != "n"):
		answer = getinput(question + " [Y/n]: ")
	return (answer == "Y")

def getinput(question):
	inp = input(question)
	return inp
