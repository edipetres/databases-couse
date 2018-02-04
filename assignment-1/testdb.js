const dbms = require('./dbms')

dbms.write('age', '28')
dbms.write('year', '2018')

setTimeout(() => {
  dbms.read('age', value => {
    console.log('RETURN:', value)
  })
  
}, 1000);
