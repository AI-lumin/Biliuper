#!/usr/bin/env python3
# coding: utf-8

#可以使用，连续运行两次即可，注意确保备份完毕，这个脚本会直接删除文件，不是放入回收站！ 

import os
import time
import datetime
import logging
import dojson

set_time = dojson.read_set()[4] #n天前，单位：天
# print(set_time)
backup_path = dojson.read_set()[1]

def main(backup_path):
    class DeleteFile(object):
        def __init__(self,path):
            self.path = path

        def logger(self):
            """
            写入日志
            :return: logger对象
            """
            logger = logging.getLogger()  # 实例化了一个logger对象
            # 在国外叫handler，在中国翻译过来，叫句柄
            # 设置文件名和编码
            fh = logging.FileHandler('delete.log', encoding='utf-8')  # 实例化了一个文件句柄 # 格式和文件句柄或者屏幕句柄关联
            sh = logging.StreamHandler()  # 用于输出到控制台

            fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # 格式化
            fh.setFormatter(fmt)  # 格式和文件句柄或者屏幕句柄关联
            sh.setFormatter(fmt)

            # 吸星大法
            logger.addHandler(fh)  # 吸收写文件功能 和logger关联的只有句柄
            logger.addHandler(sh)  # 吸收输出屏幕功能
            logger.setLevel(logging.DEBUG)  # 设置警告级别为debug,此处DEBUG源码为DEBUG = 10

            # logger.debug('debug message')
            # logger.info('info message')
            # logger.warning('warning message')

            return logger

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
            offset = datetime.timedelta(days=-set_time)
            # 获取想要的日期的时间,即前n天时间
            re_date = (today + offset)
            # 时间转换为时间戳
            re_date_unix = time.mktime(re_date.timetuple())

            try:
                while file_list:  # 判断列表是否为空
                    path = file_list.pop()  # 删除列表最后一个元素，并返回给path l = ['E:\python_script\day26']
                    for item in os.listdir(path):  # 遍历列表,path = 'E:\python_script\day26'
                        path2 = os.path.join(path, item)  # 组合绝对路径 path2 = 'E:\python_script\day26\test'
                        if os.path.isfile(path2):  # 判断绝对路径是否为文件
                            # 比较时间戳,文件修改时间小于等于3天前
                            if os.path.getmtime(path2) <= re_date_unix:
                                os.remove(path2)
                                self.logger().debug('删除文件{}'.format(path2))  # 写入日志
                        else:
                            if not os.listdir(path2):  # 判断目录是否为空
                                # 若目录为空，则删除，并递归到上一级目录，如若也为空，则删除，依此类推
                                os.removedirs(path2)
                                self.logger().debug('删除空目录{}'.format(path2))  # 写入日志
                            else:
                                # 为文件夹时,添加到列表中。再次循环。l = ['E:\python_script\day26\test']
                                file_list.append(path2)

                return True
            except Exception as e:
                print(e)
                return False

    ret = DeleteFile(backup_path).delete()  # 当前目录，用的时候修改这里，推荐用绝对路径
    print(ret)

if __name__ == '__main__':
    main(delete_path)
