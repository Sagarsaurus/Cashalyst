__author__ = 'kpahawa'
import Quandl
import numpy
from pandas import *
import csv


def init():
    authKey = "xhBMdCCxgJSnz7jDp-SM"
    DTMVX = Quandl.get("YAHOO/FUND_DTMVX", trim_start="1998-12-11", trim_end="2014-09-05", authtoken=authKey, collapse="weekly")
    PRDSX = Quandl.get("YAHOO/FUND_PRDSX", trim_start="1997-06-30", trim_end="2014-09-05", authtoken=authKey, collapse="weekly")
    DFSVX = Quandl.get("YAHOO/FUND_DFSVX", trim_start="1993-02-26", trim_end="2014-09-05", authtoken=authKey, collapse="weekly")
    # print(DFSVX)
    # print(len(DFSVX))
    s = DataFrame(data = DFSVX, columns = ['Open','High','Low','Close','Volume','Adusted Close'])
    f = open("sample.csv","w",newline='')
    s.to_csv(f)
    f.close()

init()


