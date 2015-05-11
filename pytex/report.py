from contextlib import contextmanager
import subprocess

class Report(object):
    
    packages = dict()
    base_report = None 
    instance = None
    contents = []
    headers = []

    def __init__(self, name = "Report", language = "french"):
        self.name = name
        Report.instance = self
        Report.base_report = self
        self.packages.update({"inputenc":"utf8","babel": language ,"fontenc":"T1", "lmodern":""})

    def __call__(self):
        Report.base_report = self
        Report.instance = self

    def __repr__(self):
        return self.__class__.__name__

    def contentslist(self):
        self.headers.append("tableofcontents")
        
    def figureslist(self):
        self.headers.append("listoftables")
        
    def tableslist(self):
        self.headers.append("listoffigures")

    
    @contextmanager
    def _document(self, f):
        f.write(r"\begin{document}"+ u"\n")
        yield
        f.write(u"\end{document}")
        
    def generate(self, default_size = 11, paper_format = "a4paper"):
        with open(self.name+".tex", "w") as f:
            f.write(u"\documentclass{report}["+ str(default_size) + "pt," + paper_format + u"]\n")
            f.write(r"\include{package.tex}"+"\n")
            for h in self.headers:
                f.write(r"\\" + h + u"\n")
            
            with self._document(f):
                for S in self.contents:
                    S.builder(f)
                    
            with open("package.tex", "w") as fp:
                for key, value in self.packages.items():
                    if value == "":
                        fp.write(r"\usepackage{" + key + u"}\n")
                    else:
                        fp.write(r"\usepackage{" + key + u"}[" + value + u"]\n")
                        
                    
            build = 1 #subprocess.call(["pdflatex", 
                                    #self.name + "tex"])
            if build == 0:
                subprocess.call(["rm", 
                                self.name + ".tex", 
                                self.name + ".log", 
                                self.name + ".aux", 
                                "package.tex"])
                
            
