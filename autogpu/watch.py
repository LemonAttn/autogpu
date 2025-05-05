import requests
from fake_useragent import UserAgent

gpu2region = {
    'RTX 5090': [["west-B", "west-C"]],
    'RTX 4090': [['nm-B1', 'nm-B2'], ["cq-A1"], ["west-B", "west-C"], ["bj-B1"]],
    'RTX 4090D': [["cq-A1"], ["west-B", "west-C"]],
    'RTX 3090': [['nm-B1', 'nm-B2'], ["cq-A1"], ["west-B", "west-C"], ["beijing-A", "beijing-B", "beijing-D", "beijing-E"], ["yz-A1"]],
    'RTX 3080*2': [['nm-B1', 'nm-B2'], ["west-B", "west-C"]],
    'RTX 3080 Ti': [["west-B", "west-C"]],
    'RTX 3080': [["beijing-A", "beijing-B", "beijing-D", "beijing-E"]],
    'RTX 3060': [["west-B", "west-C"]],
    'RTX 2080 Ti *2': [['nm-B1', 'nm-B2'], ["cq-A1"]],
    'RTX 2080 Ti': [["beijing-A", "beijing-B", "beijing-D", "beijing-E"]],
    'RTX 1080 Ti': [["west-B", "west-C"]],
    'vGPU-32G': [['nm-B1', 'nm-B2'], ["west-B", "west-C"]],
    'vGPU-48G': [["west-B", "west-C"]],
    'V100-32GB': [["foshan-A"], ["beijing-C"]],
    'V100-SXM2-32GB': [["beijing-A", "beijing-B", "beijing-D", "beijing-E"]],
    'A100-PCIE-40GB': [["foshan-A"]],
    'A100-SXM4-80GB': [["neimeng-A", "neimeng-C", "neimeng-D"]],
    'L20': [["bj-C1"]],
    'L40': [["west-B", "west-C"]],
    'A40': [["neimeng-A", "neimeng-C", "neimeng-D"]],
    'H800': [["west-B", "west-C"]],
    'A800': [["nm-A1"]],
    'H20-NVLink': [["beijing-A", "beijing-B", "beijing-D", "beijing-E"], ["bj-C1"]],
    'TITAN Xp': [['nm-B1', 'nm-B2']],
    'Tesla T4': [["foshan-A"]],
    'RTX A4000': [["west-B", "west-C"]],
    'CPU': [["cq-A1"], ["west-B", "west-C"]],
    'CPU-close-HT': [["west-B", "west-C"]],
    '910B2x鲲鹏920': [["gd-A1"]]
}


def watch_gpu(config, gpu):
    url = 'https://www.autodl.com/api/v1/machine/region/gpu_type'
    headers = {
        'User-Agent': UserAgent().random,
        'Authorization': config.Authorization
    }
    gpu_info = {}
    for region in gpu2region[gpu]:
        response = requests.post(url = url, headers = headers, json = {'region_sign_list': region}).json()
        for v in response['data']:
            if list(v.keys())[0] == gpu:
                gpu_info[str(region)] = {**{'gpu': gpu}, **v[list(v.keys())[0]]}
                break
            else:
                continue
    return gpu_info


def watch_wallet(config):
    url = 'https://www.autodl.com/api/v1/wallet'
    headers = {
        'User-Agent': UserAgent().random,
        'Authorization': config.Authorization
    }
    response = requests.get(url = url, headers = headers).json()
    wallet = {
        'assets': float(response['data']['assets']) / 1000,
        'used_assets': float(response['data']['accumulate']) / 1000,
        'total_recharge_asset': float(response['data']['total_recharge_asset']) / 1000,
    }
    return wallet


def watch_vip(config):
    url = 'https://www.autodl.com/api/v1/user/member/detail'
    headers = {
        'User-Agent': UserAgent().random,
        'Authorization': config.Authorization
    }
    response = requests.get(url = url, headers = headers).json()
    if response['data']['level_acq_mode'] == 'vip_student':
        return True
    else:
        return False