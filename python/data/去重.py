wordMap = {}

with open('百度汉语成语.js', 'r') as f:
    content = f.readlines()

for x in content:
    word = x.split(':')[0]
    pinyin = x.split(':')[1]
    wordMap[word] = pinyin

with open('成语.js', 'w') as f:
    for x in wordMap:
        f.write(x + ':' + wordMap[x])