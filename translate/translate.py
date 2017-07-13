#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from urllib import request,parse
import json
from colorama import  init, Fore, Back, Style 
import getopt
import sys
from xml.dom import minidom


KEY = '869FCE12F1DDFDDD9BC81253FE77F59F'
API = 'http://dict-co.iciba.com/api/dictionary.php'
TYPE = 'xml'
STRC = {'key':Fore.CYAN,'ps':Fore.BLUE,'pos':Fore.CYAN,'acceptation':'','orig':Fore.YELLOW,'trans':Fore.GREEN}
init(autoreset=True)

def main():
    args=''
    try:
        options, args = getopt.getopt(sys.argv[1:], "hz", ['help','zh'])

        for name, value in options:
            if name in ('-h', '--help'):
                color('英文译中文执行 python translate.py chinese \n中文译英文执行 python translate.py -z 中文',Fore.RED)
                return
            elif name in ('-z','--zh'):
                global TYPE
                TYPE='json'
    except getopt.GetoptError:
        pass
    if not args:
        color('英文译中文执行 python translate.py chinese \n中文译英文执行 python translate.py -z 中文',Fore.RED)
        return
    request_api(parse.quote(args[0]))

#请求API
def request_api(KEYWORD):
    url = API + '?key=' + KEY + '&type=' + TYPE + '&w=' + KEYWORD
    try:
        with request.urlopen(url) as f:
            data = f.read()
            deal_data(data)
    except getopt.GetoptError:
        print('访问接口失败')

#处理返回的数据
def deal_data(data):
    if TYPE == 'json':
        content = json.loads(data.decode('utf-8'))
        #原词
        print(content['word_name'])
        #翻译过后的词
        color('翻译：',Fore.BLUE)
        for item in content['symbols'][0]['parts'][0]['means']:
            color(item['word_mean'],Fore.GREEN)
    else:
        DOMTree = minidom.parseString(data)
        root = DOMTree.documentElement
        xml_show(root)
    
def xml_show(nodes):
    if nodes.hasChildNodes():
        for no in nodes.childNodes:
            xml_show(no)
    else:
        tag = nodes.parentNode.tagName
        if tag in STRC:
            color(nodes.nodeValue.replace('\n',''),STRC[tag])

def color(text,c="Fore.WHITE"):
    print(c+text)       


if __name__ == '__main__':
    main()

