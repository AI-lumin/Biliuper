from bilibiliuploader.bilibiliuploader import BilibiliUploader
from bilibiliuploader.core import VideoPart, login
import os
import time
import shutil
import glob
import dojson
# import sys

#出现login fail, error code = -662，说明账号或密码错误
#传输过程中请注意保持网络通畅
#录播姬的命名格式请采用{date}_{name}_{title}a/{date}_{name}_{title}_{time}.flv


def remove_file(old_path, new_path, vup_name):
    print(old_path)
    print(new_path)
    filelist = glob.glob(os.path.join(old_path, '*'+vup_name+'*')) #列出绝对路径
    # filelist.remove('config.backup.json')
    # filelist.remove('config.json')
    print(filelist)
    for file in filelist:
        src = file
        dst = os.path.join(new_path, file.split('\\')[-1])
        print('src:', src)
        print('dst:', dst)
        shutil.move(src, dst)

def do_text(filename):
    file_split = filename.split('\\')[-1]
    start=(file_split).find("_",13)
    end=(file_split).rfind("_")
    text=(file_split)[start+1:end]
    print('text:'+text)
    time_name = file_split.split("_")[0]
    return text,time_name

def do_data(time):
    year = time[0:4] #前包后不包
    month = time[4:6]
    day = time[6:8]
    # time_name = year+'年'+month+'月'+day+'日'
    time_name = month+'月'+day+'日'
    return time_name

def main(vup_name):
    json_path = ".//setting.json"
    video_path=dojson.read_set()[0] #录播姬的录像文件目录
    backup_path=dojson.read_set()[1] #上传完后，视频会移动到这个目录
    # vup_name = sys.argv[1] #会从monitor传过来vupname
    # vup_name = '仙也不知道'
    uploader_got = dojson.get_uploader(vup_name)
    # print(uploader_got)
    user_name = str(uploader_got['username'])
    # print(user_name)
    user_password = str(uploader_got['password'])
    up_tags = list(uploader_got['tag'])
    up_copyright = int(uploader_got['copyright'])
    up_source = str(uploader_got['source'])
    up_tid = int(uploader_got['tid'])
    up_thread = int(uploader_got['thread_pool_workers'])
    up_desc = str(uploader_got['desc'])

    print(time.strftime("%Y-%m-%d", time.localtime())+' 开始上传喽！')

    uploader = BilibiliUploader()
    # print(user_name, user_password)
    uploader.login(user_name, user_password) #手机or邮箱，密码，请自己改一下
    parts = []
    # files=os.listdir(video_path)
    #PermissionError: [Errno 13] Permission denied:,出现这个报错是因为video_path下有文件夹
    # files = glob.glob(os.path.join("./", "*.flv"))
    # print(files)
    files = glob.glob(os.path.join(video_path+'*\\', '*'+vup_name+'*.flv'))
    files.sort(key = lambda file: os.path.getmtime(file))
    print(files)
    for i in range(len(files)):
        files[i] = files[i].split('\\')[-2]+'\\'+files[i].split('\\')[-1]

    count=len(files)
    print(f'现在有{count}个文件')
    
    if 0<count<20:
        for i in range(0,count):
            parts.append(VideoPart(
                path=video_path+files[i],
                title="part{}".format(i+1),
                # title="p{}:{}".format(i+1,files[i].split('.')[0]),
                desc=vup_name #请修改视频描述
            ))
            print(video_path+files[i])
            print("part{}".format(i+1))
            # print("p{}:{}".format(i+1,files[i].split('.')[0]))
        
        time_name = do_text(files[0])[1]
        print(time_name)
        text = do_text(files[0])[0]

        title='【'+vup_name+'】{} {} 【直播录像】'.format(do_data(time_name),text)
        # print(title)
        up_tags.extend([vup_name,]) #可以在这里继续加tag
        test_tag = ",".join(up_tags)
        print(test_tag)

        print(parts)
        avid, bvid = uploader.upload(
            parts=parts,
            copyright=up_copyright, #1为原创2为转载
            title=title, #请修改投稿标题前缀
            tid=up_tid, # tid是投稿分区，数值请参考这个链接-->https://github.com/FortuneDayssss/BilibiliUploader/wiki/Bilibili%E5%88%86%E5%8C%BA%E5%88%97%E8%A1%A8
            tag=",".join(up_tags), #请修改视频tag
            desc="{} ".format(title)+up_desc, #请修改视频描述
            source=up_source,#来源,会自动加到简介前面
            thread_pool_workers=up_thread,
        )
        print(avid,bvid)
        # uploader.edit(
        #     avid=avid,
        #     cover='/cover_folder/cover.png',
        #     max_retry = 5
        # )
        remove_file(video_path, backup_path, vup_name)
    elif count == 0:
        print('还没有文件')
    else:
        print('超出最大上传量(20),你的录播可能成碎片了')

if __name__ == '__main__':
    
    # print(video_path,backup_path,vup_name,user_name,user_password,\
    #      up_tags,up_copyright,up_source,up_tid,up_thread,up_desc)
    # main('文静')
    main(vup_name)

