from sqlite3 import connect
from typing import List
import re
from unittest import expectedFailure
from urllib import request
from get_download_url import get_download_url
from check_download_url import check_download_url
import requests
from git import Remote, Repo
from bs4 import BeautifulSoup
import subprocess
import json
import git
import svn.remote
import mercurial.ui
import mercurial.hg
import bz2

#import cvs

def get_upstream_version(url,headers, port_name:list) -> List[str]:
    upstream_data_list = []
    while True:
        try:
            repos, content = get_download_url(url,port_name)
            break
        except Exception as e:
            print("获取repos和content失败！！！")

    #VCPKG_POLICY_EMPTY_PACKAGE
    match = re.search(r"VCPKG_POLICY_EMPTY_PACKAGE", content)
    if match:
        upstream_data_list.append({'Name': port_name, 'Version': "EMPTY_PORT", 'Commit': None})
    else:
        pass

    if repos != 0:
        for i in repos:
            if 'vcpkg_from_github(\n' in repos:

                #获取REPO Names
                repo_name = re.search(r"REPO\s+(.+)", content)
                repo_names = repo_name.group(1)
                print(repo_names)

                # 获取tags
                url = f"https://api.github.com/repos/{repo_names}/tags"
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    try:
                        tags = response.json()
                        if len(tags) > 0:
                            latest_tag = tags[0]
                            tag_name = latest_tag['name']
                            commit_sha = latest_tag['commit']['sha']
                            upstream_data_list.append({'Name': repo_names, 'Version': tag_name , 'Commit': commit_sha})
                            return upstream_data_list
                    except json.JSONDecodeError as e:
                        upstream_data_list.append({'Name': repo_names, 'Version': None})
                        print("Failed to parse response JSON: {}".format(e))
                else:
                    print("获取Tags失败")

                # 获取releases
                url = f"https://api.github.com/repos/{repo_names}/releases"
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    try:
                        releases = response.json()
                        if len(releases) > 0:
                            latest_release = releases[0]
                            upstream_data_list.append({'Name': repo_names, 'Version': latest_release})
                            return upstream_data_list
                    except json.JSONDecodeError as e:
                        upstream_data_list.append({'Name': repo_names, 'Version': None})
                        print("Failed to parse response JSON: {}".format(e))
                    else:
                        print("获取Releases失败")
                elif response.status_code == 401:
                    print('你无权访问这个端口的releases: {}'.format(port_name))
                    upstream_data_list.append({'Name': port_name, 'Version': None, 'Commit': None})

                # 获取master分支的commit
                url = f"https://api.github.com/repos/{repo_names}/commits/master"
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    try:
                        latest_commit_info = response.json()
                        latest_master_commit_info = latest_commit_info['sha']
                        upstream_data_list.append({'Name': repo_names, 'Version': None, 'Commit': latest_master_commit_info})
                    except json.JSONDecodeError as e:
                        upstream_data_list.append({'Name': repo_names, 'Version': None})
                        print("Failed to parse response JSON: {}".format(e))
                elif response.status_code == 401:
                    print('你无法访问这个GitHub端口的master commit: {}'.format(port_name))
                    upstream_data_list.append({'Name': port_name, 'Version': None, 'Commit': None})
                else:
                    print("获取Master分支的commit信息失败")
                    upstream_data_list.append({'Name': repo_names, 'Version': None})

            elif 'vcpkg_from_gitlab(\r\n' in repos or 'vcpkg_from_gitlab(\n' in repos:
               # upstream_data_list.append({'Name': port_name, 'Version': None, 'Commit': None})
                repo_name = re.search(r"REPO\s+([^\s]+)", content)
                repo_names = repo_name.group(1)
                print(repo_names)

                if repo_names == 'xiph/speexdsp':
                    gitlab_api_url = 'https://gitlab.xiph.org'
                else:
                    gitlab_url = re.search(r"GITLAB_URL\s+([^\s]+)", content)
                    gitlab_api_url = gitlab_url.group(1)
                    print(gitlab_api_url)

                search_url = f"{gitlab_api_url}/api/v4/projects"

                # 设置GitLab API的访问令牌和GitLab的URL
                headers = ''
                access_token = "glpat-sYrNykoSA4s6yv6JzHY2"
                search_headers = {
                    "PRIVATE-TOKEN": access_token
                }
                headers = search_headers
                #获取Project ID:
                search = f"{search_url}/{repo_names.replace('/', '%2F')}"
                print(search)
                response = requests.get(search, headers=search_headers)

                if response.status_code == 200:
                    try:
                        project = response.json()
                        project_id = project['id']
                        print('Project ID: {}\n'.format(project_id))
                    except json.JSONDecodeError as e:
                        project_id = 0
                        print("Failed to parse response JSON: {}".format(e))

                    if project_id != 0:
                        # 获取Tags
                        url = f"{search_url}/{project_id}/repository/tags"
                        response = requests.get(url, headers=headers)

                        if response.status_code == 200:
                            try:
                                tags = response.json()
                                if len(tags) > 0:
                                    latest_tag = tags[0]
                                    tag_name = latest_tag['name']
                                    commit_sha = latest_tag['commit']['id']
                                    upstream_data_list.append({'Name': port_name, 'Version': tag_name , 'Commit': commit_sha})
                                    return upstream_data_list
                            except json.JSONDecodeError as e:
                                print("Failed to parse response JSON: {}".format(e))
                        elif response.status_code == 401:
                            print('你无权访问这个端口的tags: {}'.format(port_name))
                            upstream_data_list.append({'Name': port_name, 'Version': None, 'Commit': None})
                        else:
                            print("获取Tags失败")

                        # 获取Releases
                        url = f"{search_url}/{project_id}/repository/releases"
                        response = requests.get(url, headers=headers)

                        if response.status_code == 200:
                            try:
                                releases = response.json()
                                if len(releases) > 0:
                                    latest_release = releases[0]
                                    upstream_data_list.append({'Name': port_name, 'Version': latest_release['tag_name'], 'Commit': latest_release['commit']['id']})
                                    return upstream_data_list
                            except json.JSONDecodeError as e:
                                print("Failed to parse response JSON: {}".format(e))
                        elif response.status_code == 401:
                            print('你无权访问这个端口的releases: {}'.format(port_name))
                        else:
                            print("获取Releases失败")

                        # 获取Master分支的Commit
                        url = f"{search_url}/{project_id}/repository/commits/master"
                        response = requests.get(url, headers=headers)

                        if response.status_code == 200:
                            try:
                                latest_commit_info = response.json()
                                latest_master_commit_info = latest_commit_info['id']
                                upstream_data_list.append({'Name': port_name, 'Version': None, 'Commit': latest_master_commit_info})
                                return upstream_data_list
                            except json.JSONDecodeError as e:
                                print("Failed to parse response JSON: {}".format(e))
                        else:
                            print("获取Master分支的commit信息失败")
                            upstream_data_list.append({'Name': port_name, 'Version': None, 'Commit': None})
                    else:
                        print("获取ID失败")
                        upstream_data_list.append({'Name': port_name, 'Version': None, 'Commit': None})
                elif response.status_code == 401:
                    print('你无权访问这个端口的API: {}'.format(port_name))
                    upstream_data_list.append({'Name': port_name, 'Version': None, 'Commit': None})
                else:
                    print('Failed to search projects: {}'.format(response.text))
                    upstream_data_list.append({'Name': port_name, 'Version': None, 'Commit': None})
            elif 'vcpkg_from_git(\n' in repos:
                 git_search_url = re.search(r"URL\s+(\S+)", content)

                 if port_name == 'chromium-base':
                     git_search_url = 'https://chromium.googlesource.com/chromium/src'
                     git_url = git_search_url
                     print(git_url)
                 elif port_name == 'libgpiod':
                    git_search_url = 'https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git'
                    git_url = git_search_url
                    print(git_url)
                 elif port_name == 'qwt':
                    git_search_url = 0
                    git_url = git_search_url
                    print("qwt 存在异常 !!!")
                 else:
                     git_url = git_search_url.group(1) if git_search_url else None

                 # 检查链接是否有效
                 if git_url != 0:
                        response = requests.head(git_url)
                        if response.status_code == 200:
                             repo = Repo()

                             process = subprocess.run(['git', 'remote'], stdout=subprocess.PIPE, cwd=repo.working_tree_dir)
                             remote_names = process.stdout.decode('utf-8').split('\n')

                             if 'origin' not in remote_names:
                                 # 创建远程 Git 仓库对象
                                remote = Remote.add(repo, "origin", git_url)
                             else:
                                 print('Remote "origin" already exists, skipping adding remote')
                                 remote = repo.remote('origin')

                             # 获取最新的commit
                             remote_refs = remote.refs
                             latest_ref = max(remote_refs, key=lambda ref: ref.commit.committed_date)
                             latest_master_commit_info = latest_ref.commit.hexsha

                             if latest_master_commit_info:
                                upstream_data_list.append({'Name': port_name, 'Version': None, 'Commit': latest_master_commit_info})
                             else:
                                upstream_data_list.append({'Name': port_name, 'Version': None, 'Commit': None})
                        else:
                             print(f"{port_name} 访问官网：\n{git_url} 失败 ！！！")
                             upstream_data_list.append({'Name': port_name, 'Version': None, 'Commit': None})
                 else:
                     print(f"{port_name} 访问官网：\n{git_url} 失败 ！！！")
                     upstream_data_list.append({'Name': port_name, 'Version': None, 'Commit': None})

            elif 'vcpkg_from_sourceforge(\r\n' in repos or 'vcpkg_from_sourceforge(\n' in repos:
               # upstream_data_list.append({'Name': port_name, 'Version': None, 'Commit': None})
                def construct_sourceforge_url(repo):
                    base_url = "https://sourceforge.net/projects"
                    project_name = repo.split('/')[0]
                    return f"{base_url}/{project_name}/"

                # 使用这个函数
                repo_name = re.search(r"REPO\s+(.+)", content)
                repo_names = repo_name.group(1)
                print(repo_names)

                repo = repo_names
                sf_url = construct_sourceforge_url(repo)
                print(sf_url)

                def get_git_info(sf_url):
                    repo = git.Repo.clone_from(sf_url, "./temp")
                    tags = [tag.name for tag in repo.tags]
                    master_commit = repo.head.commit.hexsha
                    # 获取发布信息的逻辑根据实际情况进行处理
                    return tags, master_commit

                def get_svn_info(sf_url):
                    repo = svn.remote.RemoteClient(sf_url)
                    tags = repo.list_tags()
                    master_commit = repo.info()['commit_revision']
                    # 获取发布信息的逻辑根据实际情况进行处理
                    return tags, master_commit

                def get_mercurial_info(sf_url):
                    ui = mercurial.ui.ui()
                    repo = mercurial.hg.repository(ui, sf_url)
                    tags = repo.tags()
                    master_commit = repo.changelog.tip()
                    # 获取发布信息的逻辑根据实际情况进行处理
                    return tags, master_commit

                def get_bazaar_info(sf_url):
                    branch = bzrlib.branch.Branch.open(url)
                    tags = branch.tags.get_tag_dict().keys()
                    master_commit = branch.last_revision()
                    # 获取发布信息的逻辑根据实际情况进行处理
                    return tags, master_commit

                def get_cvs_info(sf_url):
                    tags = []
                    master_commit = None
                    # 获取CVS的标签和主分支提交信息的逻辑根据实际情况进行处理
                    return tags, master_commit

                # 定义需要查询的项目列表
                projects = {
                    "Git": "https://github.com/username/repo.git",
                    "SVN": "https://svn.example.com/repo",
                    "Mercurial": "https://hg.example.com/repo",
                    "Bazaar": "https://bzr.example.com/repo",
                    "CVS": ":pserver:username@example.com:/cvsroot/repo"
                }

                upstream_data_list = []

                for vcs_type, vcs_url in projects.items():
                    if vcs_type == "Git":
                        tags, master_commit = get_git_info(vcs_url)
                    elif vcs_type == "SVN":
                        tags, master_commit = get_svn_info(vcs_url)
                    elif vcs_type == "Mercurial":
                        tags, master_commit = get_mercurial_info(vcs_url)
                    elif vcs_type == "Bazaar":
                        tags, master_commit = get_bazaar_info(vcs_url)
                    elif vcs_type == "CVS":
                        tags, master_commit = get_cvs_info(vcs_url)
                    else:
                        print(f"不支持的版本控制系统: {vcs_type}")
                        continue

                    upstream_data_list.append({
                        'VCS Type': vcs_type,
                        'Tags': tags,
                    'Master Commit': master_commit
                })

                return(upstream_data_list)
                """
            def get_git_info(url):
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    tags = [tag.text for tag in soup.find_all("a", {"class": "css-truncate-target"})]
                    master_commit = soup.find("span", {"class": "commit-id"}).text
                    # 获取发布信息的逻辑根据实际情况进行处理
                    return tags, master_commit
                else:
                    print(f"无法访问URL: {url}")
                    return [], None

                # 定义需要查询的项目列表
                projects = {
                    "Git": "https://github.com/{port_names}/repo"
                }

                upstream_data_list = []

                for vcs_type, vcs_url in projects.items():
                    if vcs_type == "Git":
                        git_url = f"{vcs_url}/tags"
                        tags, master_commit = get_git_info(git_url)
                        upstream_data_list.append({
                            'VCS Type': vcs_type,
                            'Tags': tags,
                            'Master Commit': master_commit
                        })
                    else:
                        print(f"不支持的版本控制系统: {vcs_type}")

                print(upstream_data_list)
                """
            elif 'vcpkg_download_distfile(ARCHIVE\r\n' in repos:
                upstream_data_list.append({'Name': port_name, 'Version': None, 'Commit': None})
            else:
                upstream_data_list.append({'Name': port_name, 'Version': None, 'Commit': None})
        return upstream_data_list
    else:
        upstream_data_list.append({'Name': port_name, 'Version': None, 'Commit': None})
        return upstream_data_list

