
files_codemach=$(shell find codemach -regex ".*\.\(py\)")
files_modconf=$(shell find modconf -regex ".*\.\(py\)")
files_ws_sheets=$(shell find ws_sheets -regex ".*\.\(py\)")
files_sheets_compute=$(shell find sheets_backend_pkg -regex ".*\.\(py\|service\)")

all: modconf codemach

modconf: modconf/VERSION.txt

codemach: codemach/VERSION.txt

ws_sheets: ws_sheets/VERSION.txt

whl_cmd=pip3 wheel --wheel-dir=package_index --find-links=package_index

codemach/VERSION.txt: $(files_codemach)
	python3 increment_build_number.py codemach
	$(whl_cmd) ./codemach

modconf/VERSION.txt: $(files_modconf)
	python3 increment_build_number.py modconf
	$(whl_cmd) ./modconf

ws_sheets/VERSION.txt: $(files_ws_sheets) modconf codemach
	python3 increment_build_number.py ws_sheets
	$(whl_cmd) ./ws_sheets

sheets_backend_pkg/VERSION.txt: $(files_sheets_compute) modconf sheets
	python3 increment_build_number.py sheets_backend_pkg
	$(whl_cmd) ./sheets_backend_pkg


