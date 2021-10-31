import shutil
import os
import glob
import dojson

def remove_file(old_path, new_path, vup_name):
    '''转存文件具体实现'''
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

def main(vup_name):
    '''转存文件'''
    vedio_path = dojson.get_set()['video_path']
    backup_path = dojson.get_set()['backup_path']
    remove_file(vedio_path, backup_path, vup_name)

if __name__ == '__main__':
    main(vup_name)