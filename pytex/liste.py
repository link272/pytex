from structure import Structure
from report import Report

class List(Structure):
    
    cmd = [r"\begin{itemize}",u"\end{itemize}"]
    
    def __init__(self, data = None, number = True):
        Report.instance.contents.append(self)
        self.data = data
        if number == True:
            self.cmd = [r"\begin{enumerate}",u"\end{enumerate}"]

            
    def builder(self,f):
        f.write(self.cmd[0] + u"\n")
        if isinstance(self.data, dict):
            for key, value in self.data:
                f.write("\item["+ key + "] "+ value + "\n")
        else:
            for i in self.data:
                f.write("\item " + i + "\n")
        f.write(self.cmd[1] + "\n")
        