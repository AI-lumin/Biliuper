'''
1.根据uploader数量建立线程
2.定时执行删除
3.只能让monitor自己获取相应的path了
'''

import schedule
import dojson
from threading import Thread
# import threading
# from multiprocessing import  Process
import time
import os
import monitor
import delete
# import delete
# import monitor
# import upload
# import sys
# import logging


def run_monitor(vup_name):
    print(vup_name)
    # os.system('python ' + monitor_path + ' %s' % (vup_name))
    monitor.main(vup_name)

def detele_backup(delete_path):
    # os.system('python '+delete_path)
    delete.main(delete_path)

def main():
    log_path = '.\log.txt'
    json_path = ".\setting.json"
    vedio_path = dojson.read_set()[0]
    backup_path=dojson.read_set()[1]
    vup_name_list = dojson.get_namelist()
    uploader_num = len(vup_name_list)
    # sys.stdout = open(log_path, "w")
    if not os.path.isfile(json_path):
        dojson.set_initial()
    task_list = []
    for vup_name in vup_name_list:
        time.sleep(0.5)
        # task = Thread(target=run_monitor, args=(vup_name,)) #注意在结尾加个',',这么做内存会溢出
        # task = Process(target=run_monitor,args=(vup_name,),name = vup_name) #实例化进程对象
        task = Thread(target=run_monitor,args=(vup_name,),name = vup_name)
        # task = Thread(target=run_monitor(vup_name))
        task.start()
        # task.join(timeout=86400) #24h
        task_list.append(task)
    print(f'现有{len(task_list)}个房间')
    while True:
        time.sleep(1)
        now_time = time.strftime('%H:%M:%S',time.localtime(time.time()))
        # print(now_time)
        if now_time == '00:00:00' or now_time == '00:00:05':
            detele_backup(backup_path)
        # schedule.every().day.at("00:00").do(delete_path,) #定时删除，可以传参，注意前面要是个函数
        # schedule.every(12).hours.do(detele_backup) 
        


if __name__ == '__main__':
    # log_path = '.\log.txt'
    # json_path = ".\setting.json"
    # delete_path = '.\delete.py'
    # vedio_path = dojson.read_set()[0]
    # vup_name_list = dojson.get_namelist()
    # uploader_num = len(vup_name_list)
    # monitor_path = '.\monitor.py'
    # print(monitor_path)
    main()