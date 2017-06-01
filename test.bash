
install_reqs () {
for f in `cat $1/requirements.txt`
do
	pip3 install -U ./$f

	install_reqs $f
done
}

make

echo $1

source venv/bin/activate

install_reqs $1

pip3 install -U ./$1

python3 -m unittest $1.tests -v

