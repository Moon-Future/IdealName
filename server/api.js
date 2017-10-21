var fs = require('fs');
var pinyin = require('pinyinlite');
var request = require('request');
var cheerio = require('cheerio');
// 加载编码转换模块 
var iconv = require('iconv-lite'); 
var fs = require('fs');
var wordMapFile = '../static/wordMap.js';

var getIndex = function(arr, item) {
    let result = [];
    for (let i = 0, len = arr.length; i < len; i++) {
        if (arr[i] === item) {
            result.push(i);
        }
    }
    return result;
}

module.exports = {
    convert(req, res, next) {
        let params = req.query, word = params.word,
            yinpins = pinyin(word), arr = [], obj;
        for (let i = 0, len = word.length; i < len; i++) {
            obj = {};
            obj.word = word[i];
            obj.yinpins = yinpins[i];
            obj.radio = '';
            arr.push(obj);
        }
        res.send({
            status: true,
            data: arr
        });
        res.end();
    },
    search(req, res, next) {
        let postData = req.body, wordArr = postData.data, keyList, keyStr, result = [], tmpObj = {};
        fs.readFile(wordMapFile, (err, data) => {
            if (err) {
                res.send({
                    status: false,
                    msg: '文件读取失败'
                })
                res.end();
            } else {
                data = iconv.decode(data, 'gbk');
                data = JSON.parse(data);
                keyList = data.keyList;
                keyStr = ',' + keyList.join(',') + ',';
                for (let i = 0, len = wordArr.length; i < len; i++) {
                    let word = wordArr[i].word, pinyin = wordArr[i].radio,
                        // 四字成语 开头 中间 结尾
                        arr1 = keyStr.match(new RegExp(',' + pinyin + '[\|].*?,', 'g')) || [],
                        arr2 = keyStr.match(new RegExp(',?[^,]*[\|]' + pinyin + '[\|].*?,', 'g')) || [],
                        arr3 = keyStr.match(new RegExp(',?[^,]*[\|]' + pinyin + ',', 'g')) || [],
                        arr = arr1.concat(arr2, arr3);
                    for (let j = 0, len1 = arr.length; j < len1; j++) {
                        let key = arr[j].replace(/,/g, ''),
                            indexs = getIndex(key.split('|'), pinyin),
                            originWord = data[key],
                            newWord = originWord;
                        if (tmpObj[originWord] !== undefined) {
                            continue
                        } else {
                            tmpObj[originWord] = originWord;
                        }
                        for (let k = 0, len2 = indexs.length; k < len2; k++) {
                            newWord = newWord.replace(newWord[indexs[k]], word);
                        }
                        result.push({originWord, newWord});
                    }
                }
                res.send({
                    status: true,
                    data: result
                });
                res.end();
            }
        })
    },
    spider(req, res, next) {
        request('http://hanyu.baidu.com/s?wd=百里挑一', function (error, response, body) {
            if (!error && response.statusCode == 200) {
                // res.send('hello world');
                var $ = cheerio.load(body);
                var words = $('#u1').html();
                console.log(body);
                res.send(words);
            }
        })
    }
}
