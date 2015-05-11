from contextlib import contextmanager
from report import Report
import copy

class Structure(object):
    

    package = None
    
    def __init__(self, cmd = None):
        self.contents = []
        Report.instance.contents.append(self)
        self.last_instance = None
        if cmd != None:
            self.cmd = cmd
        if self.package != None:
            Report.base_report.packages.update(self.package)
            
    def __repr__(self):
        return self.__class__.__name__
        
    def __enter__(self):
        self.last_instance = Report.instance
        Report.instance = self
        return self
        
    def __exit__(self, type, value, traceback):
        Report.instance = self.last_instance
        return True
        
    def builder(self,f):
        with self.latex(f):
            for C in self.contents:
                C.builder(f)

    @contextmanager    
    def latex(self, f):
        f.write(self.cmd[0] + "\n")
        yield
        if self.cmd[1] != "":
            f.write(self.cmd[1] + "\n")


class TitlePage(Structure):
    
    cmd = [r"\begin{titlepage}", "\end{titlepage}"]
        

class Part(Structure):
    
    def __init__(self, title = ""):
        super().__init__([r"\part{"+ title+ "}", ""])

class Section(Structure):
    
    def __init__(self, title = ""):
        super().__init__([r"\section{"+ title + "}", ""])

class SubSection(Structure):
    
    def __init__(self, title = ""):
        super().__init__([r"\subsection{"+ title+ "}", ""])


class SubSubSection(Structure):
    
    def __init__(self, title = ""):
        super().__init__([r"\subsubsection{"+ title+ "}", ""])


class Box(Structure):
    
    cmd = [r"\begin{fbox}", "\end{fbox}"]
    
class Center(Structure):
    
    cmd = [r"\begin{center}", "\end{center}"]
    
class Right(Structure):
    
    cmd = [r"\begin{flushright}", "\end{flushright}"]
    
class Center(Structure):
    
    cmd = [r"\begin{flushleft}", "\end{flushleft}"]
    

