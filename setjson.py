'''
1.可以对json文件进行方便的更改
2.想要查看的话建议直接打开json文件
'''

import dojson
import os
import traceback

json_path = ".//setting.json"

def noline_input():
    long_str = ''
    while True:
        str1 = input()
        if str1 != '0':
            long_str += str1+'\n'
        else:
            break
    return long_str

def bool_input():
    str2 = input()
    bool2 = True
    if str2 == '0' or str2 == 'false':
        bool2 = False
    return bool2

def add_uploader():
    # print(f'现在有{len(dojson.get_namelist())}个房间')
    num_str = input('请输入要加入的房间数(不超过20,默认为1):')
    if num_str.isdigit():
        num = int(num_str)     
    else:
        num = 1
    print(num)
    if num in range(1,21):
        uploader_list = []
        for i in range(num):
            uploader = {}
            # if input('vupname(自己设定的vup名称):') == None:
            #     print('1输入不能为空')
            # else:
            print('开始添加新的房间:')
            uploader['vupname'] = input('vupname(自己设定的vup名称):')
            uploader['username'] = input('username(账号):')
            uploader['password'] = input('password(密码):')
            uploader['title'] = input('title(标题,已默认设置好)')
            uploader['source'] = input('source(直播间网址):')
            # uploader['desc'] = input('desc(视频简介):')
            print('desc(视频简介,输入0以结束输入):')
            uploader['desc'] = noline_input()
            print('do_upload(是否上传,默认为true,输入0或false以改为false)')
            uploader['do_upload'] = bool_input()
            print('do_remove(是否转移,默认为true,输入0或false以改为false)')
            uploader['do_remove'] = bool_input()

            if input('upload_way(有1和2两种,默认为2,1现在暂时不可用):') != None:
                uploader['upload_way'] = 2
            else:
                uploader['upload_way'] = input('upload_way:')
            if input('copyright(默认为转载2):') != None:
                uploader['copyright'] = 2
            else:
                uploader['copyright'] = input('copyright:')
            if input('tid(分区，默认为动画区27):') != None:
                uploader['tid'] = 27
            else:
                uploader['tid'] = input('tid:')
            if input('tag(存在默认值):').split(' ') != None:
                uploader['tag'] = ["虚拟UP主","录播","虚拟偶像","直播录像","虚拟up主","VUP"]
            else:
                uploader['tag'] = input('tag:').split(' ')
            if input('thread(同时上传量，默认为4):') != None:
                uploader['thread_pool_workers'] = 4
            else:
                uploader['thread_pool_workers'] = input('thread(同时上传量，默认为4):')
            print(uploader)
            uploader_list.append(uploader)
        dojson.add_uploader(uploader_list)
    elif num <=0:
        print('这是什么呀,我不认识')
    else:
        print('超过一次性添加房间数限制')

def delete_uploader():
    # print(f'现在有{len(dojson.get_namelist())}个房间')
    # print(f'分别为:{dojson.get_namelist()}')
    name_list = input('请选择您要删除的房间名:').split(' ')
    for name in name_list:
        if name in dojson.get_namelist():
            dojson.delete_uploader(name)
    

def modify_uploader():
    num_list = ['copyright', 'thread_pool_workers', 'tid', 'upload_way']
    bool_list = ['do_remove', 'do_upload']
    uploader_list = []
    name_list = input('请选择您要修改的房间名:').split(' ')
    for name in name_list:
        if name in dojson.get_namelist():
            uploader = dojson.get_uploader(name)
            print(f'您正在修改房间{name}')
            print(uploader)
            modify_list = input('请输入您要修改的变量:').split(' ')
            # print(modify_list)
            variable_list = []
            for key in uploader:
                variable_list.append(key)
            # print(variable_list)
            for variable in modify_list:
                if variable in variable_list:
                    print(uploader[f'{variable}'])
                    if variable == 'desc':
                        print(str(f'将变量{variable}由'+str(uploader[f'{variable}'])+'修改为(输入0以停止输入):'))
                        uploader[f'{variable}'] = noline_input()
                    elif variable in num_list:
                        print(str(f'将变量{variable}由'+str(uploader[f'{variable}'])+'修改为:'))
                        uploader[f'{variable}'] = int(input())
                    elif variable in bool_list:
                        print(str(f'将变量{variable}由'+str(uploader[f'{variable}'])+'修改为(有输入为true,什么都不输即为false):'))
                        uploader[f'{variable}'] = bool(input())
                    else:
                        uploader[f'{variable}'] = input(str(f'将变量{variable}由'+uploader[f'{variable}']+'修改为:'))
            print(uploader)
            uploader_list.append(uploader)
            dojson.modify_uploader(uploader_list,name)

def modify_set():
    num_list = ['delete_time', 'pause_time', 'test_time']
    sets = dojson.get_set()
    # print('目前变量为(建议打开json手动修改):')
    print('当前为')
    print(sets)
    set_list = input('请输入您要修改的变量:').split(' ')
    variable_list = []
    for key in sets:
        variable_list.append(key)
    for variable in set_list:
        if variable in variable_list:
            if variable in num_list:
                print(str(f'将变量{variable}由'+str(sets[f'{variable}'])+'修改为:'))
                sets[f'{variable}'] = int(input())
            else:
                sets[f'{variable}'] = input(str(f'将变量{variable}由'+sets[f'{variable}']+'修改为:'))
                print('已修改')
                print(sets)
        # else:
        #     print()
    dojson.modify_set(sets)

    

def main():
    if not os.path.isfile(json_path):
       dojson.set_initial()
    while True:
        print(f'现在有{len(dojson.get_namelist())}个房间')
        print(f'分别为:{dojson.get_namelist()}')
        print('请选择您要进行的操作:')
        print('1:增加房间 2:删除房间 3:修改房间 4:修改设置')
        flag = input()
        # print(flag)
        try:
            if flag == '1':
                add_uploader()
            elif flag == '2':
                delete_uploader()
            elif flag == '3':
                modify_uploader()
            elif flag == '4':
                modify_set()
            else:
                print('请输入您想选择对象的数字哟')
        except Exception as e:
            traceback.print_exc(file=open('./日志/错误日志.log','a',encoding='utf-8'))

if __name__ == '__main__':
    main()