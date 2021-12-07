import json
import random
import string
from time import sleep

import requests


def sign(times, sleep_seconds):
    headers = {
        'Proxy-Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'DNT': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Mobile Safari/537.36',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'http://h5.vote.cmstop.com',
        'Referer': 'http://h5.vote.cmstop.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    # 获取用来签名的随机字符串
    nonce = ''.join(random.sample(string.ascii_letters + string.digits, 22)).lower()
    print("nonce: ", nonce)
    data = {"nonce": nonce}
    response = requests.post('http://api.vote.cmstop.com/api/get_sign', headers=headers, data=json.dumps(data),
                             verify=False)
    print("response: ", response.text)
    res = json.loads(response.text)['data']
    print("timestamp: ", res['timestamp'])
    print("sign: ", res['sign'])
    submit(nonce, res['sign'], res['timestamp'], times, sleep_seconds)


def submit(nonce, sign_str, timestamp, device_times, sleep_time):
    headers = {
        'Proxy-Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'DNT': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Mobile Safari/537.36',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'http://h5.vote.cmstop.com',
        'Referer': 'http://h5.vote.cmstop.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    # 投票id，每次发起的投票 id 都不同，看投票网址最后一截
    vote_id = "abcdef"

    # 生成随机设备id，用来突破投票限制
    device_id = ''.join(random.sample(string.ascii_letters + string.digits, 32)).lower()
    print("device_id: ", device_id)

    # 投票的选项，用浏览器正常投一遍，看 data 即可找到
    choices = [123456]
    # 投票数据
    data = {"vote_id": vote_id, "choices": choices, "platform": 0, "device_id": device_id, "timestamp": timestamp,
            "nonce": nonce, "sign": sign_str}

    for i in range(device_times):
        response = requests.post('http://api.vote.cmstop.com/api/stat', headers=headers, data=json.dumps(data),
                                 verify=False)
        res = json.loads(response.text)
        print(res)
        sleep(sleep_time)


if __name__ == '__main__':
    # 要投票的人数
    total = 1000
    # 每个人能投的票数
    times = 2
    # 每次之后的休息时间，最少1秒，不要给投票软件造成负担
    sleep_time = 1
    for i in range(total):
        sign(times, sleep_time)