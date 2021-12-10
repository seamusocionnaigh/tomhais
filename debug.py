from numpy import nan
import pandas as pd
import re

#pageUrl="/lightning/r/Opportunity/0060900000G3cv0AAB/view?ws=%2Flightning%2Fr%2FAccount%2F0010900000wMykyAAC%2Fview"
pageUrl="%2Flightning%2Fr%2FAccount%2F0010900000wMykyAAC%2Fview"
#print(pageUrl.find("?ws=%2F"))
if(pageUrl.find("%2Flightning%2Fr%2F")>-1):
    p = re.compile("Account")
    m = p.match(pageUrl)
    print(len(m.groups()))
    print(m.group(1))
    print(m.group(2))
