var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: '',
                        resume: '',
                        result1: '',
                        result2: '',
                        result3: '',
                        result4: '',
                        result5: '' });
});

router.use(express.urlencoded());
router.use(express.json());

/* POST to get screening result */
const {spawn} = require('child_process');
router.post('/', function(req, res) {
  const scriptPath = 'resume_screener.py'
  const process = spawn('python', [scriptPath, req.body.resume])
  var category;
  process.stdout.on('data', function (data) {
    console.log('Pipe data from python script ...');
    category = data.toString();
    category = category.split(/[\r\n]+/)
    console.log(category)
  });

  process.stderr.on('data', function (data) {
    console.error(data.toString());
  })
  // in close event we are sure that stream from child process is closed
  process.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);
    // send data to browser
    res.render('index', { title: 'Top 5 Results',
                          resume: req.body.resume,
                          result1: category[0],
                          result2: category[1],
                          result3: category[2],
                          result4: category[3],
                          result5: category[4] })
  });
})

module.exports = router;
