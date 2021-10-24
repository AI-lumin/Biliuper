# -*- coding:UTF-8 -*-
# -*- create on 2021/10/16 by alex_lumin -*-
# 主要功能：监控目标文件夹增量变化停止并持续一段时间后执行相应脚本
'''
主要是希望：
1.一直运行
2.监控文件大小并进行比较
3.定时执行功能
4.调用执行脚本
'''

import os
import time
import glob
# import sys
import dojson
import upload



'''改成upload的位置'''
def runPy(vup):
    print('run ' + vup)
    upload.main(vup)
    # os.system(f"python {upload_path} {vup}")
    # os.system("python  /tandelindata/ETL_code/ftp_dowload_local.py")

def getSize(filePath, size=0):
    for root, dirs, files in os.walk(filePath):
        for f in files:
            size += os.path.getsize(os.path.join(root, f))
            # print(f)
    return size

def sizeJugde(path,vup_name,pause_time):
        is_euqal = False
        folder_list = glob.glob(os.path.join(path, '*'+vup_name+'*'))
        size_1 = 0
        for folder in folder_list:
            size_1 += getSize(folder)
        print('{}文件大小1:{}'.format(vup_name,size_1))
        time.sleep(pause_time)
        size_2 = 0
        for folder in folder_list:
            size_2 += getSize(folder)
        print('{}文件大小2:{}'.format(vup_name,size_2))
        if size_1 == size_2:
            is_euqal = True
        return is_euqal

def main(vup_name):
    pause_time = dojson.read_set()[2] #这里建议设置为5s以上，10s
    test_time = dojson.read_set()[3] #延时，可以长一些，300s
    path = dojson.read_set()[0]
    while True:
        now_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        print(vup_name+' '+now_time)
        is_euqal = sizeJugde(path,vup_name,pause_time)
        # print(is_euqal)
        print(f'{vup_name}开始进行是否录制判断')
        while not is_euqal:
            print('{}正在录制'.format(vup_name))
            is_euqal = sizeJugde(path,vup_name,pause_time)
            print(is_euqal)
            print(f'{vup_name}进行录制结束判断')
            if is_euqal:
                print('{}录制结束，暂停测试{}秒'.format(vup_name,test_time))
                time.sleep(test_time)
                is_euqal = sizeJugde(path,vup_name,pause_time)
                print(is_euqal)
                print(f'{vup_name}开始进行是否上传判断')
                if is_euqal:
                    print(f'{vup_name}启动上传')
                    runPy(vup_name)
                    # task = Thread(target=runPy, args=(vup_name,)) #注意在结尾加个','
                    # task.start()
                    print(f'{vup_name}上传结束')
                else:
                    print(f'{vup_name}录制中，不启动上传')
            else:
                print(f'{vup_name}录制中，尚未结束')
        # else:
        print(f'{vup_name}尚未进行录制')


if __name__ == '__main__':
    # path = dojson.read_set()[0]
    # upload_path = './/upload.py'
    # # vup_name = sys.argv[1]
    # pause_time = dojson.read_set()[2] #这里建议设置为5s以上，10s
    # test_time = dojson.read_set()[3] #延时，可以长一些，300s
    main(vup_name)
