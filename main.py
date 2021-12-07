import json
import random
import string
import sys
from time import sleep

import requests


def sign(times, sleep_time, vote_id, vote_item_id):
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
    # print("nonce: ", nonce)
    data = {"nonce": nonce}
    response = requests.post('http://api.vote.cmstop.com/api/get_sign', headers=headers, data=json.dumps(data),
                             verify=False)
    # print("response: ", response.text)
    res = json.loads(response.text)['data']
    # print("timestamp: ", res['timestamp'])
    # print("sign: ", res['sign'])
    submit(nonce, res['sign'], res['timestamp'], times, sleep_time, vote_id, vote_item_id)


def submit(nonce, sign_str, timestamp, device_times, sleep_time, vote_id, vote_item_id):
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

    # 生成随机设备id，用来突破投票限制
    device_id = ''.join(random.sample(string.ascii_letters + string.digits, 32)).lower()
    # print("device_id: ", device_id)

    # 投票的选项，用浏览器正常投一遍，看 data 即可找到
    choices = [vote_item_id]
    # 投票数据
    data = {"vote_id": vote_id, "choices": choices, "platform": 0, "device_id": device_id, "timestamp": timestamp,
            "nonce": nonce, "sign": sign_str}

    for i in range(device_times):
        response = requests.post('http://api.vote.cmstop.com/api/stat', headers=headers, data=json.dumps(data),
                                 verify=False)
        res = json.loads(response.text)
        print(res["message"])
        sleep(sleep_time)


def get(vote_id, title):
    headers = {
        'Proxy-Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Mobile Safari/537.36',
        'DNT': '1',
        'Origin': 'http://h5.vote.cmstop.com',
        'Referer': 'http://h5.vote.cmstop.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    response = requests.get(
        f'http://api.vote.cmstop.com/api/groups?vote_id={vote_id}&offset=0&order_key=number&order_by=asc&title={title}',
        headers=headers, verify=False)
    # print(response.text)
    return json.loads(response.text)["data"]["data"][0]


# 获取网址的最后一截作为 vote_id
def get_vote_id_from_vote_url(vote_url):
    return vote_url.split('/')[-1]


if __name__ == '__main__':
    # 获取用户输入的投票链接
    vote_url = input("请输入投票链接，输入后回车: ")
    if not vote_url:
        print("投票链接为空或错误")
        sys.exit()
    # 获取投票编号
    vote_id = get_vote_id_from_vote_url(vote_url)
    if not vote_id:
        print("投票链接为空或错误")
        sys.exit()
    # 获取用户输入的用户编号
    title = input("请输入用户编号，输入后回车: ")
    if not title:
        print("用户编号为空或错误")
        sys.exit()
    # 获取投票项
    vote_item = get(vote_id, title)
    print(f'您好，{vote_item["title"]},您的当前票数是：{vote_item["vote_numbers"]}')
    vote_item_id = vote_item["vote_items_id"]
    # 获取用户输入的投票人数
    total = input("请输入投票人数(默认为 1000)，输入数字后回车，或者直接回车取默认值:") or 1000
    # 获取用户输入的每人投票次数
    times = input("请输入每人投票次数(默认为 2)，输入数字后回车，或者直接回车取默认值:") or 2
    # 每次之后的休息时间，最少1秒，不要给投票软件造成负担
    sleep_time = 1
    for i in range(total):
        sign(times, sleep_time, vote_id, vote_item_id)
