import abac_parser as p
import rule
import request_interpreter as interpret

abacFile = input("Please enter the file with policy information: ")
attributes, rules = p.parse("university.abac")
reqFile = input("Please enter the file with requests: ")
interpret.request_review("university-requests.txt", attributes, rules)
