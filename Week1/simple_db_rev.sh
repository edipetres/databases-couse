db_set () {
	echo "$1,$2" >> database
}
db_get () {
	grep "^$1," database | sed -t "s/^$1,//" | tail -n 1
}
