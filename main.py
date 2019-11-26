from cnf2cyk import *
from cfg2cnf import *
from lexer import *
import sys
from os import path

if(len(sys.argv)>=2):
	filename = sys.argv[1]
	if(path.exists(filename)):
		compile_CYK(filename)
	else:
		print("File doesn't exist.")
else:
	print("Usage: python main.py <filename>.")