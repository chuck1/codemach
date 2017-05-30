import os
import jinja2

BASE_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

def do_install():
    
    def input_(prompt, default):
        s = input(prompt + '[' + default + ']')
        if not s:
            return default
        return s
    
    print(__name__)
    print('base dir:', BASE_DIR)
    print('template dir:', TEMPLATE_DIR)
    print('package:', __package__)

    env = jinja2.Environment(
            loader=jinja2.PackageLoader(__package__, 'templates'))
    
    template = env.get_template('service.service')
    
    
    
    script_name = input_(
            'name of script:'.format(__package__),
            'web_sheets_' + __package__ + '.py')
    
    base,_ = os.path.splitext(script_name)

    service_name = input_(
            'name of service:'.format(__package__),
            base + '.service')

    user = input_(
            'user for service:',
            base)
    
    conf = input_(
            'modconf directory:',
            '/etc/' + base)
    
    text = template.render(
            user=user,
            script_name=script_name,
            conf=conf)
    
    print(text)
    
if __name__ == '__main__':
    do_install()
    
