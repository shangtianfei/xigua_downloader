import requests
import json
import base64
import os
from bs4 import BeautifulSoup
def xigua_download(url):
    # 指定目标URL
    url = "https://www.ixigua.com/" + url + "?wid_try=1" #这里可以自行添加User-Agent和cookie

    # 发送HTTP请求获取URL内容
    response = requests.get(url)

    # 检查是否成功获取内容
    if response.status_code == 200:
        content = response.text
        # 按照字符串 "video_4" 进行切割
        flag = 0
        is_4k = 0
        if content.find("video_5") != -1:
                video_parts = content.split("video_5")
                print("4K")
                is_4k = 1
        else :
            video_parts = content.split("video_4")
            print("1080P")
        while flag == 0 :
            
            response = requests.get(url)
            content = response.content.decode('utf-8')
            if content.find("video_5") != -1:
                video_parts = content.split("video_5")
                is_4k = 1
            else :
                video_parts = content.split("video_4")
        
            for part in video_parts[1:]:
                brace_count = 0
                json_content = ""
                
                for char in part:
                    if char == "{":
                        brace_count += 1
                    elif char == "}":
                        brace_count -= 1
                        if brace_count == 0:
                            json_content =  json_content + char
                            break
                    if brace_count > 0:
                        json_content += char

                if json_content:
                    try:
                        data = json.loads(json_content)
                        
                        # 检查是否有 "codec_type" 为 "bytevc1" 的对象
                        if is_4k == 0:
                                if "codec_type" in data and data["codec_type"] == "bytevc1":
                                    main_url = data.get("main_url")
                                    if main_url:
                                        #print("Main URL:", main_url)
                                        
                                        # 解码 main_url 的值并输出
                                        decoded_url = base64.b64decode(main_url).decode('utf-8')
                                        test = requests.head(decoded_url)
                                        if test.status_code == 200: #这里每次都要下载判断资源是否能访问，速度慢，那位大佬可以优化一下
                                                print("Decoded Main URL:", decoded_url)
                                                soup = BeautifulSoup(content, 'html.parser')
                                                title = soup.title.string.strip()
                                                print("curl  " + "\"" + decoded_url + "\"" + " -o " + "\"" + title + "\"" + ".mp4" + "\"")
                                                os.system("curl  " + "\"" + decoded_url + "\"" + " -o " + "\"" + title  + ".mp4" + "\"")
                                                flag = 1
                                                break
                                    else:
                                        print("No main_url found.")

                                    
                        else :
                        
                            main_url1 = data.get("main_url")
                            if main_url1:
                                #print("Main URL:", main_url)
                                # 解码 main_url 的值并输出
                                decoded_url = base64.b64decode(main_url1).decode('utf-8')
                                test = requests.head(decoded_url)
                                if test.status_code == 200: #这里每次都要下载判断资源是否能访问，速度慢，那位大佬可以优化一下
                                    print("Decoded Main URL:", decoded_url)
                                    soup = BeautifulSoup(content, 'html.parser')
                                    title = soup.title.string.strip()
                                    print("curl  " + "\"" + decoded_url + "\"" + " -o " + "\"" + title + "\"" + ".mp4" + "\"")
                                    os.system("curl  " + "\"" + decoded_url + "\"" + " -o " + "\"" + title  + ".mp4" + "\"")
                                    flag = 1
                    except json.JSONDecodeError as e:
                        print("Error decoding JSON:", e)
    else:
        print("Failed to retrieve content from the URL.")


if __name__ == "__main__":
    with open('list.txt', 'r') as file:  
        for line in file:  
            if line.strip(): 
               xigua_download(line.strip())