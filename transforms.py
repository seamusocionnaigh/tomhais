from numpy import nan
import pandas as pd
import re

def derivePageName(pageUrl):
    """Attempts to give a simple label to the page being viewed i.e. Home, Setup, Account"""
    if (pageUrl.find("/lightning/page/pardot")>-1):
        return "Pardot"
    elif (pageUrl.find("/lightning/page/chatter")>-1):
        return "Chatter"
    elif (pageUrl.find("/lightning/page/home")>-1):
        return "Home"
    elif (pageUrl.find("/lightning/settings")>-1):
        return "Personal Settings"
    elif (pageUrl.find("/lightning/setup")>-1):
        return "Setup"
    elif (pageUrl.find("/one/one.app")>-1):
        return "No App"
    elif (pageUrl.find("/lightning/cmp/")>-1):
        p = re.compile("(\/lightning\/cmp\/)((?:\w)+)_?")
        m = p.match(pageUrl)
        if (len(m.groups())==2):
            return m.group(2)
        else:
            return "Unknown Lightning Component"
    else:
        p = re.compile("(\/lightning\/[a-z]\/)((?:\w)+)_?")
        m = p.match(pageUrl)
        if (len(m.groups())==2):
            return m.group(2)
        else:
            return "Unknown Page"

def deriveSourceSObject(pageUrl):
    """Returns the name of the SObject which is the primary console tab i.e. after ?ws= URL param"""
    if(pageUrl.find("?ws=%2F")>-1):
        p = re.compile("(.*?)(\?ws=%2Flightning%2F[a-z]%2F)((?:\w)+)_?(%2F)(([a-z0-9]\w{4}0\w{12}|[a-z0-9]\w{4}0\w{9}))")
        m = p.match(pageUrl)
        if (len(m.groups())==6):
            return m.group(3)
        else:
            return "Unknown Object"
    else:
        return ""

def deriveSourceRecordId(pageUrl):
    """Returns the ID of the SObject which is the primary console tab i.e. after ?ws= URL param"""
    if(pageUrl.find("?ws=%2F")>-1):
        p = re.compile("(.*?)(\?ws=%2Flightning%2F[a-z]%2F)((?:\w)+)_?(%2F)(([a-z0-9]\w{4}0\w{12}|[a-z0-9]\w{4}0\w{9}))")
        m = p.match(pageUrl)
        if (len(m.groups())==6):
            return m.group(5)
        else:
            return ""
    else:
        return ""

#What columns / data points do we need?
columns = ["COMPONENT_NAME", "DEVICE_SESSION_ID", "GRANDPARENT_UI_ELEMENT","PAGE_APP_NAME","PAGE_CONTEXT","PAGE_ENTITY_ID","PAGE_ENTITY_TYPE","PAGE_START_TIME","PAGE_URL","PARENT_UI_ELEMENT","RECORD_ID","RECORD_TYPE","RELATED_LIST","REQUEST_ID","SESSION_KEY","TARGET_UI_ELEMENT","TIMESTAMP","TIMESTAMP_DERIVED","UI_EVENT_SEQUENCE_NUM","UI_EVENT_SOURCE","UI_EVENT_TIMESTAMP","UI_EVENT_TYPE","USER_ID_DERIVED","USER_TYPE"]

#what is our primary index
index=['USER_ID_DERIVED','SESSION_KEY']

#Load Lightning Interaction Logs
liLog = pd.read_csv("LightningINteraction.csv",usecols=columns,index_col=index,parse_dates=["TIMESTAMP_DERIVED"])
#sort by ui timestamp
liLog = liLog.sort_values(by=['UI_EVENT_TIMESTAMP'],ascending=True)
#drop those pesky NaN rows
liLog = liLog.dropna(subset=['PAGE_URL'])
#Only interested in user clicks for now
liLog = liLog[(liLog.UI_EVENT_SOURCE == "click") & (liLog.UI_EVENT_TYPE=="user")]
#print(liLog['PAGE_URL'].head(50))
liLog["PAGE_NAME"] = liLog['PAGE_URL'].apply(derivePageName)
liLog["SOURCE_SOBJECT"] = liLog['PAGE_URL'].apply(deriveSourceSObject)
liLog["SOURCE_RECORD_ID"] = liLog['PAGE_URL'].apply(deriveSourceRecordId)
liLog['UI_EVENT_TIMESTAMP_DERIVED'] = pd.to_datetime(liLog['UI_EVENT_TIMESTAMP'], unit='ms', utc=True)
liLog['TARGET_URL'] = liLog['PAGE_URL'].shift(-1)
print(liLog.TARGET_URL.head(20))
print(liLog.PAGE_URL.head(20))
#print(liLog.head(20))