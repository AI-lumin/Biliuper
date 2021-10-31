#!/usr/bin/env python3
# coding: utf-8

#可以使用，连续运行两次即可，注意确保备份完毕，这个脚本会直接删除文件，不是放入回收站！ 
# 获取的是修改时间

import os
import time
import datetime
import dojson
import reprint

print = reprint.print

# set_time = dojson.read_set()[4] #n天前，单位：天
backup_path = dojson.get_set()['backup_path']

def main(backup_path,hour):
    class DeleteFile(object):
        def __init__(self,path):
            self.path = path

        def delete(self):
            """
            删除文件
            :param path: 文件路径
            :return: bool
            """
            file_list = [self.path]  # 文件夹列表
            # 获取当前时间
            today = datetime.datetime.now()
            # 计算偏移量
            # offset = datetime.timedelta(days=-day,hours = -hour)
            offset = datetime.timedelta(hours = -hour)
            # 获取想要的日期的时间,即前n天时间
            re_date = (today + offset)
            # 时间转换为时间戳
            re_date_unix = time.mktime(re_date.timetuple())
            for i in range(2):
                '''进行两次以删除干净'''
                try:
                    while file_list:  # 判断列表是否为空
                        path = file_list.pop()  # 删除列表最后一个元素，并返回给path l 
                        for item in os.listdir(path):  # 遍历列表
                            # if item != '错误日志.txt':
                                path2 = os.path.join(path, item)  # 组合绝对路径 path2 
                                if os.path.isfile(path2):  # 判断绝对路径是否为文件
                                    # 比较时间戳
                                    if os.path.getmtime(path2) <= re_date_unix:
                                        os.remove(path2)
                                        print('删除文件{}'.format(path2))  # 写入日志
                                else:
                                    if not os.listdir(path2):  # 判断目录是否为空
                                        # 若目录为空，则删除，并递归到上一级目录，如若也为空，则删除，依此类推
                                        os.removedirs(path2)
                                        print('删除空目录{}'.format(path2))  # 写入日志
                                    else:
                                        # 为文件夹时,添加到列表中。再次循环。
                                        file_list.append(path2)
                    return True
                except Exception as e:
                    print(e)
                    return False

    ret = DeleteFile(backup_path).delete()  # 当前目录，用的时候修改这里，推荐用绝对路径
    print(ret)

if __name__ == '__main__':
    '''这里会执行两次以保证删除'''
    # delete_path = '.\\日志\\'
    main(backup_path,hour)
