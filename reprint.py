import os
import datetime
import time
# import codecs #这个是将windows格式改为unix格式用的

rewrite_print = print       
def print(*arg):
    day_time = time.strftime('%Y年%m月%d日',time.localtime(time.time()))
    now_time = time.strftime('%H:%M:%S',time.localtime(time.time()))
    rewrite_print(*arg) 
    # rewrite_print(day_time+' '+now_time,*arg)  
    output_dir = ".\\日志\\"
    if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            # print('新建log文件夹')
    #    log_name = 'log.txt' # 日志文件名称
    log_name = datetime.datetime.now().strftime('%Y年%m月%d日日志.log')
    filename = os.path.join(output_dir, log_name)
    rewrite_print(day_time+' '+now_time,*arg,file=open(filename,"a",encoding='utf-8'))
#     rewrite_print(day_time+' '+now_time,*arg,file=codecs.open(filename,"a",encoding='utf-8')) # 写入文件
    # rewrite_print(day_time+' '+now_time,*arg,file=open(filename,"a")) # 写入文件,遇到ଘ之类的会报错

