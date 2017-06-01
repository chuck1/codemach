
files_codemach=$(shell find codemach -regex ".*\.\(py\)")
files_modconf=$(shell find modconf -regex ".*\.\(py\)")
files_ws_sheets=$(shell find ws_sheets -regex ".*\.\(py\)")
files_ws_sheets_server=$(shell find ws_sheets_server -regex ".*\.\(py\|service\)")
files_ws_web_aiohttp=$(shell find ws_web_aiohttp -regex ".*\.\(py\|service\|html\)")

output  = modconf
output += codemach
output += ws_web_aiohttp

all: modconf codemach ws_sheets ws_sheets_server $(output)

modconf: modconf/VERSION.txt

codemach: codemach/VERSION.txt

ws_storage: ws_storage/VERSION.txt

ws_sheets: ws_sheets/VERSION.txt

ws_sheets_server: ws_sheets_server/VERSION.txt

ws_web_aiohttp: ws_web_aiohttp/VERSION.txt

whl_cmd=pip3 wheel --wheel-dir=package_index --find-links=package_index

codemach/VERSION.txt: $(files_codemach)
	python3 increment_build_number.py codemach
	#$(whl_cmd) ./codemach

modconf/VERSION.txt: $(files_modconf)
	python3 increment_build_number.py modconf
	#$(whl_cmd) ./modconf

ws_sheets/VERSION.txt: $(files_ws_sheets) modconf codemach
	python3 increment_build_number.py ws_sheets
	#$(whl_cmd) ./ws_sheets

ws_sheets_server/VERSION.txt: $(files_sheets_server) modconf codemach ws_sheets
	python3 increment_build_number.py ws_sheets_server
	#$(whl_cmd) ./ws_sheets_server

ws_web_aiohttp/VERSION.txt: $(files_ws_web_aiohttp) modconf codemach ws_sheets
	python3 increment_build_number.py ws_web_aiohttp
	#$(whl_cmd) ./ws_web_aiohttp


