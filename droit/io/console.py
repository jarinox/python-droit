# console.py - io - printing to console
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jaybeejs/python-droit)


def output(text):
	print(text)

def binaryQuestion(question):
	answer = ""
	while(answer != "Y" && answer != "n"):
		answer = input(question + " [Y/n]: ")
	return (answer == "Y")

def input(question):
	inp = input(question)
	return inp
