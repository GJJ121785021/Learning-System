import requests
from scrapy import Selector


def english_translate_chinese(string: str) -> str:
    """
    英文翻译成中文
    :param string: 英文
    :return: 中文
    """
    url = f'http://dict.youdao.com/search?q={string}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    response = requests.get(url, headers=headers)
    response = Selector(text=response.text)
    translate_list = response.xpath('//div[@class="trans-container"]/ul/li/text()').getall()
    translate_result = '\n'.join(translate_list).strip()
    return translate_result


def chinese_translate_english(string: str) -> str:
    """
    中文翻译成英文
    :param string: 中文
    :return: 英文
    """
    url = f'http://dict.youdao.com/search?q={string}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    response = requests.get(url, headers=headers)
    response = Selector(text=response.text)
    translate_list = response.xpath('//p[@class="wordGroup"]/span[@class="contentTitle"]/a/text()').getall()[:2]
    translate_result = '\n'.join(translate_list).strip()
    return translate_result


if __name__ == '__main__':
    c = english_translate_chinese('expose')
    print(c)

