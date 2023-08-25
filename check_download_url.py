import requests
from bs4 import BeautifulSoup
import re
import json


def check_download_url(port_names,content: str) -> tuple[list, list]:
    """
    This function extracts the github repository information from a given string.

    Args:
        content (str): The string to extract the github repository information from.

    Returns:
        str: The github repository information if found, else None.
    """
    # 判断repo地址
    get_no_repo = []
    if 'vcpkg_from_github(\n' in content:
        get_repo = re.search(r"vcpkg_from_github\(\n", content)

    elif 'vcpkg_from_gitlab(\r\n' in content or 'vcpkg_from_gitlab(\n' in content:
        get_repo = re.search(r"vcpkg_from_gitlab\(\r\n|vcpkg_from_gitlab\(\n", content)
        if get_repo:
            return get_repo.group(), get_no_repo

    elif 'vcpkg_from_git(\n' in content:
        get_repo = re.search(r"vcpkg_from_git\(\n", content)

    elif 'vcpkg_from_sourceforge(\r\n' in content or 'vcpkg_from_sourceforge(\n' in content:
        get_repo = re.search(r"vcpkg_from_sourceforge\(\r\n|vcpkg_from_sourceforge\(\n", content)
        if get_repo:
            return get_repo.group(), get_no_repo

    elif 'vcpkg_download_distfile(ARCHIVE\r\n' in content:
        get_repo = re.search(r"vcpkg_download_distfile\(ARCHIVE\r\n", content)
    else:
        get_no_repo.append({'Name': port_names})
        return None, get_no_repo

    if get_repo:
        return get_repo.group(), get_no_repo
    else:
        print(f"The port not has function vcpkg_from", port_names)
        return None, get_no_repo