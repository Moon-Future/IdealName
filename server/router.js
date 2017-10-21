var express = require('express');
var router = express.Router();
var api = require('./api');

router.get('/convert', (req, res, next) => {
    api.convert(req, res, next);
})

router.post('/search', (req, res, next) => {
    api.search(req, res, next);
})

router.get('/spider', (req, res, next) => {
    api.spider(req, res, next);
})

module.exports = router;
