require 'gdbm'

gdbm = GDBM.new('fruitstore.db')
gdbm.each_pair do |key, value|
    print "#{key}: #{value}\n"
end
gdbm.close