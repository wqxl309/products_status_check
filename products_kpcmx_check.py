import os
import datetime as dt
import pandas as pd
from checking_functions import *
import sys
sys.path.append(r'E:\take_kpcmx\products_base_info')
import products_base_info as pinfo


if __name__=='__main__':
    kpcmx_report = pd.DataFrame()
    for p in pinfo.base_info.BASEINFO:
        if p['monthtype']=='Back2':
            yy = 'yy'
        else:
            yy = ''
        tname = ''.join([p['product'],'_',yy,p['cttype'],p['strategy']])
        pname = tname.replace('_','')
        kpcmxdir = os.path.join(p['host'],tname,'kpcmx','kpcmx_update','_'.join([pname,'KPCMX.txt']))
        kpcmx = check_kpcmx_status(kpcmxdir)
        kpcmx.update({'kpcmx_filetime': dt.datetime.fromtimestamp(os.path.getmtime(kpcmxdir)).strftime('%Y-%m-%d %H:%M:%S' )})
        kpcmx_report = kpcmx_report.append(pd.DataFrame(kpcmx,index=[pname]),ignore_index=False)
    print(kpcmx_report)