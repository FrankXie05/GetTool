import requests
import json

def get_port_info_vcpkg(url,port_names:str) -> list:
	
    
    vcpkg_data_list = []
    for i, port_name in enumerate(port_names):
        # 读取每个端口的vcpkg.json文件并提取名称和版本信息
        json_url = 'https://raw.githubusercontent.com/microsoft/vcpkg/master/ports/' + port_name + '/vcpkg.json'
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
            print(f"{i+1}/{len(port_names)}: {port_name} Done")
        else:
            print(f"Failed to retrieve {json_url}.")

    return vcpkg_data_list
