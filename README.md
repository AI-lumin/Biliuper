# Biliuper

b站录播姬辅助上传小帮手 by 艾路明



# 感谢

FortuneDayssss/BilibiliUploader 

ForgQi/biliup



# 使用说明

##### 1.b站录播姬文件保存格式

设置b站录播姬文件保存格式为：

```
{date}_{name}_{title}f/{date}_{name}_{title}_{time}.flv
```

folder那里一定要有字符，否则在windows系统里文件夹结尾处为'.'时可能会出现报错

由于b站投稿限制，单个录制文件应为4g以下

##### 2.设置setting.json

打开BiliUperset.exe，进行设置

##### 3.使用

然后打开BiliUper.exe，就可以自动监视并运行了



# 变量说明

设置信息保存在setting.json内

目前有用的为sets和uploader

##### 1.sets

这里的停等时间是指，为了防止有的主播直播中出现断流而导致提前上传不完整录播，会等一段时间再判断是否上传

```
"backup_path": "C:\\备份\\",  //备份路径（绝对路径）

"delete_time": 24,			//删除一定时间前的录播，单位：小时

"pause_time": 10,			//检测间隔时间，单位：秒

"test_time": 600,			//停等时间，单位：秒，建议为600s

"deletelog_time":168,		//删除一定时间前的日志，单位：小时

"video_path": "C:\\录播\\"	//录播姬的工作路径（绝对路径）
```

##### 2.uploader

视频分区tid可以参考https://github.com/FortuneDayssss/BilibiliUploader/wiki/Bilibili%E5%88%86%E5%8C%BA%E5%88%97%E8%A1%A8

```
"copyright": 2,				//自制还是转载，1是自制，2是转载

"desc": "点赞仙天赋一饼 \nhttps://space.bilibili.com/1777380035",
							//视频简介

"do_remove": true,			//是否将录播转移到备份路径

"do_upload": true,			//是否将录播上传到b站

"password": "",				//你的登录密码

"source": "https://live.bilibili.com/23351571",
							//视频来源

"tag": [""],				//视频标签

"thread_pool_workers": 4,	//同时上传并发数（路线2没法设置）

"tid": 27,					//视频分区

"upload_way": 2,			//上传路线，目前有1和2，1暂时用不了

"username": "",				//你的登录账号

"vupname": "点赞仙"			//主播名称，注意应该设为录播姬主播名字或名字的一部分
```





# 可能的一些问题

##### 1.log乱码

log采用的编码格式为utf-8，如果出现乱码，可以试试将本机的txt文件默认编码格式改为utf-8

具体方法参考：https://blog.csdn.net/shiaohan/article/details/109033193

##### 2.运行卡住

嗯，可以多敲几下回车？具体原理我也不太清楚

##### 3.怎么备份

现阶段我是利用百度网盘会员的文件夹备份功能，直接备份备份文件夹



# 反馈途径

🎈qq群：811017486

♟b站：艾路明，直接私信也可以
