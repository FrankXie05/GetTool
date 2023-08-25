"""
import os
import win32com.client as win32

from send_mail import send_email

send_email(
subject='这是邮件的主题',
body='这是邮件的正文',
to='v-frankxie@microsoft.com',
attachment_path='versions.xlsx',
sender='v-frankxie@microsoft.com'
)
"""

"""
import os
import pandas as pd

def search_ports(path):
    ports = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file == "portfile.cmake":
                ports.append(os.path.join(root, file))
    return ports

def count_vcpkg_from(ports):
    vcpkg_from_github = []
    vcpkg_from_gitlab = []
    vcpkg_from_git = []
    vcpkg_from_sourceforge = []
    vcpkg_download_distfile = []
    no_from = []

    for port in ports:
        with open(port) as f:
            content = f.read()
            if 'vcpkg_from_github(\n' in content:
                vcpkg_from_github.append((port.split("/")[-2], "vcpkg_from_github"))

            elif 'vcpkg_from_gitlab(\r\n' in content or 'vcpkg_from_gitlab(\n' in content:
                vcpkg_from_gitlab.append((port.split("/")[-2], "vcpkg_from_gitlab"))

            elif 'vcpkg_from_git(\n' in content:
                vcpkg_from_git.append((port.split("/")[-2], "vcpkg_from_git"))

            elif 'vcpkg_from_sourceforge(\r\n' in content or 'vcpkg_from_sourceforge(\n' in content:
                vcpkg_from_sourceforge.append((port.split("/")[-2], "vcpkg_from_sourceforge"))

            elif 'vcpkg_download_distfile(ARCHIVE\r\n' in content:
                vcpkg_download_distfile.append((port.split("/")[-2], "vcpkg_download_distfile"))

            else:
                no_from.append((port.split("/")[-2], "no_from"))

    df_github = pd.DataFrame(vcpkg_from_github, columns=["port_name", "vcpkg_from"])
    df_gitlab = pd.DataFrame(vcpkg_from_gitlab, columns=["port_name", "vcpkg_from"])
    df_git = pd.DataFrame(vcpkg_from_git, columns=["port_name", "vcpkg_from"])
    df_sourceforge = pd.DataFrame(vcpkg_from_sourceforge, columns=["port_name", "vcpkg_from"])
    df_gdistfile = pd.DataFrame(vcpkg_download_distfile, columns=["port_name", "vcpkg_from"])
    df_no = pd.DataFrame(no_from, columns=["port_name", "vcpkg_from"])

    return df_github, df_gitlab, df_git, df_sourceforge, df_gdistfile, df_no

if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "vcpkg", "ports")
    ports = search_ports(path)
    df_github, df_gitlab, df_git, df_sourceforge, df_gdistfile, df_no = count_vcpkg_from(ports)
    print("Ports with vcpkg_from_github:")
    print(df_github.to_string(index=False))

    print("\nPorts with vcpkg_from_gitlab:")
    print(df_gitlab.to_string(index=False))

    print("\nPorts with vcpkg_from_git:")
    print(df_git.to_string(index=False))

    print("\nPorts with vcpkg_from_sourceforge:")
    print(df_sourceforge.to_string(index=False))

    print("\nPorts with vcpkg_download_distfile:")
    print(df_gdistfile.to_string(index=False))

    print("\nPorts with df_no:")
    print(df_no.to_string(index=False))
"""

"""
from get_port_info_vcpkg import get_port_info_vcpkg
port_names = ['openssl', 'libjpeg-turbo', 'libpng']

# 遍历列表并调用函数
for port_name in port_names:
    port_info = get_port_info_vcpkg(port_name)
    print(port_info)
"""

"""
import gitlab
import git
import requests

# GitLab API access token
access_token = "ggopatFJAQwncMzAWaypEKG8kx"
search_headers = {
    "PRIVATE-TOKEN": access_token
}
gitlab_api_url = 'https://gitlab.freedesktop.org'
search_url = f"{gitlab_api_url}/api/v4/projects"
repo_names = 'font/util'

search = f"{search_url}/{repo_names.replace('/', '%2F')}"
print(search)
response = requests.get(search, headers=access_token)
 
if response.status_code == 200:
    project = response.json()
    project_id = project['id']
    print('Project ID: {}\n'.format(project_id))
"""

import requests
from bs4 import BeautifulSoup

search_url = "https://sourceforge.net/p"
def get_sf_info(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        tags = [tag.text for tag in soup.find_all("a", {"class": "css-truncate-target"})]
        master_commit = soup.find("span", {"class": "Commit"}).text
        releases = soup.find("span", {"class": "sidebarmenu"}).text
        # 获取发布信息的逻辑根据实际情况进行处理
        return tags, master_commit, releases
    else:
        print(f"无法访问URL: {url}")
        return [], None

projects = {
    "Git": f"{search_url}/{port_namses}/git/ci/master/tree/",
    "Code": f"{search_url}/{port_namses}/code/ci/tree/",
    "Code2": f"{search_url}/{port_namses}/code/HEAD/tree/",
    "Code3": f"{search_url}/{port_namses}/code/HEAD/tree/tags/",
    #"Svn": "https://svn.example.com/repo",
    #"Mercurial": "https://hg.example.com/repo",
    #"Bazaar": "https://bzr.example.com/repo",
    #"CVS": ":pserver:username@example.com:/cvsroot/repo"
}

upstream_data_list = []

for sf_type, sf_url in projects.times():
    if sf_type == "Git":
        tags, master_commit, releases = get_sf_info(sf_url)
    elif sf_type == "Code":
        tags, master_commit, releases = get_sf_info(sf_url)
    elif sf_type == "Code2":
        tags, master_commit, releases = get_sf_info(sf_url)
    elif sf_type == "Code3":
        tags, master_commit, releases = get_sf_info(sf_url)

    upstream_data_list.append({'Name': port_names, 'Version': tag_name , 'Commit': commit_sha})
    return upstream_data_list

print(upstream_data_list)
