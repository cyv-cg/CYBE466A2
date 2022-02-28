def request_review(file, attributes, rules):
    f = open(file, "r")
    lines = f.readlines()
    f.close()
    
    results = []
    for r in lines:
        elements = r.strip().split(",")
        subject = attributes[elements[0]]
        resource = attributes[elements[1]]
        outcome = rules.ruleCheck(elements[2], subject.attributes, resource.attributes)
        results.append(outcome)
        print(r.strip(), ": RESULT: ", outcome)

    #not really needed as far as I can tell so I commented it out
    #return results