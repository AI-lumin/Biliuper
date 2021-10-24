import json
import os

# 循环调用函数即可

json_path = ".//setting.json"
txt_path = './/set.txt'

def read_set(): #返回一个set的元组
    data = read_json(json_path)
    # video_path = ''
    # backup_path = ''
    # pause_time = 10
    # test_time = 300
    # delete_time = 1
    # if data['video_path'] != None:
    video_path = data['video_path']
    # if data['backup_path'] != None:
    backup_path = data['backup_path']
    # if data['pause_time'] != None:
    pause_time = data['pause_time']
    # if data['test_time'] != None:
    test_time = data['test_time']
    # if data['delete_time'] != None:
    delete_time = data['delete_time']
    return video_path,backup_path,pause_time,test_time,delete_time

def get_namelist(): #返回成员列表
    name_list = []
    data = read_json(json_path)
    uploader = data.get('uploader')
    # print(uploader)
    if uploader != None:
        for i in uploader:
            name_list.append(i.get('vupname'))
    return name_list

def get_uploader(name): #根据名字查找，返回一个uploader
    data = read_json(json_path)
    uploader_list = data.get('uploader')
    uploader = {}
    if uploader_list != None:
        for i in uploader_list:
            if name == i.get('vupname'):
                uploader = i
    return uploader

def read_txt(txt_path):
    fr = open(txt_path,'r+')
    dic = eval(fr.read())   #读取的str转换为字典
    fr.close()
    return dic

def write_txt(txt_path,dic):
    fw = open("set.txt",'w+')
    fw.write(str(dic))      #把字典转化为str
    fw.close()

# def add_uploader(name):
#     uploader ={}
#     vup_name = input('vup_name:')
#     user_name = input('user_name:')
#     user_password = input('user_password:')

#     write_json(json_path,uploader)

def read_json(json_path): #返回python可以处理的字典
    if not os.path.isfile(json_path):
        set_initial()
    f = open(json_path,'r',encoding='utf-8')
    read_data = f.read()
    loads_data = json.loads(read_data)
    f.close()
    return loads_data

def write_json(json_path,write_data):
    f = open(json_path,'w',encoding='utf-8')
    json_data_dumps = json.dumps(write_data,ensure_ascii=False, sort_keys=True, indent=2)
    f.write(json_data_dumps)
    f.close()

def new_json(json_path):
    f = open(json_path,'w',encoding='utf-8')
    f.close()

def set_initial():
    initial = {
    'video_path':"C:\\录播\\", #录播姬的录像文件目录
    'backup_path':"C:\\备份\\", #上传完后，视频会移动到这个目录
    'pause_time':10,
    'test_time':300,
    'delete_time':1
    }
    uploader_list = []
    uploader = {
        'vupname':"点赞仙",
        'username':"",
        'password':"",
        'copyright':2,
        'source':"https://live.bilibili.com/23351571",
        'tid':27,
        'tag':["虚拟UP主","录播","虚拟偶像","直播录像","虚拟up主","VUP"],
        'desc':"""点赞仙天赋一饼 
        https://space.bilibili.com/1777380035""",
        'thread_pool_workers':4
    }
    uploader_list.append(uploader)
    initial['uploader'] = uploader_list
    write_json(json_path,initial)

def add_uploader(uploader_list): #从setjson获取uploaderlist后加到列表后面
    data = read_json(json_path)
    data['uploader']+=uploader_list
    write_json(json_path,data)

def delete_uploader(name): #从setjson获取房间名删除房间
    data = read_json(json_path)
    for room in data['uploader']:
        if room['vupname'] == name:
            data['uploader'].remove(room)
    write_json(json_path,data)

def modify_uploader(uploader_list,name): #从setjson传入name和uploader_list进行替换
    delete_uploader(name)
    add_uploader(uploader_list)

def main():
    if not os.path.isfile(json_path):
        set_initial()

    read_data = read_json(json_path)
    print(read_data)


    json_data_loads = read_data
    print(json_data_loads)

    print(read_set())
    print(read_set()[4])
    print(get_namelist())
    print(len(get_namelist()))
    print(get_uploader('点赞仙'))
    print(get_uploader('浓密仙'))


if __name__ == '__main__':
    # print(get_uploader('文静',json_path))
    main()

# 可以调用函数呀，让别的py文件调用本py文件的函数


