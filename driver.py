import abac_parser as p
import rule
import request_interpreter as interpret

abacFile = input("Please enter the file with policy information: ")
attributes, rules = p.parse(abacFile)
reqFile = input("Please enter the file with requests: ")
interpret.request_review(reqFile, attributes, rules)
