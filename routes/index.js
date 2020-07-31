var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { result: '', resume: '' });
});

router.use(express.urlencoded());
router.use(express.json());

/* POST to get screening result */
const {spawn} = require('child_process');
router.post('/', function(req, res) {
  const scriptPath = 'test.py'
  const process = spawn('python', [scriptPath, req.body.resume])
  var category;
  process.stdout.on('data', function (data) {
    console.log('Pipe data from python script ...');
    category = data.toString();
  });

  process.stderr.on('data', function (data) {
    console.error(data.toString());
  })
  // in close event we are sure that stream from child process is closed
  process.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);
    // send data to browser
    res.render('index', { result: category, resume: req.body.resume })
  });
})

module.exports = router;
