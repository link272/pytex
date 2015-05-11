from structure import Structure
from report import Report
import numpy as np

class Figure(Structure):
    
    package = {"float":""}
    cmd = [r"\begin{figure}", u"\end{figure}"]
    
class BaseFigure(object):
    
    caption_text = None
    figure = None
    
    def __init__(self):
        with Figure() as F:
            F.contents.append(self)
            self.figure = F
        
    def caption(self, text = ""):
        self.caption_text = text
        return self
        
    def fixed(self):
        self.figure.cmd[0] += "[H]"
        return self

class Image(BaseFigure):
    
    def __init__(self, filename ="", ratio = 1):
        Report.base_report.packages.update({"graphicx":"dvips"})
        super().__init__()
        self.filename = filename
        self.ratio = ratio
    
    def __repr__(self):
        return self.__class__.__name__

    def builder(self, f):
        f.write("\includegraphics["+ str(self.ratio) +"]{"+ self.filename +"}\n")
        if self.caption_text != None:
            f.write("\caption{"+ self.caption_text +"}\n")
            

class Table(BaseFigure):
    
    def __init__(self, data = [], headers = None):
        super().__init__()
        self.data = data
        self.headers = headers
        if headers != None:
            if len(data) != len(headers):
                print("Wrong dimension :", self)
                self.headers = None
        
    def __repr__(self):
        return self.__class__.__name__
                
                
    def builder(self, f):
            tmp = "|"
            for c in range(0,len(self.data)):
                tmp += "c|"
            f.write(r"\begin{tabular}["+ tmp + "]"+"\n")
            
            if self.headers != None:
                tmp = ""
                for h in self.headers:
                    tmp += " & " + h
                f.write(tmp[3:] + r"\\" + "\n")
                
            self.data = np.transpose(self.data)
            for rows in self.data:
                tmp = ""
                for r in rows:
                    tmp += " & " + r
                f.write(tmp[3:] + r"\\" + "\n")
                
            f.write(r"\end{tabular}"+"\n")
            if self.caption_text != None:
                f.write("\caption{"+ self.caption_text +"}\n")
        