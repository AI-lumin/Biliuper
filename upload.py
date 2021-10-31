from bilibiliuploader.bilibiliuploader import BilibiliUploader
from bilibiliuploader.core import VideoPart, login, upload
import os
import time
import glob
import dojson
import reprint
import traceback
from biliup.plugins.bili_webup import BiliBili, Data
# import bilibili_up

print = reprint.print


#出现login fail, error code = -662，说明账号或密码错误
#传输过程中请注意保持网络通畅
#录播姬的命名格式请采用{date}_{name}_{title}a/{date}_{name}_{title}_{time}.flv

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

def upload_web():
    '''web方式上传'''
    print(1)

def upload_client(user_name,user_password,count,video_path,files,vup_name,
up_tags,up_copyright,up_tid,up_desc,up_source,up_thread,title):
    '''客户端方式上传'''
    uploader = BilibiliUploader()
    # print(user_name, user_password)
    uploader.login(user_name, user_password) #手机or邮箱，密码，请自己改一下
    parts = []
    # files=os.listdir(video_path)
    #PermissionError: [Errno 13] Permission denied:,出现这个报错是因为video_path下有文件夹
    # files = glob.glob(os.path.join("./", "*.flv"))
    # print(files)
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

def main(vup_name):
    video_path=dojson.get_set()['video_path'] #录播姬的录像文件目录
    backup_path=dojson.get_set()['backup_path'] #上传完后，视频会移动到这个目录
    # uploader_got = dojson.get_uploader(vup_name)
    print('upload_got = '+str(uploader_got))
    user_name = str(uploader_got['username'])
    # print(user_name)
    user_password = str(uploader_got['password'])
    upload_way = int(uploader_got['upload_way'])
    up_tags = list(uploader_got['tag'])
    up_copyright = int(uploader_got['copyright'])
    up_source = str(uploader_got['source'])
    up_tid = int(uploader_got['tid'])
    up_thread = int(uploader_got['thread_pool_workers'])
    up_desc = str(uploader_got['desc'])
    up_title = str(uploader_got['title'])

    print(time.strftime("%Y-%m-%d", time.localtime())+' 开始上传喽！')
    print(f'采用上传方式{upload_way} 1:客户端 2:网页端')

    files = glob.glob(os.path.join(video_path+'*\\', '*'+vup_name+'*.flv'))
    files.sort(key = lambda file: os.path.getmtime(file))
    # print('files' + str(files))
    file_list = files #绝对路径
    print(file_list)
    files = []
    for i in range(len(file_list)):
        i = file_list[i].split('\\')[-2]+'\\'+file_list[i].split('\\')[-1]
        files.append(i)
    count=len(files)
    print(f'现在有{count}个文件')
    print('file_list:'+str(file_list))
    time_name = do_text(files[0])[1]
    print(time_name)
    text = do_text(files[0])[0]

    if up_title.isspace() == True or len(up_title) == 0:
        title = '【'+vup_name+'】{} {} 【直播录像】'.format(do_data(time_name),text)
    else:
        title = up_title
    print('title = '+title)
    up_tags.extend([vup_name,]) #可以在这里继续加tag
    tags=",".join(up_tags)
    # print(tags)
    
    filepath = file_list[0] #要求是绝对路径
    print('filepath:'+str(filepath))

    try:
        if 0<count<20:
            if upload_way == 1:
                upload_client(user_name,user_password,count,video_path,files,vup_name,
                up_tags,up_copyright,up_tid,up_desc,up_source,up_thread,title)


            elif upload_way == 2:
                video = Data()
                video.title = title
                video.desc = "{} ".format(title)+up_desc
                video.source = up_source
                # 设置视频分区,默认为160 生活分区
                video.tid = up_tid
                video.set_tag(up_tags)

                with BiliBili(video) as bili:
                    bili.login_by_password(user_name, user_password)
                    i = 1 
                    for file in file_list:
                        video_part = bili.upload_file(file)  # 上传视频
                        video_part['title'] = f'part{i}'
                        video_part['desc'] = vup_name
                        # print('video_part = ' + str(video_part))
                        video.append(video_part)  # 添加已经上传的视频
                        i += 1 
                    bili.submit()  # 提交视频
                        
            else:
                print('请您选择正确的上传方式')

        elif count == 0:
            print('还没有文件')
        else:
            print('超出最大上传量(20),你的录播可能成碎片了')

    except Exception as e:
        print(traceback.format_exc())  
        traceback.print_exc(file=open('./日志/错误日志.log','a',encoding='utf-8'))

if __name__ == '__main__':
    vup_name = '点赞仙'
    main(vup_name)

