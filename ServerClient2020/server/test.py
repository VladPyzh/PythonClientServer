import unittest
import json
from my_server import change_status, storage_reader, read_mails
from json_writer import writter


# important to check file on content before
writter()


class TestServer(unittest.TestCase):
    def test_read_mails(self):
        self.assertEqual(read_mails("123"), "Sorry, we lost your order. \u00af\\_(\u30c4)_/\u00af")
        self.assertEqual(read_mails("123"), "nothing")
        self.assertEqual(read_mails("NOT_EXISTING_AT_ALL"), "nothing")

    def test_storage_reader(self):
        try:
            storage_reader()
        except Exception as ex:
            self.fail("storage_reader() raised {}".format(ex))

    def test_change_status(self):
        self.assertEqual(change_status("Test", "asdasdfasdf"), False)
        self.assertEqual(change_status("Test", "123"), True)
        with open("statuses.txt", "r") as f:
            statuses = json.loads(f.read())
            self.assertEqual(123, statuses["Test"])
