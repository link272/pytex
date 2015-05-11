from report import Report

def it(self):
        self.text = r"\it{"+ self.text + "}"
    
def bolt(self):
        self.text = r"\textbf{"+ self.text + "}"

class TextZone(object):
    
    
    def __init__(self, text = []):
        self.textzone = text
        Report.instance.contents.append(self)
        
    def __repr__(self):
        return self.__class__.__name__
        
    def __add__(self, text):
        self.textzone.append(text)
        
    def builder(self, f):
        for text in self.textzone:
            f.write(text)
        f.write("\n")
        
class Text(object):
    
    
    def __init__(self, text = ""):
        self.text = text
        Report.instance.contents.append(self)
        
    def __repr__(self):
        return self.__class__.__name__
        
    def it(self):
        self.text = r"\it{"+ self.text + "}"
    
    def bolt(self):
        self.text = r"\textbf{"+ self.text + "}"
        
    def builder(self, f):
        f.write(self.text + "\n")