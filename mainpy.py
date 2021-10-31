'''
1.根据uploader数量建立线程
2.定时执行删除
3.只能让monitor自己获取相应的path了
'''

import dojson
from threading import Thread
import time
import os
import monitor
import delete
import reprint

print = reprint.print

def run_monitor(vup_name):
    print(vup_name)
    # os.system('python ' + monitor_path + ' %s' % (vup_name))
    monitor.main(vup_name)

def delete_backup(delete_path,day):
    # os.system('python '+delete_path)
    delete.main(delete_path,day)

def make_timelist():
    time_list = []
    for i in range(24):
        time = '{:02d}:00:05'.format(i)
        time_list.append(time)
    return time_list

def main():
    time_list = make_timelist()
    json_path = ".\setting.json"
    log_path = '.\\日志\\'
    video_path = dojson.get_set()['video_path']
    backup_path=dojson.get_set()['backup_path']
    delete_time = dojson.get_set()['delete_time'] #单位：小时
    deletelog_time = dojson.get_set()['deletelog_time']
    vup_name_list = dojson.get_namelist()
    uploader_num = len(vup_name_list)
    if not os.path.isfile(json_path):
        dojson.set_initial()
    task_list = []
    for vup_name in vup_name_list:
        time.sleep(0.5)
        # task = Thread(target=run_monitor, args=(vup_name,)) #注意在结尾加个',',这么做内存会溢出
        # task = Process(target=run_monitor,args=(vup_name,),name = vup_name) #实例化进程对象
        task = Thread(target=run_monitor,args=(vup_name,),name = vup_name)
        task.start()
        # task.join(timeout=86400) #24h
        task_list.append(task)
    print(f'现有{len(task_list)}个房间')
    while True:
        time.sleep(1)
        now_time = time.strftime('%H:%M:%S',time.localtime(time.time()))
        # print(now_time)
        if now_time in time_list:
            delete_backup(backup_path,delete_time)
        if now_time == '00:00:05':
            delete_backup(log_path,deletelog_time)


if __name__ == '__main__':
        main()
