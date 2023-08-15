import requests
import json
import base64
import os
from bs4 import BeautifulSoup



def xigua_download(url):
    # 指定目标URL
    url = "https://www.ixigua.com/" + url +'?wid_try=1'  #这里可以自行添加User-Agent和cookie

    # 发送HTTP请求获取URL内容
    flag = 0
    is_hevc = 0 
    out_q = 0
    while flag == 0 :
            while 1 :
                try:
                    response = requests.get(url)
                    break
                except ConnectionError as e:
                    continue

            content = response.content.decode('utf-8')
            if content.find("video_5") != -1:
                if out_q == 0 :
                    out_q = 1   
                    print("4K")
                video_parts = content.split("video_5")
            else :
                if content.find("video_4") != -1 :
                    if out_q == 0 :
                        out_q = 1 
                        print("1080P")
                    video_parts = content.split("video_4")
                else :
                    if content.find("video_3") != -1 :
                        if out_q == 0 :
                            out_q = 1 
                            print("720P")
                        video_parts = content.split("video_3")
                    else :
                        if content.find("video_2") != -1 :
                            if out_q == 0 :
                                out_q = 1 
                                print("480P")
                            video_parts = content.split("video_2")
                        else :
                             if out_q == 0 :
                                out_q = 1 
                                print("360P")
                             video_parts = content.split("video_1")

               
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
                        if "codec_type" in data and data["codec_type"] == "bytevc1":
                                main_url = data.get("main_url")
                                if main_url:
                                        # 解码 main_url 的值并输出
                                        decoded_url = base64.b64decode(main_url).decode('utf-8')
                                        test = requests.head(decoded_url)
                                        is_hevc = 1
                                        if test.status_code == 200:
                                                print("HEVC")
                                                print("Decoded Main URL:", decoded_url)
                                                soup = BeautifulSoup(content, 'html.parser')
                                                title = soup.title.string.strip()
                                                os.system("curl  " + "\"" + decoded_url + "\"" + " -o " + "\"" + title  + ".mp4" + "\"")
                                                flag = 1
                                                break
                                else:
                                    print("No main_url found.")
                    except json.JSONDecodeError as e:
                        print("Error decoding JSON:", e)              
            if is_hevc == 0 :
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
                            main_url = data.get("main_url")
                            if main_url:     
                                # 解码 main_url 的值并输出
                                decoded_url = base64.b64decode(main_url).decode('utf-8')
                                test = requests.head(decoded_url)
                                if test.status_code == 200:
                                    print("AVC")
                                    print("Decoded Main URL:", decoded_url)
                                    soup = BeautifulSoup(content, 'html.parser')
                                    title = soup.title.string.strip()
                                    os.system("curl  " + "\"" + decoded_url + "\"" + " -o " + "\"" + title  + ".mp4" + "\"")
                                    flag = 1
                                    break
                            else:
                                print("No main_url found.")
                        except json.JSONDecodeError as e:
                            print("Error decoding JSON:", e)            



if __name__ == "__main__":
    with open('list.txt', 'r') as file:  
        for line in file:  
            if line.strip(): 
               xigua_download(line.strip())
