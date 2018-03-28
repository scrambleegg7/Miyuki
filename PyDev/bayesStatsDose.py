#coding: utf-8
from __future__ import division
from CacheDBClass import CacheDB
from bayesStatsDoseClass import bayesStatsDoseClass
import glob
import sys, traceback

def main():
    
    CacheDBObj = CacheDB('receipty')
    try:
        with CacheDBObj:
            #ret_code = dataRetrieveAndCalc(CacheDBObj)
            bayesStatsDoseObj = bayesStatsDoseClass(CacheDBObj)
            try:
                with bayesStatsDoseObj:
                    pass
            except:
                # エラーの情報をsysモジュールから取得
                info = sys.exc_info()
                # tracebackモジュールのformat_tbメソッドで特定の書式に変換
                tbinfo = traceback.format_tb( info[2] )
                # 収集した情報を読みやすいように整形して出力する----------------------------
                print 'Python Error.'.ljust( 80, '=' )
                for tbi in tbinfo:
                    print tbi
                print '  %s' % str( info[1] )
                print '\n'.rjust( 80, '=' )

    except:
        # エラーの情報をsysモジュールから取得
        info = sys.exc_info()
        # tracebackモジュールのformat_tbメソッドで特定の書式に変換
        tbinfo = traceback.format_tb( info[2] )
        # 収集した情報を読みやすいように整形して出力する----------------------------
        print 'Python Error.'.ljust( 80, '=' )
        for tbi in tbinfo:
            print tbi
        print '  %s' % str( info[1] )
        print '\n'.rjust( 80, '=' )
        
if __name__ == '__main__':
    main()