from typing import List

from get_download_url import get_download_url
from check_download_url import check_download_url

def handle_repos() -> List[str]:
    repos = List(get_download_url())
    for i in repos:
        if 'vcpkg_from_github(\n' in repos:
            pass
        elif 'vcpkg_from_gitlab(\n' in repos:
            pass
        elif 'vcpkg_from_git(\n' in repos:
            pass
        elif 'vcpkg_from_sourceforge(\n' in repos:
            pass
        elif 'vcpkg_download_distfile(ARCHIVE\r\n' in repos:
            pass
        else:
            print("Failed to retrieve port repos.")
