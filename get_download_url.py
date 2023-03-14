import requests
from bs4 import BeautifulSoup
import re
from typing import List
from check_download_url import check_download_url


def get_download_url(url,port_names:str) -> List[str]:
    """
    This function returns a list of all repositories found in vcpkg ports.

    Returns:
        List[str]: A list of all  repositories found in vcpkg ports.
    """
    response = requests.get(url)
    if response.status_code == 200:
        port_url = []
        # 读取每个端口的portfile.cmake文件并提取GitHub仓库信息
        for i, port_name in enumerate(port_names):
            portfile_url = 'https://raw.githubusercontent.com/microsoft/vcpkg/master/ports/' + port_name + '/portfile.cmake'
            port_response = requests.get(portfile_url)

            if port_response.status_code == 200:
                content = port_response.content.decode('utf-8')
                repo = check_download_url(port_name,content)

                if repo:
                        port_url.append(repo)

                return port_url,content
    else:
        print(f"Failed ro retrieve {url}.")
        return []
