import unittest
import ws_web_aiohttp


class TestWebServer(unittest.TestCase):
    def test(self):
        ws_web_aiohttp.main(('','ws_web_aiohttp.tests.conf.simple'))



