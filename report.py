# -*- coding: utf8 -*-

class Table():
        
        def __init__(self):
                self.tablename=""
                self.header=[]
                self.dataset=[]
                self.statdata=[]
                self.graph_nb=0
        
        def xmlreader(self, filename, element, sous_elements, string= False):
                import xml.etree.ElementTree as ET
                root = ET.parse(filename).getroot()
                self.header=sous_elements
                self.dataset=[]
                for column in range(0,len(self.header)):
                        self.dataset.append([])
                        for row in root.findall(element):
                                if (string==True):
                                        self.dataset[column].append(str(row.findtext(self.header[column])))
                                else:
                                        self.dataset[column].append(float(row.findtext(self.header[column])))

        def csvreader(self,filename):
                import csv
                import numpy as np
                self.dataset=[]
                temp=[]
                with open(filename, 'r') as f:
                        for row in csv.reader(f, delimiter=";"):
                                self.dataset.append(row)
                        self.header=self.dataset.pop(0)
                        self.dataset=np.transpose(self.dataset)
                        for row in range(0,len(self.dataset)):
                                temp.append([])
                                for item in self.dataset[row]:
                                        temp[row].append(item)#float(item.replace(",",".")))
                        self.dataset=temp


        def csvwriter(self,filename):
                import csv
                with open(filename+".csv", "w") as f:
                        cw = csv.writer(f ,delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        cw.writerow(self.header)
                        temp=[]
                        for row in range(0,len(self.dataset)):
                                temp.append([])
                                for item in self.dataset[row]:
                                        temp[row].append(str(item).replace(".",","))
                        for row in zip(*temp):
                                cw.writerow(row)

#	    def converter(self):
#		    for i in self.dataset:
#			    for j in i:
#				    self.dataset[i][j]=round(self.dataset[i][j],4)

        def graphique(self,setx,sety):
                import matplotlib.pyplot as plt
                #dic={"title":,"xlabel":,"ylabel":,"axisrange":}
                plt.plot(self.dataset[self.header.index(setx)],self.dataset[self.header.index(sety)])
                plt.title(setx+"= f("+sety+")")
                plt.xlabel(setx)
                plt.ylabel(sety)
                xmin=float(min(self.dataset[self.header.index(setx)]))
                xmax=float(max(self.dataset[self.header.index(setx)]))
                ymin=float(min(self.dataset[self.header.index(sety)]))
                ymax=float(max(self.dataset[self.header.index(sety)]))
                plt.axis([xmin-(xmax-xmin)*0.8, xmax+(xmax-xmin)*0.8,ymin-(ymax-ymin)*0.8,ymax+(ymax-ymin)*0.8])
                plt.savefig(self.filename+str(self.graph_nb)+".png")
                self.graph_nb=self.graph_nb+1

        def statistique(self,data,coeff):
                import numpy as np
                import matplotlib.pyplot as plt
                import matplotlib.mlab as mlb
                import math
                mean=np.mean(self.dataset[self.header.index(data)])
                variance=np.var(self.dataset[self.header.index(data)],ddof=1)
                x = np.linspace(mean-coeff*variance,mean+coeff*variance,100)
                plt.plot(x,mlb.normpdf(x,mean,math.sqrt(variance)))
                plt.xlabel("Mean ="+str(round(mean,4))+"    Ecart-type ="+str(round(math.sqrt(variance),4)))
                plt.savefig(self.filename+str(self.graph_nb)+".png")
                self.graph_nb=self.graph_nb+1
                print("Mean ="+str(round(mean,4))+" Variance ="+str(round(math.sqrt(variance),4)))
                self.statdata={"mean":str(round(mean,4)), "ecart_type":str(round(math.sqrt(variance),4)), "interval_95%":[str(round(mean-1.96*math.sqrt(variance),4)),str(round(mean+1.96*math.sqrt(variance),4))], "interval_68,2%":[str(round(mean-math.sqrt(variance),4)),str(round(mean+math.sqrt(variance),4))]}
				

				


class Latex(object):

    
    def __init__(self,filename):
        import time
        self.filename=filename
        self.text=["\documentclass[a4paper,9pt,titlepage,oneside]{article}"]
        self.text.append(r"\usepackage{ucs}")
        self.text.append(r"\usepackage{wrapfig}")
        self.text.append(r"\usepackage{fancyhdr}")
        self.text.append(r"\usepackage[utf8]{inputenc}")
        self.text.append(r"\usepackage{fontenc}")
        self.text.append(r"\usepackage{soul}")
        self.text.append(r"\usepackage{ulem}")
        self.text.append(r"\usepackage{amsmath}")
        self.text.append(r"\usepackage[french]{babel}")
        self.text.append(r"\usepackage{eurosym}")
        self.text.append(r"\usepackage{float}")
        self.text.append(r"\usepackage[T1]{fontenc}")
        self.text.append(r"\usepackage{lmodern}")
        self.text.append(r"\usepackage[dvips]{graphicx}")
        self.text.append(r"\usepackage{amssymb}")
        self.text.append(r"\usepackage{mathrsfs}")
        self.text.append(r"\usepackage{color}")
#        self.text.append(r"\usepackage{wrapfig}")
#        self.text.append(r"\usepackage{wrapfig}")
#        self.text.append(r"\usepackage{wrapfig}")
#        self.text.append(r"\usepackage{wrapfig}")
#        self.text.append(r"\usepackage{wrapfig}")
        self.text.append(r"\author{Benoit}")
        self.text.append(r"\title{"+filename+"}")
        self.text.append("\date{"+time.strftime("%Y")+"}")
        self.text.append("\pagestyle{fancy}")
        self.text.append(r"\renewcommand{\headrulewidth}{1pt}")
        self.text.append(r"\fancyhead[C]{}")
        self.text.append(r"\fancyhead[L]{}")
        self.text.append(r"\fancyhead[R]{}")
        self.text.append(r"\renewcommand{\footrulewidth}{1pt}")
        self.text.append(r"\fancyfoot[C]{} ")
        self.text.append(r"\fancyfoot[L]{}")
        self.text.append(r"\fancyfoot[R]{\thepage}")
        self.text.append(r"\begin{document}")



### 1) Begining

    def fpage(self,titre1,titre2,titre3):
        self.text.append(r"\begin{titlepage}")
        self.text.append(r"\begin{center}")
        self.text.append(r"\includegraphics[scale=0.5]{./logo.png}")
        self.jline("2")
        self.maj(self.LARGE(titre1))
        self.jline("2")
        self.maj(self.Large(titre2))
        self.jline("2")
        self.text.append(r"\hrulefill{}")
        self.jline("2")
        self.maj(self.Huge(titre3))
        self.jline("2")
        self.text.append(r"\hrulefill{}")
        self.jline("3")
        self.large(r"{\today}")
        self.text.append(r"\end{center}")
        self.text.append(r"\end{titlepage}")

    def content_table(self):        
        self.text.append(r"\tableofcontents")

    def figure_table(self):
        self.text.append("\listoffigures")

    def list_table(self):
        self.text.append("\listoftables")


### 2) Tree
        
    def part(self, include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+1
        self.text.insert(-include,"\part{")
        self.text.append("}")
        return include


    def sect(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+1
        self.text.insert(-include,"\section{")
        self.text.append("}")
        return include

    def subsect(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+1
        self.text.insert(-include,"\subsection{")
        self.text.append("}")
        return include
    
    def w(self,include):
        self.text.append(include)

    def p(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+1
        self.text.insert(-include,"\paragraph{")
        self.text.append("}")
        return include

### 3) Inclusion

    def finclude(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+1
        self.text.insert(-include,"\include{")
        self.text.append("}")
        return include
    
### 4) Position

    def right(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+2
        self.text.insert(-include,r"\begin{flushright}")
        self.text.append(r"\end{flushright}")
        return include


    def center(self):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+2
        self.text.insert(-include,r"\begin{center}")
        self.text.append(r"\end{center}")
        return include


    def left(self):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+2
        self.text.insert(-include,r"\begin{flushleft}")
        self.text.append(r"\end{flushleft}")
        return include

### 5) Jump

    def jline(self, size):
        self.text.append(r"\\["+str(size)+"cm]")
        
    def jpage(self):
        self.text.append("\clearpage")

### 6) Liste

    def enumerate(self,table):
        self.text.append(r"\begin{enumerate}")
        for item in table:
            self.text.append("\item "+ item)
        self.text.append("\end{enumerate}")

    def itemize(self,table):
        self.text.append(r"\begin{itemize}")
        for item in table:
            self.text.append("\item "+ item)
        self.text.append("\end{itemize}")

### 7) Police
       
    def bolt(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+2
        self.text.insert(-include,r"\bfseries{")
        self.text.append(r"}")
        return include

    def it(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+2
        self.text.insert(-include,r"\textit{")
        self.text.append(r"}")
        return include


    def exp(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+2
        self.text.insert(-include,r"\textsuperscript{")
        self.text.append(r"}")
        return include
    
    def maj(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+2
        self.text.insert(-include,r"\textsc{")
        self.text.append(r"}")
        return include


    def box(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+2
        self.text.insert(-include,r"\fbox{")
        self.text.append(r"}")
        return include

    def ul(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+2
        self.text.insert(-include,r"\ul{")
        self.text.append(r"}")
        return include

    def st(self):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+2
        self.text.insert(-include,r"\st{")
        self.text.append(r"}")
        return include


            
    def color(self,coloration,include):
            #black, white, red, green, blue, yellow, magenta, cyan
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+2
        self.text.insert(-include,r"\textcolor{"+coloration+"}{")
        self.text.append(r"}")
        return include

    def tiny(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+2
        self.text.insert(-include,r"\tiny{")
        self.text.append("}")
        return include

    def scriptsize(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+2
        self.text.insert(-include,r"\scriptsize{")
        self.text.append("}")
        return include

    def footnotesize(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+2
        self.text.insert(-include,r"\footnotesize{")
        self.text.append("}")
        return include

    def small(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+2
        self.text.insert(-include,r"\small{")
        self.text.append("}")
        return include

    def normalsize(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+2
        self.text.insert(-include,r"\normalsize{")
        self.text.append("}")
        return include

    def large(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+2
        self.text.insert(-include,r"\large{")
        self.text.append("}")
        return include

    def Large(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+2
        self.text.insert(-include,r"\Large{")
        self.text.append("}")
        return include

    def LARGE(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+2
        self.text.insert(-include,r"\Large{")
        self.text.append("}")
        return include

    def huge(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+2
        self.text.insert(-include,r"\huge{")
        self.text.append("}")
        return include

    def Huge(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+2
        self.text.insert(-include,r"\Huge{")
        self.text.append("}")
        return include

### 8) Reference

    def quot(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+1
        self.text.insert(-include,r"\begin{quote}")
        self.text.append(r"\end{quote}")
        return include
                         
    def quota(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+1
        self.text.insert(-include,r"\begin{quotation}")
        self.text.append(r"\end{quotation}")
        return include
    
    def url(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+1
        self.text.insert(-include,r"\\url{")
        self.text.append("}")
        return include

    def ftnote(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+1
        self.text.insert(-include,r"\footnote{")
        self.text.append("}")
        return include

    def label(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+1
        self.text.insert(-include,r"\label{")
        self.text.append("}")
        return include

    def index(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+1
        self.text.insert(-include,"r\ref{")
        self.text.append("}")
        return include

    def pageref(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+1
        self.text.insert(-include,"r\pageref{")
        self.text.append("}")
        return include


### 9) Figure

    def figure(self,file,scale,caption):
        self.text.append(r"\begin{figure}[H]")
        self.text.append(r"\begin{center}")
        self.text.append(r"\includegraphics[scale="+scale+r"]{./"+file+"}")
        self.text.append("\caption{"+caption+"}")
        self.text.append("\end{center}")
        self.text.append("\end{figure}")

    def reflection(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+1
        self.text.insert(-include,"r\\reflectbox{%")
        self.text.append("}")
        return include



### 10) Tableau

    def tabular(self,table,header,caption=""):
        import numpy as np
        transpose=np.transpose(table)
        temp="|"
        for column in table:
            temp=temp+"c|"

        self.text.append(r"\begin{figure}[H]")
        self.text.append(r"\begin{center}")
        self.text.append(r"\begin{tabular}{"+temp+"}")
        self.text.append("\hline")
        temp=""
        for item in header:
            temp=temp+" & "+str(item).replace("_"," ")
        self.text.append(temp[3:] +r"\\")
        self.text.append("\hline")
        for row in transpose:
            temp=""            
            for item in row:
                temp=temp+" & "+str(item)
            self.text.append(temp[3:] +r"\\")
            self.text.append("\hline")
        self.text.append("\end{tabular}")
        self.text.append("\caption{"+caption+"}")
        self.text.append("\end{center}")
        self.text.append("\end{figure}")

        
### 11) Maths

    def eq(self,include):
        if (isinstance(include,str)):
            self.text.append(include)
            include=1
        else:
            include=include+1
        self.text.insert(-include,"$")
        self.text.append("$")
        return include

    def array(self,liste):
            self.text=[]
            self.text.append(r"\begin{array}{r}")
            for item in liste:
                         self.text.append(item+r"\\")     
            self.text.append("\end{array}")
            self.text.append("\right")
        
    def fract(self,num,den):
            return "\cfract{"+str(num)+"}{"+str(den)+"}"
    def sqrt(self,degree,nb):
            return "\sqrt["+str(degree)+"]{"+str(nb)+"}"
    def lim(self,nb1,nb2):
            return  "\lim_{"+str(nb1)+"\to"+str(nb2)+"}"
    def ex(self,nb):
            return "^{"+str(nb)+"}"
    def ind(self,nb):
            return "_{"+str(nb)+"}"
    def cos(self,include):
            return "\cos("+include+")"
    def sin(self,include):
            return "\sin("+include+")"
    def tan(self,include):
            return "\tan("+include+")"
    def ln(self,include):
            return "\ln("+include+")"
    def exp(self,include):
            return "\exp("+include+")"
    def log(self,include):
            return "\log("+include+")"
    def min(self,include):
            return  "\min("+include+")"
    def max(self,include):
            return  "\max("+include+")"
    def integsimp(self,include):
            return "\int{"+include+"}"
    def integborn(self,include,b1,b2):
            return "\int_{"+str(b1)+"}^{"+str(b2)+"}{"+include+"}"
    def mt_sum(self,include,b1,b2):
            return "\sum_{"+str(b1)+"}^{"+str(b2)+"}"+include
    def prod(self,include,b1,b2):
            return "\prod_{"+str(b1)+"}^{"+str(b2)+"}"+include
                         
    def matrix(self,table):
        import numpy as np
        transpose=np.transpose(table)
        temp="|"
        self.text.append(r"\begin{pmatrix}")
        for row in transpose:
            temp=""            
            for item in row:
                         if isinstance(item,float):
                                temp=temp+" & "+str(round(item,4))
                         else:
                                temp=temp+" & "+str(item)
                         
            self.text.append(temp[3:] +r"\\")
            self.text.append("\end{pmatrix}")

    def dot(self,letter):
        return "\dot{"+letter+"}"
    def acute(self,letter):
        return r"\acute{"+letter+"}"
    def vec(self,letter):
        return r"\vec{"+letter+"}"
    def ddot(self,letter):
        return "\ddot{"+letter+"}"
    def underbrace(self,include,name):
        return r"\underbrace{"+include+"}_{"+name+"}"
    def overbrace(self,include,name):
        return "\overbrace{"+include+"}^{"+name+"}"


### 12) Générator

    def convertor(self,number):
        return str(round(number,4))

    def generate(self):
        self.text.append("\end{document}")

##filter

        for i in range(0,3):
                for element in self.text:
                        if element=="}":
                                tmp=self.text.index(element)
                                self.text[tmp-1]=self.text[tmp-1]+"}"
                                self.text.pop(tmp)

                        if "{" == element[-1]:
                                tmp=self.text.index(element)
                                self.text[tmp]=self.text[tmp]+self.text[tmp+1]
                                self.text.pop(tmp+1)
                        if "€" in element:
                                self.text[self.text.index(element)]=element.replace("€",r"\euro{}")

                
        filename=self.filename
        import subprocess as sp
        with open(filename+".tex",'w') as f:
            for element in self.text:
                print(element)
                f.write(element+"\n")
        print(sp.call(["pdflatex", filename]))

### 13) Symbols & Letter

    def hat(self,letter):
        return r'\^{'+letter+'}'

    alpha=r'\alpha'
    beta=r'\beta'
    gamma=r'\gamma'
    delta=r'\delta'
    epsilon=r'\epsilon'
    zeta=r'\zeta'
    eta=r'\eta'
    theta=r'\theta'
    iota=r'\iota'
    kappa=r'\kappa'
    Lambda=r'\lambda'
    mu=r'\mu'
    nu=r'\nu'
    xi=r'\xi'
    pi=r'\pi'
    rho=r'\rho'
    sigma=r'\sigma'
    tau=r'\tau'
    upsilon=r'\upsilon'
    phi=r'\phi'
    chi=r'\chi'
    psi=r'\psi'
    omega=r'\omega'
    Lambda=r'\Lambda'
    Theta=r'\Theta'
    Gamma=r'\Gamma'
    Delta=r'\Delta'
    Xi=r'\Xi'
    Pi=r'\Pi'
    Sigma=r'\Sigma'
    Upsilon=r'\Upsilon'
    Phi=r'\Phi'
    Psi=r'\Psi'
    Omega=r'\Omega'
    neq=r"\neq"



