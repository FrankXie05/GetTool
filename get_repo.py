import requests
from bs4 import BeautifulSoup
import re


def get_repo(port_name,content: str) -> str:
    """
    This function extracts the github repository information from a given string.

    Args:
        content (str): The string to extract the github repository information from.

    Returns:
        str: The github repository information if found, else None.
    """
    # 判断repo地址

    if 'vcpkg_from_github(\n' in content:
        get_repo = re.search(r"vcpkg_from_github\(\n", content)

    elif 'vcpkg_from_gitlab(\n' in content:
        get_repo = re.search(r"vcpkg_from_gitlab\(\n", content)

    elif 'vcpkg_from_git(\n' in content:
        get_repo = re.search(r"vcpkg_from_git\(\n", content)

    elif 'vcpkg_from_sourceforge(\n' in content:
        get_repo = re.search(r"vcpkg_from_sourceforge\(\n", content)

    elif 'vcpkg_download_distfile(ARCHIVE\r\n' in content:
        get_repo = re.search(r"vcpkg_download_distfile\(ARCHIVE\r\n", content)
        
    if get_repo:
        print(f"{port_name}: {get_repo.group(0)}")
        return get_repo

    return None
