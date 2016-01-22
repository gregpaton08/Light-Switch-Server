import ls_server
import unittest


class LSServerTestCase(unittest.TestCase):

    def setUp(self):
        self.app = ls_server.app.test_client()

    def tearDown():
        pass



if __name__ == '__main__':
    unittest.main()