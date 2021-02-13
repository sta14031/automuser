const express = require('express')
const app = express()
const path = require('path')
const bodyParser = require('body-parser')
const PORT = process.env.PORT || 7000

app.use(express.static(path.join(__dirname, 'public')))
// Body parser stuff
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({extended: false }));
app.set('views', path.join(__dirname, 'views'))
app.set('view engine', 'ejs')
app.get('/', (req, res) => res.render('pages/index'))
app.get('/about', (req, res) => res.render('pages/about'))
app.get('/song', (req, res) => {
    let seed = req.query.seed

    res.render('pages/view_song')
})

function sendToPython() {
  var python = require('child_process').spawn('python', ['./src/main.py', input.value]);
  python.stdout.on('data', function (data) {
    console.log("Python response: ", data.toString('utf8'));
    result.textContent = data.toString('utf8');
  });

  python.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  python.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
  });

}

app.listen(PORT, () => console.log(`Example app listening on port ${PORT}!`))