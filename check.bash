
check () {
	for f in `find $1 -name "*.py"`
	do
		#stat $1/VERSION.txt
		if [ "$1/VERSION.txt" -ot "$f" ]
		then
			echo $f is older than $1/VERSION.txt

			python3 increment_build_number.py $1

			return 1
		fi
	done
	return 0
}

check myexecutor_pkg
check mysocket_pkg
check storage_pkg
check sheets_pkg
check sheets_backend_pkg


