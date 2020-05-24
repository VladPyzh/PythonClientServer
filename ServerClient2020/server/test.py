import unittest
import json
from my_server import change_status, storage_reader, read_mails
from json_writer import writter
from test_config import Test_strings


# important to check file on content before
writter()


class TestServer(unittest.TestCase):
    def test_read_mails(self):
        self.assertEqual(read_mails(Test_strings.test_id), Test_strings.lost)
        self.assertEqual(read_mails(Test_strings.test_id), Test_strings.nothing)
        self.assertEqual(read_mails(Test_strings.dont_exist), Test_strings.nothing)

    def test_storage_reader(self):
        try:
            storage_reader()
        except Exception as ex:
            self.fail(Test_strings.raised_by_storage.format(ex))

    def test_change_status(self):
        self.assertEqual(change_status(Test_strings.test_item, Test_strings.trash), False)
        self.assertEqual(change_status(Test_strings.test_item, Test_strings.test_id), True)
        with open("statuses.txt", "r") as f:
            statuses = json.loads(f.read())
            self.assertEqual(123, statuses[Test_strings.test_item])
