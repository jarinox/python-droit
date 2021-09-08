class inp:
    def __init__(self):
        self.tag = "TEXT"
    
    def placeholder(self, rule, pTexts):
        if(rule.tag == self.tag):
            if(pTexts == []):
                for child in rule.children:
                    pTexts.append(child + " ")
            else:
                pNew = []
                for i in range(0, len(pTexts)):
                    for child in rule.children:
                        pNew.append(pTexts[i] + child + " ")
                pTexts = pNew
        
        return pTexts
