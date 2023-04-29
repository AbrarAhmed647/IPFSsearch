const express = require('express')
const router = express.Router()
const filesController = require('../controllers/filesController')

router.route('/')
    .get(filesController.getAllFilesByNameAndCID)
    .post(filesController.sendSelectedFilesContent)

module.exports = router