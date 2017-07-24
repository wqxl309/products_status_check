import os
import datetime as dt
import pandas as pd
from checking_functions import *


if __name__=='__main__':

    kpcmxlist = [
         'BQ1ICLong',
         'BQ2ICLong',
         'BQ3ICLong',
         'JQ1ICLong',
         'HJ1ICLong',
         'GD2ICLong',
         'LS1ICLong',
         'MS1ICLong',

         'BQ1IFLong',
         #'BQ2IFLong',
         'BQ3IFLong',
         'JQ1IFLong',
         'HJ1IFLong',
         #'GD2IFLong',
         'LS1IFLong',

        'BQ1ICHedge',
        'BQ2ICHedge',
        'BQ3ICHedge',
        'GD2ICHedge',
        'LS1ICHedge',

        'GD2yyICHedge'
    ]

    kpcmx_pool_path = r'E:\take_kpcmx\KPCMX_checking_pool'

    kpcmx_report = pd.DataFrame()
    for p in kpcmxlist:
        kpcmxdir = os.path.join(kpcmx_pool_path,'_'.join([p,'KPCMX.txt']))
        kpcmx = check_kpcmx_status(kpcmxdir)
        kpcmx.update({'kpcmx_filetime': dt.datetime.fromtimestamp(os.path.getmtime(kpcmxdir)).strftime('%Y-%m-%d %H:%M:%S' )})
        kpcmx_report = kpcmx_report.append(pd.DataFrame(kpcmx,index=[0]),ignore_index=True)
    kpcmx_report.index = kpcmxlist
    print(kpcmx_report)