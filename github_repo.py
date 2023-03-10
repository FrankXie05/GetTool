import requests
from bs4 import BeautifulSoup
import re
from typing import List
from get_repo import get_repo


def github_port() -> List[str]:
    """
    This function returns a list of all repositories found in vcpkg ports.

    Returns:
        List[str]: A list of all  repositories found in vcpkg ports.
    """
    # 获取所有端口的链接
    url = 'https://github.com/microsoft/vcpkg/tree/master/ports'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # 找到所有文件夹的链接
        links = soup.find_all('a', {'class': 'js-navigation-open Link--primary'})

        # 匹配所有端口的链接
        port_names = ['3fd']
        for link in links:
            port_names.append(link['title'])

        github_repos = []
        # 读取每个端口的portfile.cmake文件并提取GitHub仓库信息
        for port_name in port_names:
            portfile_url = 'https://raw.githubusercontent.com/microsoft/vcpkg/master/ports/' + port_name + '/portfile.cmake'
            port_response = requests.get(portfile_url)

            if port_response.status_code == 200:
                content = port_response.content.decode('utf-8')
                repo = get_repo(content)

                if repo:
                        print(f"{port_name}: {get_repo.group(0)}")
                        github_repos.append(repo)

                return github_repos
    else:
        print(f"Failed ro retrieve {url}.")
        return []
