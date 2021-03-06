import requests
from scrapy import Selector
import execjs

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


def get_js_function(js_path, func_name, func_args):
    '''
    获取指定目录下的js代码, 并且指定js代码中函数的名字以及函数的参数。
    :param js_path: js代码的位置
    :param func_name: js代码中函数的名字
    :param func_args: js代码中函数的参数
    :return: 返回调用js函数的结果
    '''

    with open(js_path, encoding='utf-8') as fp:
        js = fp.read()
        ctx = execjs.compile(js)
        return ctx.call(func_name, func_args)


def youdao(word):
    '''
    有道翻译
    :param word: 传入的待翻译的词汇
    :return: 返回的翻译后的内容
    '''
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    result = get_js_function('youdao.js', 'youdao', word)
    data = {
        'i': word,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': result['salt'],
        'sign': result['sign'],
        'ts': result['ts'],
        'bv': result['bv'],
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_CLICKBUTTION',
    }
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '242',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'OUTFOX_SEARCH_USER_ID=1726048911@10.169.0.84; OUTFOX_SEARCH_USER_ID_NCOO=998841688.7251934; _ntes_nnid=a31cda64b2586670bbfaa1138bf220fc,1554879349324; _ga=GA1.2.851305956.1555316006; JSESSIONID=abc-vREXHwVUd8GgTQ8Ww; ___rl__test__cookies=1564385974367',
        'Host': 'fanyi.youdao.com',
        'Origin': 'http://fanyi.youdao.com',
        'Pragma': 'no-cache',
        'Referer': 'http://fanyi.youdao.com/?keyfrom=fanyi.logo',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    response = requests.post(url, data=data, headers=headers)
    return response.json()


if __name__ == '__main__':
    # 第一个仅供翻译单词短语
    c = english_translate_chinese('expose')
    print(c)
    # 第二个是API，可翻译句子
    result = youdao('鸡你太美')
    print(result)
    if result['errorCode'] == 0:
        print('翻译结果:' + result['translateResult'][0][0]['tgt'])

