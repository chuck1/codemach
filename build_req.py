
import jinja2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('dir')

args = parser.parse_args()

def read_version(d):
    with open(os.path.join(d, 'VERSION.txt')) as f:
        return f.read()

context = {
        'sheets_version': read_version('sheets_pkg'),
        }

import jinja2
with open(os.path.join(args.dir, 'templates', 'requirements.txt')) as f:
    template = jinja2.Template(f.read())

with open(os.path.join(args.dir, 'requirements.txt')) as f:
    f.write(template.render(context))

