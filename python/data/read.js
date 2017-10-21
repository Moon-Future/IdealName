var fs = require('fs')
var iconv = require('iconv-lite')

fs.readFile('wordMap.js', (err, data) => {
    if (err) {
        throw err;
    } else {
        data = iconv.decode(data, 'gbk');
        console.log(typeof data);
        data = data.replace(/'/g, '"')
        content = JSON.parse(JSON.stringify(data));
        // console.log(content);
        keyList = data.keyList;
        console.log(keyList);
    }
})