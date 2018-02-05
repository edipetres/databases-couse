module.exports = (function () {
  const fs = require('fs')
  const path = require('path')
  const readline = require('readline')
  const stream = require('stream')
  
  let _dbFilename = 'js_database'
  let _separator = ':'
  let _delimiter = '\n'

  let indexMap = new Map()

  function _getIndexMap () {
    return indexMap
  }

  function _setIndexMap (incomingIndexMap) {
    indexMap = incomingIndexMap
  }

  function write (key, value) {
    let line = key + _separator + value + _delimiter
    fs.appendFile(_dbFilename, line, (err) => {
      if (err) {
        throw err
      }
      _updateIndex(key, line)
    })
  }
  
  function read (key, callback) {
    _indexDatabase(() => {
      let buf = fs.readFileSync(_dbFilename, 'utf-8')
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
  
  function _indexDatabase(done) {
    // return early if index already exists
    if (indexMap.size > 0) {
      return done()
    }
    // load index from file if exists
    _readIndexMapFromDisk(err => {
      // if file reading was successful end indexing
      if (!err) { 
        return done()
      }
      // no index file found. Do indexing...
      console.log('Indexing database...')
      let dbContent = fs.readFileSync(path.join(__dirname, _dbFilename)).toString()
    
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

  function _updateIndex(key, line) {
    let dbContent = fs.readFileSync(_dbFilename, 'utf-8').toString()
    let indexValue = dbContent.lastIndexOf(line)
    console.log('adding to index:', key, indexValue)
    indexMap.set(key, indexValue)
    _saveIndexMapToDisk()
  }
  
  function _saveIndexMapToDisk () {
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
  
  function _populateDatabase () {
    for (let index = 0; index < 20; index++) {
      write(index, Math.random().toString(36).substring(7))
    }
  }

  return {
    read, 
    write
  }

})()
