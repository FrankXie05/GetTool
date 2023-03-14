import requests
import json
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from bs4 import BeautifulSoup
import re
from get_download_url import get_download_url
from check_download_url import check_download_url
from get_port_info_vcpkg import get_port_info_vcpkg

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
url = 'https://github.com/microsoft/vcpkg/tree/master/ports/'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    # 找到所有文件夹的链接
    links = soup.find_all('a', {'class': 'js-navigation-open Link--primary'})
    # 匹配所有端口的链接
    port_names = []
    for link in links:
            port_names.append(link['title'])

    # 调用get_vcpkg_version返回vcpkg_data_list
    vcpkg_data_list = get_port_info_vcpkg(url,port_names)

    #调用get_repo返回content(portfile)
    port_url,content = get_download_url(url,port_names)

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
