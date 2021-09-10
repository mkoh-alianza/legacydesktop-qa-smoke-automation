class TextComparer:
    def compareOutputToFile(expected, output):
        expText = open(expected, 'r')
        expText = expText.read()
        print("Expected: " + expText)
        print("Recognized: " + output)
        expText = expText.split(' ')
        output = output.split(' ')
        issueCount = 0
        offset = 0
        print("") 
        print(" -- Beginning status report -- ")
        for x in range(len(expText)):
            if(len(output) > x + offset):
                if(output[x + offset] != expText[x]):
                    issueCount = issueCount + 1
                    
                    if(len(output) > x + offset + 1 and output[x + offset + 1] == expText[x]):
                        print("Extra word '" + output[x + offset] +"' was found")
                        offset = offset + 1
                    elif(len(expText) > x + 1 and output[x + offset] == expText[x + 1]):
                        print("The word '" + expText[x] + "' was missing")
                        offset = offset - 1
                    else:
                        print("Was expecting '" + expText[x] + "' but found '" + output[x + offset] + "' instead")
            elif(len(expText) > x + offset):
                issueCount = issueCount + 1
                print("Missing the word " + expText[x + offset])
        
        print(str(issueCount) + " issues were found in total")
        print("  -- End of status report --  ")