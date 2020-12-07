import sys
import parser

code = open(sys.argv[1], "r")

parser.Parser.run(code.read())