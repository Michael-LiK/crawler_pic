# coding=UTF-8
import requests
import re
import os
import multiprocessing
import config


class meitulu:
    def get_pic_list(self, url):
        response = requests.get(url)
        response.encoding = 'utf-8'
        pic_num_search = re.compile(r'图片： (\d+) 张')
        pic_index_search = re.compile(r'href="https://www.meitulu.com/item/(\d+).html"')
        pic_tag_search = re.compile(r'class="tags">(\w+)</a>')
        pic_title_search = re.compile(r'target="_blank">(.*?)</a>')
        pic_num = pic_num_search.findall(response.text)
        pic_index = pic_index_search.findall(response.text)
        pic_tag = pic_tag_search.findall(response.text)
        pic_title = pic_title_search.findall(response.text)
        pic_index = pic_index[0::2]
        pic_title = pic_title[1::2]

        i = 0
        res = []
        for value in pic_num:
            pic_info = {}
            pic_info['index'] = pic_index[i]
            pic_info['title'] = pic_title[i]
            pic_info['tag'] = pic_tag[i]
            pic_info['num'] = value
            i = i + 1
            res.append(pic_info)
        return res

    def download_img(self, info):
        print('download start' + info['title'])
        dirname = config.base_path + info['title']
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        for i in range(1, int(info['num']) + 1):
            img_url = 'https://mtl.gzhuibei.com/images/img/' + info['index'] + '/' + str(i) + '.jpg'
            print(img_url)
            if (config.proxy_config['open'] == "true"):
                response = requests.get(url=img_url, proxies=config.proxy_config['proxy'])
            else:
                response = requests.get(url=img_url)
            if response.status_code == 200:
                filename = dirname + '/' + str(i) + '.jpg'
                # 打开文件夹并写入图片
                with open(filename, 'wb') as f:
                    f.write(response.content)
        print('download finished' + info['title'])


if __name__ == '__main__':
    bass_path = config.base_path
    if not os.path.exists(bass_path):
        os.mkdir(bass_path)
    client = meitulu()
    pic_list = client.get_pic_list("https://www.meitulu.com/t/minidamengmeng/")
    # config the process pool
    pool = multiprocessing.Pool(config.processes_num)

    for value in pic_list:
        pool.apply_async(client.download_img, args=(value,))
    pool.close()
    pool.join()
    print("crawler end")
