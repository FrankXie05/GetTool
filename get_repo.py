import requests
from bs4 import BeautifulSoup
import re


def get_repo(content: str) -> str:
    """
    This function extracts the github repository information from a given string.

    Args:
        content (str): The string to extract the github repository information from.

    Returns:
        str: The github repository information if found, else None.
    """
    # 判断repo地址

    if 'vcpkg_from_github(\n' in content:
        github_repo = re.search(r"vcpkg_from_github\(\n", content)
        if github_repo:
            return github_repo.group(1)

    elif 'vcpkg_from_gitlab(\n' in content:
        gitlab_repo = re.search(r"vcpkg_from_gitlab\(\n", content)
        if gitlab_repo:
            return gitlab_repo.group(1)

    elif 'vcpkg_from_git(\n' in content:
        git_repo = re.search(r"vcpkg_from_git\(\n", content)
        if git_repo:
            return git_repo.group(1)

    elif 'vcpkg_from_sourceforge(\n' in content:
        sourceforge_repo = re.search(r"vcpkg_from_sourceforge\(\n", content)
        if sourceforge_repo:
            return sourceforge_repo.group(1)

    elif 'vcpkg_download_distfile(ARCHIVE\r\n' in content:
        other_repo = re.search(r"vcpkg_download_distfile\(ARCHIVE\r\n", content)
        if other_repo:
            return other_repo.group(1)

    return None
