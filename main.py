import requests
import json
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from bs4 import BeautifulSoup
import re
from github_port import github_port
from get_repo import get_repo
from get_vcpkg_version import get_vcpkg_version

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

    # 调用get_vcpkg_version
    content,vcpkg_data_list = get_vcpkg_version(port_name)

    #调用github_repos
    github_repos = github_port()

    #调用get_repos
    github_repo = get_repo(content)
    
    # 将数据转换为表格
    vcpkg_version_df = pd.DataFrame(vcpkg_data_list)
    print(vcpkg_version_df)

    # 创建邮件对象
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = 'vcpkg.json 表格数据'

    # 将表格数据转换为csv格式，并作为附件添加到邮件中
    csv_data = vcpkg_version_df.to_csv(index=False)
    attachment = MIMEApplication(csv_data.encode(), Name='vcpkg.csv')
    attachment['Content-Disposition'] = 'attachment; filename="vcpkg.csv"'
    msg.attach(attachment)

    # 使用SMTP_SSL发送邮件
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp:
        smtp.login(username, password)
        smtp.send_message(msg)
else:
    print("Failed to retrieve port links.")
