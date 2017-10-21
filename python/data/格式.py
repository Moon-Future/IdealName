import json

wordMap = {}
keyList = []
option = {
    'ā': 'a',
    'á': 'a',
    'ǎ': 'a',
    'à': 'a',
    'ē': 'e',
    'é': 'e',
    'ě': 'e',
    'è': 'e',
    'ī': 'i',
    'í': 'i',
    'ǐ': 'i',
    'ì': 'i',
    'ō': 'o',
    'ó': 'o',
    'ǒ': 'o',
    'ò': 'o',
    'ū': 'u',
    'ú': 'u',
    'ǔ': 'u',
    'ù': 'u',
    'ü': 'v',
    'ǖ': 'v',
    'ǘ': 'v',
    'ǚ': 'v',
    'ǜ': 'v',
    'ń': 'n',
    'ň': 'n',
}
with open('百度汉语成语.js', 'r') as f:
    content = f.readlines()

for x in content:
    word = x.split(':')[0]
    pinyin = x.split(':')[1].strip()
    for key in option:
        if (pinyin.find(key) != -1):
            pinyin = pinyin.replace(key, option[key])
    if (pinyin in wordMap and wordMap[pinyin] != word):
        pinyin = pinyin + '_' + word
    wordMap[pinyin] = word
    keyList.append(pinyin)
wordMap['keyList'] = keyList
wordMap['length'] = len(content)
with open('wordMap.js', 'w') as f:
    f.write(str(wordMap))
