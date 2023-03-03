import requests
from bs4 import BeautifulSoup
import re

# 获取所有端口的链接
url = 'https://github.com/microsoft/vcpkg/tree/master/ports'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    # 找到所有文件夹的链接
    links = soup.find_all('a', {'class': 'js-navigation-open Link--primary'})
    # 匹配所有端口的链接
    port_names = []
    for link in links:
        port_names.append(link['title'])

    # 读取每个端口的portfile.cmake文件并提取GitHub仓库信息
    for i, port_name in enumerate(port_names):
        portfile_url = 'https://raw.githubusercontent.com/microsoft/vcpkg/master/ports/' + port_name + '/portfile.cmake'
        port_response = requests.get(portfile_url)
        if port_response.status_code == 200:
            content = port_response.content.decode('utf-8')
            if 'vcpkg_from_github(\n' in content:
                github_repo = re.search(r"vcpkg_from_github\(\n", content)
                if github_repo:
                    print(f"{port_name}: {github_repo.group(0)}")
            elif 'vcpkg_from_gitlab(\n' in content:
                gitlab_repo = re.search(r"vcpkg_from_gitlab\(\n", content)
                if gitlab_repo:
                    print(f"{port_name}: {gitlab_repo.group(0)}")
            elif 'vcpkg_from_git(\n' in content:
                git_repo = re.search(r"vcpkg_from_git\(\n", content)
                if git_repo:
                    print(f"{port_name}: {git_repo.group(0)}")
            elif 'vcpkg_from_sourceforge(\n' in content:
                sourceforge_repo = re.search(r"vcpkg_from_sourceforge\(\n", content)
                if sourceforge_repo:
                    print(f"{port_name}: {sourceforge_repo.group(0)}")
            elif 'vcpkg_download_distfile(ARCHIVE\r\n' in content:
                other_repo = re.search(r"vcpkg_download_distfile\(ARCHIVE\r\n", content)
                if other_repo:
                    print(f"{port_name}: {other_repo.group(0)}")          
            else:
                print(f"Failed to retrieve {port_name}.")
        else:
            print(f"Failed to retrieve {portfile_url}.")
else:
    print("Failed to retrieve port links.")
