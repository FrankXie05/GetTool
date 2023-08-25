import requests
from bs4 import BeautifulSoup
import re
from typing import List
from check_download_url import check_download_url
import json


def get_download_url(url,port_name:list) -> List[str]:
    """
    This function returns a list of all repositories found in vcpkg ports.

    Returns:
        List[str]: A list of all  repositories found in vcpkg ports.
    """

    response = requests.get(url)
    if response.status_code == 200:
        port_url = []
        # 读取每个端口的portfile.cmake文件并提取GitHub仓库信息
        portfile_url = 'https://raw.githubusercontent.com/microsoft/vcpkg/master/ports/'+ port_name + '/portfile.cmake'
        port_response = requests.get(portfile_url)

        if port_response.status_code == 200:
            content = port_response.content.decode('utf-8')
            get_repo, get_no_repo = check_download_url(port_name,content)

            if get_repo is not None:
                port_url.append(get_repo)
            else:
                print(f"The port no download_url: {port_name}.")
                port_url.append(get_no_repo)

            return port_url,content
    else:
        print(f"Failed ro retrieve {url}.")
        return []
