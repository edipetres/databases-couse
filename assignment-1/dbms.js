module.exports = (function () {
  const fs = require('fs')
  const path = require('path')
  const readline = require('readline')
  const stream = require('stream')
  
  let dbFileName = 'database.txt'
  let _separator = ':'
  let _delimiter = '\n'

  let indexMap = new Map()

  function _getIndexMap () {
    return indexMap
  }

  function _setIndexMap (incomingIndexMap) {
    indexMap = incomingIndexMap
  }
  
  function _indexDatabase(done) {
    // return early if already indexed
    if (_getIndexMap().size > 0) {
      return done()
    }
    // load index from file if exists
    _readIndexMapFromDisk(err => {
      // if file reading was successful end indexing
      if (!err) { 
        return done()
      }

      console.log('Indexing database...')
      let dbContent = fs.readFileSync(path.join(__dirname, dbFileName)).toString()
    
      // set up buffer stream for reading lines
      var buffer = new Buffer(dbContent)
      var bufferStream = new stream.PassThrough()
      bufferStream.end(buffer)
      var lineReader = readline.createInterface({
        input: bufferStream
      })
      // read lines one by one
      lineReader.on('line', line => {
        let key = line.split(':')[0]
        let value = dbContent.lastIndexOf(line)
        indexMap.set(key, value)
      })
      // trigger event when finished reading lines
      lineReader.addListener('close', () => {
        console.log('Done indexing.')
        return done()
      })
    })
  }
  
  function write (key, value) {
    let line = key + _separator + value + _delimiter
    fs.appendFile('database.txt', line, (err) => {
      if (err) {
        throw err
      }
      console.log('Saved.')
    })
  }
  
  function read (key, callback) {
    _indexDatabase(() => {
      let indexMap = _getIndexMap()
      let buf = fs.readFileSync(dbFileName, 'utf-8')
      // get the bit offset for the key from our index hashmap
      let keyIndex = indexMap.get(key)
      if (!keyIndex) {
        console.log('Key not found in index map.')
        return callback()
      }
      let eolIndex = buf.indexOf('\n') + 1
      let keyValue = buf.substr(keyIndex, eolIndex).toString()
      let value =  keyValue.split(_separator)[1]
      return callback(value)
    })
  }
  
  function _populateDatabase () {
    for (let index = 0; index < 20; index++) {
      write(index, Math.random().toString(36).substring(7))
    }
  }

  function _saveIndexMapToDisk () {
    let indexMap = _getIndexMap()
    let keys = indexMap.keys()
    let indexMapString = ''
    for (let key of keys) {
      indexMapString += key + _separator + indexMap.get(key) + _delimiter
    }
    fs.writeFileSync('indexMap', indexMapString)
    console.log('Done writing indexMap into file.')
  }

  function _readIndexMapFromDisk (done) {
    try {
      let indexMapString = fs.readFileSync(path.join(__dirname, 'indexMap'), 'utf-8').toString()
      let lines = indexMapString.split(_delimiter)
      let indexMap = new Map()
      lines.map(line => {
        let keyValue = line.split(_separator)
        let key = keyValue[0]
        let value = keyValue[1]
        indexMap.set(key, value)
      })
      _setIndexMap(indexMap)
      console.log('Done reading index map from file.')
      return done()
    }
    catch (err) {
      return console.log('Cannot find index map file on disk.')
    }
  }

  let test = "13"
  read(test, (value) => {
    console.log(`value for ${test}:`, value)
    _saveIndexMapToDisk()
  })

  return {
    read, 
    write
  }


})()
