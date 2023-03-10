import requests
import json

def get_vcpkg_version(port_name:str) -> list:
	
    # 读取每个端口的vcpkg.json文件并提取名称和版本信息
    vcpkg_data_list = []
    port_names = str(port_name)
    for i, port_link in enumerate(port_name):
        json_url = 'https://raw.githubusercontent.com/microsoft/vcpkg/master/ports/' + port_link + '/vcpkg.json'
        json_response = requests.get(json_url)
        if json_response.status_code == 200:
            content = json_response.content.decode('utf-8')
            vcpkg_data = json.loads(content)
            if 'version' in vcpkg_data:
                Version = vcpkg_data.get('version')
            elif 'version-date' in vcpkg_data:
                Version = vcpkg_data.get('version-date')
            elif 'version-semver' in vcpkg_data:
                Version = vcpkg_data.get('version-semver')
            elif 'version-string' in vcpkg_data:
                Version = vcpkg_data.get('version-string')
            else:
                Version = None

            name = vcpkg_data.get('name')
            vcpkg_data_list.append({'Name': name, 'Version': Version})
            print(f"{i+1}/{len(port_name)}: {port_link} Done")
        else:
            print(f"Failed to retrieve {json_url}.")

    return content, vcpkg_data_list
