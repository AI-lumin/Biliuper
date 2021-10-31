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
import dojson
import upload
import reprint
import remove
import traceback

print = reprint.print


def run_upload(vup):
    print(f'上传{vup}录播')
    upload.main(vup)

def run_remove(vup):
    print(f'转存{vup}录播')
    remove.main(vup)

def get_size(filePath, size=0):
    for root, dirs, files in os.walk(filePath):
        for f in files:
            size += os.path.getsize(os.path.join(root, f))
            # print(f)
    return size

def size_judge(path,vup_name,pause_time):
        is_euqal = False
        folder_list = glob.glob(os.path.join(path, '*'+vup_name+'*'))
        # print(folder_list)
        size_1 = 0
        for folder in folder_list:
            size_1 += get_size(folder)
        print('{}文件大小1:{}'.format(vup_name,size_1))
        time.sleep(pause_time)
        size_2 = 0
        for folder in folder_list:
            size_2 += get_size(folder)
        print('{}文件大小2:{}'.format(vup_name,size_2))
        if size_1 == size_2:
            is_euqal = True
        return is_euqal

def main(vup_name):
    '''对录制文件进行监控,根据大小比较'''
    pause_time = dojson.get_set()['pause_time'] #这里建议设置为5s以上，10s
    test_time = dojson.get_set()['test_time'] #延时，可以长一些，300s
    path = dojson.get_set()['video_path']
    do_upload = dojson.get_uploader(vup_name)['do_upload']
    do_remove = dojson.get_uploader(vup_name)['do_remove']
    while True:
        now_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        print(vup_name+' '+now_time)
        is_euqal = size_judge(path,vup_name,pause_time)
        # print(is_euqal)
        print(f'{vup_name}开始进行是否录制判断')
        while not is_euqal:
            print('{}正在录制'.format(vup_name))
            is_euqal = size_judge(path,vup_name,pause_time)
            # print(is_euqal)
            print(f'{vup_name}进行录制结束判断')
            if is_euqal:
                print('{}录制结束，暂停测试{}秒'.format(vup_name,test_time))
                time.sleep(test_time)
                is_euqal = size_judge(path,vup_name,pause_time)
                # print(is_euqal)
                print(f'{vup_name}开始进行是否上传判断')
                if is_euqal and do_upload is True:
                    print(f'{vup_name}启动上传')
                    try:
                        run_upload(vup_name)
                    except Exception as e:
                        print(traceback.format_exc())  
                        traceback.print_exc(file=open('./日志/错误日志.log','a',encoding='utf-8'))
                    print(f'{vup_name}上传结束')
                elif is_euqal and do_upload is not True:
                    print(f'{vup_name}录制中，不启动上传')
                else:
                    print(f'{vup_name}未开启上传选项,不启动上传')
                print(f'{vup_name}开始进行是否转存判断')
                if do_remove:
                    print(f'{vup_name}启动转存')
                    try:
                        run_remove(vup_name)
                    except Exception as e:
                        print(traceback.format_exc())  
                        traceback.print_exc(file=open('./日志/错误日志.log','a',encoding='utf-8'))
                else:
                    print(f'{vup_name}未开启转存选项,不启动转存')
            else:
                print(f'{vup_name}录制中，尚未结束')
            # else:
            print(f'{vup_name}尚未进行录制')



if __name__ == '__main__':
    main(vup_name)
