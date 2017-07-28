
import datetime as dt
import os
import re
import pandas as pd
from checking_functions import *
from remotewind import w
import sys
sys.path.append(r'E:\take_kpcmx\products_base_info')
import products_base_info as pinfo

if __name__=='__main__':
    nowtime = dt.datetime.now()
    today = nowtime.strftime('%Y%m%d')
    w.start()
    lasttrdday = w.tdaysoffset(-1,today).Times[0].strftime('%Y%m%d')
    timenow = nowtime.strftime('%H:%M:%S')
    # generate report
    report = pd.DataFrame()
    products = []
    for p in pinfo.base_info.BASEINFO:
        combined = {}
        if p['monthtype']=='Back2':
            yy = 'yy'
        else:
            yy = ''
        tname = ''.join([p['product'],'_',yy,p['cttype'],p['strategy']])
        pname = tname.replace('_','')
        products.append(pname)
        cwfile = os.path.join(p['host'],tname,'cwstate')
        cwdir = os.path.join(cwfile,'cwstate.txt')
        lastcwdir = os.path.join(cwfile,'cwstate_history',''.join(['cwstate_',lasttrdday,'.txt']))
        combined.update(check_positions_status(cwdir))
        combined.update(check_trading_status(cwdir,lastcwdir))
        result = pd.DataFrame(combined,index=[0])
        report = report.append(combined,ignore_index=True)
    report.index = products
    report['full_position'] = report['position_levels']==report['tot_levels']
    report['empty_position'] = report['position_levels']==0
    #report.to_csv(r'C:\Users\Jiapeng\Desktop\status.csv')
    print('**************** Products Status Check ********************')
    print(report)