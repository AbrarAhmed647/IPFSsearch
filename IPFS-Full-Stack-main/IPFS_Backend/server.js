require('dotenv').config()
const express = require('express')
const bodyParser = require('body-parser')
const app = express()
const cors = require('cors')
const corsOptions = require('./config/corsOptions')
const path = require('path')
const { logger, logEvents } = require('./middleware/logger')
const errorHandler = require('./middleware/errorHandler')
const PORT = process.env.PORT || 3500

console.log(process.env.NODE_ENV)
app.use(logger)
app.use(cors(corsOptions))
app.use(express.json())

app.use('/', require('./routes/root'))
app.use('/files', require('./routes/filesRoutes'))
app.use('/testAPI', require('./routes/testAPI'))

app.all('*', (req, res) => {
    res.status(404)
    if (req.accepts('html')) {
        res.sendFile(path.join(__dirname, 'views', '404.html'))
    } else if (req.accepts('json')) {
        res.json({ message: '404 Not Found' })
    } else {
        res.type('txt').send('404 Not Found')
    }
})

app.listen(PORT, () => console.log(`Server running on port ${PORT}`))