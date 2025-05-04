import ast

import requests
from fake_useragent import UserAgent

from .watch import watch_gpu


region2name = {
    "['nm-B1', 'nm-B2']": '内蒙B区',
    "['cq-A1']": '重庆A区',
    "['west-B', 'west-C']": '西北B区',
    "['bj-B1']": '北京B区',
    "['beijing-A', 'beijing-B', 'beijing-D', 'beijing-E']": '北京A区',
    "['foshan-A']": '佛山区',
    "['neimeng-A', 'neimeng-C', 'neimeng-D']": '内蒙A区',
    "['bj-C1']": 'L20专区',
    "['yz-A1']": '3090专区',
    "['beijing-C']": 'V100专区',
    "['nm-A1']": 'A800专区',
    "['gd-A1']": '华为昇腾专区',
}


def get_machine_id(config, gpu, region):
    url = 'https://www.autodl.com/api/v1/user/machine/list'
    headers = {
        'User-Agent': UserAgent().random,
        'Authorization': config.Authorization
    }
    data = {
        'charge_type': 'payg',
        'default_order': True,
        'gpu_idle_num': 1,
        'gpu_type_name': [gpu],
        'page_index': 1,
        'page_size': 10,
        'region_sign_list': ast.literal_eval(region),
    }
    machine_id = []
    response = requests.post(url = url, headers = headers, json = data).json()
    for v in response['data']['list']:
        machine_id.append(v['machine_id'])
    return machine_id


def use(config, gpu):
    url = 'https://www.autodl.com/api/v1/order/instance/create/payg'
    headers = {
        'User-Agent': UserAgent().random,
        'Authorization': config.Authorization
    }
    data = {
        'instance_info': {
            'charge_type': 'payg',
            'expand_data_disk': 0,
            'image': 'hub.kce.ksyun.com/autodl-image/torch:cuda12.4-cudnn-devel-ubuntu22.04-py312-torch2.5.1',
            'machine_id': '',
            'req_gpu_amount': 1
        },
        'price_info': {
            'charge_type': 'payg',
            'expand_data_disk': 0,
            'machine_id': '',
            'num': 1
        }
    }
    gpu_info = watch_gpu(config, gpu)
    for region in gpu_info.keys():
        code = ''
        machine_id = get_machine_id(config, gpu, region)
        for id in machine_id:
            data['instance_info']['machine_id'] = id
            data['price_info']['machine_id'] = id
            response = requests.post(url = url, headers = headers, json = data).json()
            if response['code'] == 'Success':
                code = 'Success'
                print('购买成功')
                print({
                    'gpu': gpu,
                    'region': region2name[str(region)]
                })
                break
            else:
                continue
        if code == 'Success':
            break
        else:
            continue

