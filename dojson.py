import json
import os
import reprint

print = reprint.print

# 循环调用函数即可

json_path = ".//setting.json"
txt_path = './/set.txt'

def get_set(): 
    '''返回一个set的字典'''
    data = read_json(json_path)['sets']
    return data

def get_namelist():
    '''返回成员列表''' 
    name_list = []
    data = read_json(json_path)
    uploader = data.get('uploader')
    # print(uploader)
    if uploader != None:
        for i in uploader:
            name_list.append(i.get('vupname'))
    return name_list

def get_uploader(name):
    '''根据名字查找，返回一个uploader
    会包含以下内容:vupname,username,password,copyright,
    source,tid,tag,desc,thread_pool_workers,do_upload,do_remove,upload_way
    ''' 
    data = read_json(json_path)
    uploader_list = data.get('uploader')
    uploader = {}
    if uploader_list != None:
        for i in uploader_list:
            if name == i.get('vupname'):
                uploader = i
    return uploader

def get_initialuploader():
    data = read_json(json_path)
    uploader = data.get('initialuploader')
    return uploader


def read_txt(txt_path):
    '''读取txt文件内容'''
    fr = open(txt_path,'r+')
    dic = eval(fr.read())   #读取的str转换为字典
    fr.close()
    return dic

def write_txt(txt_path,dic):
    '''向txt文件写入'''
    fw = open("set.txt",'w+')
    fw.write(str(dic))      #把字典转化为str
    fw.close()

def read_json(json_path): 
    '''读操作,返回python可以处理的字典'''
    if not os.path.isfile(json_path):
        set_initial()
    f = open(json_path,'r',encoding='utf-8')
    read_data = f.read()
    loads_data = json.loads(read_data)
    f.close()
    return loads_data

def write_json(json_path,write_data):
    '''写操作,将python字典写入'''
    f = open(json_path,'w',encoding='utf-8')
    json_data_dumps = json.dumps(write_data,ensure_ascii=False, sort_keys=True, indent=4)
    f.write(json_data_dumps)
    f.close()

def new_json(json_path):
    '''新建空json文件'''
    f = open(json_path,'w',encoding='utf-8')
    f.close()

def set_initial():
    '''设置初始的json数据'''
    initial = {}
    sets = {
    'video_path':"C:\\录播\\", #录播姬的录像文件目录
    'backup_path':"C:\\备份\\", #上传完后，视频会移动到这个目录
    'pause_time':10,
    'test_time':300,
    'delete_time':24,
    'deletelog_time':168
    }
    initialuploader = {
        #upload_way 1是客户端,2是web
        'do_upload':True,
        'do_remove':True,
        'upload_way':1, 
        'vupname':"点赞仙",
        'username':"",
        'password':"",
        'title':"",
        'copyright':2,
        'source':"https://live.bilibili.com/23351571",
        'tid':27,
        'tag':["虚拟UP主","录播","虚拟偶像","直播录像","虚拟up主","VUP"],
        'desc':"""点赞仙天赋一饼 
        https://space.bilibili.com/1777380035""",
        'thread_pool_workers':4
    }
    uploader_list = []
    uploader = initialuploader
    uploader_list.append(uploader)
    initial['uploader'] = uploader_list
    initial['initialuploader'] = initialuploader
    initial['sets'] = sets
    write_json(json_path,initial)

def add_uploader(uploader_list): 
    '''从setjson获取uploaderlist后加到列表后面'''
    data = read_json(json_path)
    data['uploader']+=uploader_list
    write_json(json_path,data)

def delete_uploader(name): 
    '''从setjson获取房间名删除房间'''
    data = read_json(json_path)
    for room in data['uploader']:
        if room['vupname'] == name:
            data['uploader'].remove(room)
    write_json(json_path,data)

def modify_uploader(uploader_list,name):
    '''从setjson传入name和uploader_list进行替换''' 
    delete_uploader(name)
    add_uploader(uploader_list)

def modify_set(sets):
    '''从setjson传入改好的set字典'''
    data = read_json(json_path)
    data['sets'] = sets
    write_json(json_path,data)

def main():
    if not os.path.isfile(json_path):
        set_initial()


if __name__ == '__main__':
    # print(get_uploader('文静'))
    # print(get_set())
    main()

# 可以调用函数呀，让别的py文件调用本py文件的函数


