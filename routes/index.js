var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Resume Screener, a project for CodeDay Labs' });
});

module.exports = router;
