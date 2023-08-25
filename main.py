from email import header
from genericpath import isdir
import subprocess
import PyInstaller
import shutil
import openpyxl
#with open('requirements.txt', 'r') as f:
#    for line in f:
#        package, version = line.strip().split('==')
#        subprocess.call(['C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\Scripts\pip.exe', 'install', f'{package}=={version}'])

import requests
import json
import pandas as pd
import smtplib
import os
import glob
from git import Repo
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from bs4 import BeautifulSoup
import win32com.client as win32
import re
from get_download_url import get_download_url
from check_download_url import check_download_url
from get_port_info_vcpkg import get_port_info_vcpkg
from get_upstream_version import get_upstream_version
from compare_version import compare_version
from send_mail import send_email

# 用你自己的Access Token替换掉这里的<ACCESS_TOKEN>
vcpkg_headers = {
    'User-Agent': 'Mozilla/5.0',
    'Authorization': 'token ',
    'Accept': 'application/json'
}
# 获取所有端口的链接
port_names = []
total_data = []

#Test
port_names.extend(["wtl"])

url = 'https://github.com/microsoft/vcpkg/tree/master/ports/'
response = requests.get(url, headers=vcpkg_headers)
if response.status_code == 200:
    # 检查本地是否有 vcpkg 仓库，如果没有则克隆
    vcpkg_dir = os.path.join(os.getcwd(), 'vcpkg')
    if not os.path.isdir(vcpkg_dir):
        Repo.clone_from('https://github.com/Microsoft/vcpkg.git', vcpkg_dir)
        print("Clone VCPKG Dond")   

    # 列出本地 vcpkg/ports 目录中的所有文件名
    ports_dir = os.path.join(vcpkg_dir, 'ports')

    if os.path.isdir(ports_dir):
        for filepath in os.listdir(ports_dir):
            port_names.append(filepath)
        print(port_names)

        #将vcpkg_port_info逐行添加到表格当中 

        vcpkg_version_df = pd.DataFrame()
        upstream_version_df = pd.DataFrame()

        for port_name in port_names:
            vcpkg_data_list, xml_data_list = get_port_info_vcpkg(port_name)
            upstream_data_list = get_upstream_version(url,vcpkg_headers,port_name)

            port_df = pd.DataFrame(vcpkg_data_list, columns=['Name', 'Version', 'Version_type', 'Upstream_version'])
            upstream_df = pd.DataFrame(upstream_data_list, columns=['Name', 'Version', 'Commit'])
            port_df['Upstream_version'] = upstream_df['Version']
         #  port_df['Update'] = port_df['Version'] == port_df['Upstream_version']

            vcpkg_version_df = pd.concat([vcpkg_version_df, port_df], ignore_index=True)
            upstream_version_df = pd.concat([upstream_version_df, upstream_df], ignore_index=True)

            # 将主 DataFrame 每行数据逐行追加到 CSV 文件
            with open('vcpkg.csv', 'a') as f:
                port_df.to_csv(f, header=f.tell() == 0, index=False)
            with open('upstream.csv', 'a') as f:
                upstream_df.to_csv(f, header=f.tell() == 0, index=False)

            # 将两个 DataFrame 输出到同一个 Excel 文件的不同工作表中
            with pd.ExcelWriter('versions.xlsx') as writer:
                vcpkg_version_df.to_excel(writer, sheet_name='vcpkg_version', index=False)
                upstream_version_df.to_excel(writer, sheet_name='upstream_version', index=False)

            print(f"{port_names.index(port_name)+1}/{len(port_names)}: {str(port_name)} Done")
            print("vcpkg_version:")
            print(vcpkg_version_df)
            print("\nupstream_version:")
            print(upstream_version_df)

            #集中处理version数据
            vcpkg_version_df, upstream_version_df = compare_version(vcpkg_version_df, upstream_version_df)

            #网站后台表格
            
            total_data.extend(xml_data_list)
        
        xml_df = json.dumps(total_data, indent=4, ensure_ascii=False)
        with open('data.json', 'a', encoding='utf-8') as file:
                file.write(xml_df)

        #最终处理version.xlsx
        # 创建一个临时文件，用于保存原始的 Excel 文件
        shutil.copyfile('versions.xlsx', 'temp_versions.xlsx')

        # 加载 'vcpkg_version' 工作表，并进行修改
        df = pd.read_excel('versions.xlsx', sheet_name='vcpkg_version')
        df['Update'] = df['Update'].replace(0, 'FALSE')

        # 创建一个新的 Excel 文件
        with pd.ExcelWriter('versions.xlsx', engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='vcpkg_version', index=False)

        # 加载原始的 Excel 文件
        book = openpyxl.load_workbook('temp_versions.xlsx')

        with pd.ExcelWriter('versions.xlsx', engine='openpyxl', mode='a') as writer:
            for sheet in book.sheetnames:
                if sheet == 'vcpkg_version':
                    continue  # Skip the modified sheet

                df = pd.read_excel('temp_versions.xlsx', sheet_name=sheet)
                df.to_excel(writer, sheet_name=sheet, index=False)

        # 删除临时文件
        os.remove('temp_versions.xlsx')

    else:
        print("Failed to get ports names")
elif response.status_code == 401:
    print('你无权访问vcpkg的官网：{}'.format(url))
else:
    print("Failed to retrieve port links.")

print("运行结束！！！！！！！！！！！！！！！！！")

# 发送邮件
"""
print("开始发送邮件")
script_dir = os.path.dirname(os.path.abspath(__file__))
attachment_path = os.path.join(script_dir, 'versions.xlsx')
subject='Vcpkg Verison Check'
#to='vcpkgcti@microsoft.com'
to='1433351828@qq.com'
#sender='frank <v-frankxie@microsoft.com>'
send_email(subject, to, attachment_path, sender=None)
"""