from asyncio.windows_events import NULL
from urllib import response
import requests
import json
from typing import List
from get_link import get_link

def baseline_version_get(port_name:list) -> List[str]:

    port_prefix = port_name[0]
    xml_data_list = []
    baseline_url = 'https://raw.githubusercontent.com/microsoft/vcpkg/master/versions/' + port_prefix + '-/' + port_name + '.json'
    json_response = requests.get(baseline_url)
    if json_response.status_code == 200:

        content = json_response.content.decode('utf-8')
        data = json.loads(content)
        versions = data.get('versions', [])
        
        for version_data in versions:
            git_tree = version_data.get('git-tree', '')
            version = version_data.get('version', '')
            port_version = version_data.get('port-version', '')

            xml_data_list.append({
                'gitTree': git_tree,
                'version': version,
                'portVersion': port_version,
                'link': NULL
            })

        return xml_data_list
    elif response.status.code == 401:
        print('你无权访问vcpkg的这个端口的baseline: {}'.format(port_name))

    else:
        print(f"Failed to retrieve {baseline_url}.")
        return []

    baseline_version = print(json.dumps(xml_data_list, indent=2)) 
    return baseline_version
