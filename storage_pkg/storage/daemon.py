
import logging
import logging.config

import storage.filesystem

def test():
    sys.path.insert(0, '/etc/web_sheets_storage')
    settings_module = __import__('web_sheets_storage.settings', fromlist=['*'])

    logging.config.dictConfig(settings_module.LOGGING)

    port = settings_module.PORT

    logging.config.dictConfig()

    port = settings.get('port',10001)

def daemon():
    logger = logging.getLogger(__name__)
    try:
        test()
    except Exception as e:
        logger.exception(str(e))



