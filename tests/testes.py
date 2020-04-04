import unittest
from rss import downloadRss
from rss import app
import unittest


class RssSenderTest(unittest.TestCase):

    def test_send(self):
        pass

    def test_downloadData(self):
        self.assertEqual(downloadRss()[0], "https://sourceforge.net/p/simplerss/news/feed", msg="ok")
