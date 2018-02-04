require 'gdbm'

gdbm = GDBM.new('fruitstore.db')
gdbm['ananas'] = '3'
gdbm['banana'] = '8'
gdbm['cranberry'] = '4909'
gdbm['ananas'] = '42'
gdbm.close