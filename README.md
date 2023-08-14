# xigua_downloader
下载西瓜视频的单个视频或合集
### date 2023/8/14借助ChatGPT完成开发

# 使用方法
## 下载单个视频

1. 访问一个URL将其中的数字部分部分复制下来

    e.g.

    ![image-20230814213233673](https://git.acwing.com/wangjunji/my_cdn/-/raw/main/pictures/2023_08_14/image-20230814213233673_time_21h32m46s.png)

    7260831939848995364

2. 将数字写入list.txt（UTF-8）

3. 运行xigua_downloader.py，注意报错

## 下载合集

1.访问合集中的任何一个视频（注意要从合集进入，一定要使用Chrome浏览器）

![image-20230814214040436](https://git.acwing.com/wangjunji/my_cdn/-/raw/main/pictures/2023_08_14/image-20230814214040436_time_21h40m43s.png)

2. 然后按F12，选择网络搜索`pseries_more`

   ![image-20230814214318829](https://git.acwing.com/wangjunji/my_cdn/-/raw/main/pictures/2023_08_14/image-20230814214318829_time_21h43m21s.png)

3. 这时会出现四个请求，一个一个地点进去，复制其中的相应数据到origin_data.txt

      ![image-20230814214556895](https://git.acwing.com/wangjunji/my_cdn/-/raw/main/pictures/2023_08_14/image-20230814214556895_time_21h45m59s.png)

4. 运行get_list.py，最好先创建list.txt

![image-20230814214741627](https://git.acwing.com/wangjunji/my_cdn/-/raw/main/pictures/2023_08_14/image-20230814214741627_time_21h47m44s.png)

这里会显示有多少的视频***一定要注意核对数目***
5. 运行xigua_downloader.py，注意报错

## 依赖项

```python
# xigua_downloader.py
import requests
import json
import base64
import os
from bs4 import BeautifulSoup
# get_list.py
# 无
```

还需要`curl`在本地目录 

- Windows https://curl.se/windows/

- Linux 用包管理器安装curl
