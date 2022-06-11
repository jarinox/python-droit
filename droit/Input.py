CHARACTERS = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIKLMNOPQRSTUVWXYZ0123456789ÄÖÜäöüß"

class Input:
    def __init__(self, string: str) -> None:
        self.rawInput = string
        
        self.processedInput = ""
        for c in self.rawInput:
            if c in CHARACTERS:
                self.processedInput += c
        
        while("  " in self.processedInput):
            self.processedInput = self.processedInput.replace("  ", " ")
        
        self.wordscs = self.processedInput.split(" ")
        self.words = self.processedInput.lower().split(" ")