from urllib import response
import requests
import json
from typing import List
from baseline_version_get import baseline_version_get
from get_link import get_link

def get_port_info_vcpkg(port_name:list) -> List[str]:

    vcpkg_data_list = []
    xml_data_list = []

    # 读取每个端口的vcpkg.json文件并提取名称和版本信息
    json_url = 'https://raw.githubusercontent.com/microsoft/vcpkg/master/ports/' + port_name + '/vcpkg.json'
    baseline_version = baseline_version_get(port_name)
    link = get_link(port_name)

    json_response = requests.get(json_url)
    if json_response.status_code == 200:
        content = json_response.content.decode('utf-8')
        vcpkg_data = json.loads(content)
        if 'version' in vcpkg_data:
                Version = vcpkg_data.get('version')
                Version_type = 'version'
        elif 'version-date' in vcpkg_data:
            Version = vcpkg_data.get('version-date')
            Version_type = 'version-date'
        elif 'version-semver' in vcpkg_data:
            Version = vcpkg_data.get('version-semver')
            Version_type = 'version-semver'
        elif 'version-string' in vcpkg_data:
            Version = vcpkg_data.get('version-string')
            Version_type = 'version-string'
        else:
            Version = 'N/A'

        name = vcpkg_data.get('name')
        port_version = vcpkg_data.get('port-version')
        description = vcpkg_data.get('description')
        homepage = vcpkg_data.get('homepage')
        license = vcpkg_data.get('license')
        supports = vcpkg_data.get('supports')

        dependencies = []
        for dep in vcpkg_data.get('dependencies', []):
            if isinstance(dep, dict):
                dependencies.append(dep)
            else:
                dependencies.append(dep)

        xml_data_list.append({
            'name': name,
            'version': Version,
            'portVersion': port_version,
            'description': description,
            'homepage': homepage,
            'license': license,
            'supports': supports,
            'dependencies': dependencies,
            'baseline_version': baseline_version,
        })

        vcpkg_data_list.append({'Name': name, 'Version': Version, 'Version_type': Version_type})

    elif json_response.status_code == 401:
        print('你无权访问vcpkg的json文件')
        vcpkg_data_list.append({'错误的网络生成的': name, 'Version': 'N/A', 'Version_type':'N/A'})
    else:
        print(f"Failed to retrieve {json_url}.")
        vcpkg_data_list.append({'Name': '错误的网络生成的', 'Version': 'N/A', 'Version_type':'N/A'})
        xml_data_list.append({
            'Name': name,
            'Version': 'N/A',
            'portVersion': 'N/A',
            'description': 'N/A',
            'homepage': 'N/A',
            'license': 'N/A',
            'supports': 'N/A',
            'dependencies': 'N/A',
            'baseline_version': 'N/A',
            'Version_type': 'N/A'
        })

    return vcpkg_data_list, xml_data_list

        