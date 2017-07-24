
import datetime as dt
import os
import re
import pandas as pd
from checking_functions import *
#from WindPy import w
from remotewind import w



if __name__=='__main__':
    nowtime = dt.datetime.now()
    today = nowtime.strftime('%Y%m%d')
    w.start()
    lasttrdday = w.tdaysoffset(-1,today).Times[0].strftime('%Y%m%d')
    timenow = nowtime.strftime('%H:%M:%S')

    curr_cwstate = {'BQ1ICLong' :r'\\BQ1_ICLONG\cwstate',
                    'BQ2ICLong' :r'\\BQ2_ICLONG\cwstate',
                    'BQ3ICLong' :r'\\BQ3_ICLONG\cwstate',
                    'JQ1ICLong' :r'\\JQ1_ICLONG\cwstate',
                    'HJ1ICLong' : r'\\HJ1_ICLONG\cwstate',
                    'LS1ICLong' :r'\\LS1_ICLONG\cwstate',
                    'GD2IClong' :r'\\GD2_ICLONG\cwstate',
                    'MS1IClong' :r'\\MS1_ICLONG\cwstate',

                    #'BQ1IFLong' :r'\\BQ1_IFLONG\cwstate',
                    #'BQ2IFLong' :r'\\BQ2_IFLONG\cwstate',
                    #'BQ3IFLong' :r'\\BQ3_IFLONG\cwstate',
                    'JQ1IFLong' :r'\\JQ1_IFLONG\cwstate',
                    #'HJ1IFLong' :r'\\HJ1_IFLONG\cwstate',
                    #'LS1IFLong' :r'\\LS1_IFLONG\cwstate',
                    #'GD2IFLong' :r'\\GD2_IFLONG\cwstate',

                    'BQ1ICHedge':r'\\BQ1_ICHEDGE\cwstate',
                    'BQ2ICHedge':r'\\BQ2_ICHEDGE\cwstate',
                    'BQ3ICHedge':r'\\BQ3_ICHEDGE\cwstate',
                    'LS1ICHedge':r'\\LS1_ICHEDGE\cwstate',
                    'GD2ICHedge':r'\\GD2_ICHEDGE\cwstate',

                    'GD2yyICHedge':r'\\GD2_yyICHEDGE\cwstate'
                    }

    report = pd.DataFrame()
    products = []
    for p in curr_cwstate:
        products.append(p)
        combined = {}
        cwdir = os.path.join(curr_cwstate[p],'cwstate.txt')
        lastcwdir = os.path.join(curr_cwstate[p],'cwstate_history',''.join(['cwstate_',lasttrdday,'.txt']))

        match_h = re.search('[A-Za-z]{2}Hedge',p,re.I)
        match_l = re.search('[A-Za-z]{2}Long',p,re.I)
        if match_h:
            ct = match_h.group()[0:2]
        elif match_l:
            ct = match_l.group()[0:2]
        else:
            print(p)
            raise('No ct detected')
        kpcmxdir = os.path.join(curr_cwstate[p],ct,''.join([p,'_KPCMX.txt']))    # 须确保合约类型在产品名后，产品名三个字母

        combined.update(check_positions_status(cwdir))
        combined.update(check_trading_status(cwdir,lastcwdir))
        #combined.update(check_kpcmx_status(kpcmxdir))
        #combined.update({'kpcmx_filetime': dt.datetime.fromtimestamp(os.path.getmtime(kpcmxdir)).strftime('%Y-%m-%d %H:%M:%S' )})
        result = pd.DataFrame(combined,index=[0])
        report = report.append(combined,ignore_index=True)

    report.index = products
    report['full_position'] = report['position_levels']==report['tot_levels']
    report['empty_position'] = report['position_levels']==0
    #report.to_csv(r'C:\Users\Jiapeng\Desktop\status.csv')
    print('**************** Products Status Check ********************')
    print(report)