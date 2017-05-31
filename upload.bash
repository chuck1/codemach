#!/bin/bash
python3 setup.py bdist_wheel
for f in dist/*.whl; do twine upload $f || echo "Failed to upload $f"; done
