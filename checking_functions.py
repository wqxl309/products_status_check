
import numpy as np


def read_status(filedir,stattype = 'trade'):
    with open(filedir,'r') as statinfo:
        temp = statinfo.readlines()
        contents_temp = [row.strip().split(',') for row in temp]
        if stattype == 'trade':
            contents = [[float(c) for c in row] for row in contents_temp if len(row)==6]
        elif stattype == 'kpcmx':
            contents = [float(c) if not c[0:2].isalpha() else c for c in contents_temp[0]]
        else:
            raise Exception( 'No status type provided ! ')
        return contents

def check_positions_status(currentdir):
    cwstatus = read_status(currentdir,stattype = 'trade')
    cwstatus = np.array(cwstatus)
    size = cwstatus.shape
    poslevels = np.sum(cwstatus[:,0]==-1)
    return {'tot_levels':size[0] , 'position_levels':poslevels}

def check_trading_status(currentdir,lastdir):
    curr_cw = np.array( read_status(currentdir,stattype = 'trade') )
    last_cw = np.array( read_status(lastdir,stattype = 'trade') )
    statchg = curr_cw[:,0] - last_cw[:,0]
    inleves = np.sum(statchg < 0)
    outleves = np.sum(statchg > 0)
    #holdleves = np.sum(statchg == 0)
    return {'in_levels' : inleves, 'out_levels': outleves}   #, 'hold_levels':holdleves }

def check_kpcmx_status(kpcmxdir):
    kpcmx_stat = read_status(kpcmxdir,stattype = 'kpcmx')
    kpcmx_date = str(int(kpcmx_stat[2]))
    kpcmx_contract = kpcmx_stat[3]
    kpcmx_type = kpcmx_stat[-1].split('_')
    return {'kpcmx_date':kpcmx_date,'kpcmx_contract':kpcmx_contract,'kpcmx_month':kpcmx_type[0],
            'kpcmx_strategy':'_'.join(kpcmx_type[1:3]),'kpcmx_levels':'_'.join(kpcmx_type[3:])}


if __name__=='__main__':
    import os
    import datetime as dt
    import time
    pt = r'C:\Users\Jiapeng\Desktop\tempholdings\ls1_20170720.csv'
    print( dt.datetime.fromtimestamp(os.path.getmtime(pt)).strftime('%Y-%m-%d %H:%M:%S' ))
    print( dt.datetime.fromtimestamp(os.stat(pt).st_mtime ) )
    print( dt.datetime.fromtimestamp(os.stat(pt).st_ctime )) #获取文件修改时间
    print( dt.datetime.fromtimestamp(os.path.getctime(pt) ))#获取文件的创建时间