
import requests
import json
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from bs4 import BeautifulSoup
import re

# 邮件发送者和接收者
sender = 'sender@qq.com'
recipient = 'recipient@gmail.com'

# QQ邮箱的SMTP服务器和端口号
smtp_server = 'smtp.qq.com'
smtp_port = 465

# QQ邮箱的账号和授权码（注意不是邮箱密码）
username = 'user@qq.com'
password = 'xxxxxx'

# 获取所有端口的链接
url = 'https://github.com/microsoft/vcpkg/tree/master/ports'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    # 找到所有文件夹的链接
    links = soup.find_all('a', {'class': 'js-navigation-open Link--primary'})
    # 匹配所有端口的链接
    port_name = []
    for link in links:
            port_name.append(link['title'])

    # 读取每个端口的vcpkg.json文件并提取名称和版本信息
    data_list = []
    cont = 0
    port_names = str(port_name)
    for i, port_link in enumerate(port_name):
        json_url = 'https://raw.githubusercontent.com/microsoft/vcpkg/master/ports/' + port_link + '/vcpkg.json'
        json_response = requests.get(json_url)
        if json_response.status_code == 200:
            content = json_response.content.decode('utf-8')
            data = json.loads(content)
            if 'version' in data:
                Version = data.get('version')
            elif 'version-date' in data:
                Version = data.get('version-date')
            elif 'version-semver' in data:
                Version = data.get('version-semver')
            elif 'version-string' in data:
                Version = data.get('version-string')
            else:
                Version = None

            name = data.get('name')
            data_list.append({'Name': name, 'Version': Version})
            cont ++ 1
            print(f"{i+1}/{len(port_name)}: {port_link} Done")
        else:
            print(f"Failed to retrieve {json_url}.")
    
    # 将数据转换为表格
    df = pd.DataFrame(data_list)
    print(df)

    # 创建邮件对象
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = 'vcpkg.json 表格数据'

    # 将表格数据转换为csv格式，并作为附件添加到邮件中
    csv_data = df.to_csv(index=False)
    attachment = MIMEApplication(csv_data.encode(), Name='vcpkg.csv')
    attachment['Content-Disposition'] = 'attachment; filename="vcpkg.csv"'
    msg.attach(attachment)

    # 使用SMTP_SSL发送邮件
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp:
        smtp.login(username, password)
        smtp.send_message(msg)
else:
    print("Failed to retrieve port links.")
