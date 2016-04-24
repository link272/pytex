from report6 import *

R = Report()
print(Report.instance, Report.instance.contents)
with TitlePage() as tp:
    print(Report.instance, Report.instance.contents)
    Text("coucou")
    print(Report.instance, Report.instance.contents)
    Image("logo.png").caption("coucou2").fixed()
    print(Report.instance, Report.instance.contents)
print(Report.instance, Report.instance.contents)
with Section("Coucou, les lapins!!") as sec:
    print(Report.instance, Report.instance.contents)
    Text('hello')
    print(Report.instance, Report.instance.contents)
    Text("jule de chez smith d'en face").bolt()
    print(Report.instance, Report.instance.contents)
print(Report.instance, Report.instance.contents)
print(R.contents[0].contents)
R.generate()
