const express = require('express')
const app = express()
const path = require('path')
const bodyParser = require('body-parser')
const childProcess = require('child_process')
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
  var sanitized_seed = req.query.seed.replace(/\W/g, '')

  try {
    childProcess.execFileSync('python', ['./src/main.py', sanitized_seed])
  } catch (err) {
    res.render('pages/under_construction')
  }

  res.render('pages/view_song', {
    seed : sanitized_seed
  })
})
// app.get('/generated_songs', (req, res) => res.send('generated_songs'))
app.use('/generated_songs', express.static('public/generated_songs'));

app.listen(PORT, () => console.log(`Example app listening on port ${PORT}!`))