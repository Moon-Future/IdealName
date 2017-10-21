# import urllib.request
# import urllib
# import re
import time
from selenium import webdriver

# def getWord(url):
#     content = urllib.request.urlopen(url).read().decode('utf-8')

#     # num=re.findall(r'(?<=>)\d{1,5}(?=</i>)', content)
#     # name=re.findall(r'(?<=title=").*?(?=" target)', content)
#     # web=re.findall(r'(?<=href=").*?(?=" title)', content)[95:]

#     return web

# if __name__=='__main__':
#     start = time.clock()
#     url = 'http://www.zdic.net/z/zb/ty.htm'
#     web(url)
#     end = time.clock()
#     print('一共抓取时间:%s Seconds' %(end-start))

# wordMap = {}

# browser = webdriver.Chrome()
# browser.get('http://hanyu.baidu.com/s?wd=卧虎藏龙&from=zici')

# word = browser.find_element_by_xpath("//div[@id='pinyin']/h2/strong").text
# pinyin = browser.find_element_by_xpath("//div[@id='pinyin']/h2/span/b").text
# otherWords = browser.find_elements_by_xpath("//div[@id='jielong-wrapper']/div[@class='tab-content']/a")

# for x in range(len(otherWords)):
#     print(otherWords[x].get_attribute("href"))

# for x in pinyin.split(' '):
#     if (x != '' or x != '[' or x != ']'):
#         arr.append(x)
# key = '|'.join(arr)

# if (key in wordMap and wordMap[key] != word):
#     print('存在相同key，但value不同')
#     wordMap[key + '|' + word] = word
# elif (key not in wordMap):
#     wordMap[key] = word

# print(wordMap)

# with open('百度汉语成语.js', 'w') as f:
#     f.write(str(wordMap))

def getWeb(browser):
    otherWords = browser.find_elements_by_xpath("//div[@id='jielong-wrapper']/div[@class='tab-content']/a")
    webArr = []
    for x in range(len(otherWords)):
        web = otherWords[x].get_attribute("href")
        webArr.append(web)
    return webArr

def getWordPinyin(browser, url, flag):
    if (url != 'http://hanyu.baidu.com/s?wd=心照不宣&from=poem' and url in linked):
        print('已爬取')
        return;

    global count
    browser.get(url)

    if (len(browser.find_elements_by_xpath("//div[@id='word-header']")) != 0):
        print('内容格式错误')
        return

    if (len(browser.find_elements_by_xpath("//div[@class='poem-detail-item-title']")) != 0):
        print('没有相关结果')
        return

    if (len(browser.find_elements_by_xpath("//div[@id='data-container']/div[@class='poem-list-item']/div/a")) != 0):
        web = browser.find_element_by_xpath("//div[@id='data-container']/div[@class='poem-list-item']/div/a").get_attribute("href")
        getWordPinyin(browser, web, True)
        return

    arr = []
    word = browser.find_element_by_xpath("//div[@id='pinyin']/h2/strong").text
    pinyin = browser.find_element_by_xpath("//div[@id='pinyin']/h2/span/b").text
    pinyin = pinyin.replace('[', '')
    pinyin = pinyin.replace(']', '')
    for x in pinyin.split(' '):
        if (x != '' and x != '[' and x != ']'):
            arr.append(x)
    key = '|'.join(arr)

    # if (key in wordMap and wordMap[key] != word):
    #     print('存在相同key，但value不同')
    #     return
    #     wordMap[key + '|' + word] = word
    # elif (key not in wordMap):
    #     wordMap[key] = word

    if (word in wordMap):
        print(word + '已存在')
        return
    else:
        wordMap[word] = key
    count = count + 1

    print('正在爬取第' + str(count) + '个成语 ------ ' + word + ':' + key)

    with open('百度汉语成语.js', 'a') as f:
        # f.write(str(wordMap))
        f.write(word + ':' + key + '\n')

    with open('已爬链接.js', 'a') as f:
        f.write(url + '\n')

    if (flag):
        webArr = getWeb(browser)
        length = len(webArr)
        if (length == 0):
            # browser.close()
            return
        for i in range(length):
            # if (i != length -1):
            #     getWordPinyin(browser, webArr[i], False)
            # else:
            #     getWordPinyin(browser, webArr[i], True)
            getWordPinyin(browser, webArr[i], True)

if __name__ == '__main__':
    linked = {}
    content = []
    with open('已爬链接.js', 'r') as f:
        content = f.readlines()
    for i in range(len(content)):
        linked[content[i].strip()] = i
    print('已经爬取' + str(len(content)) + '个')

    start = time.clock()
    wordMap = {}
    count = len(content)
    browser = webdriver.Chrome()
    # browser = webdriver.PhantomJS()
    url = 'http://hanyu.baidu.com/s?wd=心照不宣&from=poem'
    getWordPinyin(browser, url, True)
    end = time.clock()
    print('一共抓取' + str(count) + ', 花费时间:%s Seconds' %(end-start))


    # browser = webdriver.Chrome()
    # url = 'http://hanyu.baidu.com/s?wd=上下一心&from=poem'
    # browser.get(url)
    # # a = browser.find_elements_by_xpath("//div[@id='jielong-wrapper']/div[@class='tab-content']/a")
    # a = browser.find_elements_by_xpath("//div[@id='word-header']")
    # print(a, len(a))