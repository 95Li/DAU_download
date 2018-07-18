import json
import os

import requests

# Setting timeout
TIMEOUT = 10

main_url = 'http://lf.snssdk.com/api/news/feed/v82/?category=hotsoon_video&iid=33053253765'

headers = {
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
}


def get_content(url, header):
    """
    发送请求，获取内容
    :param url:
    :param header:
    :return:
    """
    return requests.get(url, headers=header, )


def download(medium_type, url, target_folder, video_id):
    file_name = url
    if medium_type == 'video':
        file_name += '.mp4'
    else:
        return

    file_path = os.path.join(target_folder, video_id + '.mp4')
    resp = requests.get(url, stream=True, timeout=TIMEOUT, verify=False, )
    with open(file_path, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=1024):
            f.write(chunk)


html = requests.get(main_url, headers=headers, )
origin_data_dict = json.loads(html.text)
print(html.text)
print('===================')
print(origin_data_dict)
main_content = origin_data_dict.get('data')
for item in main_content:
    item_dict = json.loads(item.get('content'))
    item_url = item_dict.get('raw_data').get('video').get('play_addr').get('url_list')[0]
    uri = item_dict.get('raw_data').get('video').get('play_addr').get('uri')
    print(item_url)
    download('video', item_url, os.getcwd(), uri)
