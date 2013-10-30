import os
import runner
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, runner.app.config['SQLITE_APPDB_PATH'] = tempfile.mkstemp()
        runner.app.config['TESTING'] = True
        self.app = runner.app.test_client()
        runner.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(runner.app.config['SQLITE_APPDB_PATH'])

    def test_test(self):
        rv=self.app.get('/')
        assert tables in rv.data

if __name__ == '__main__':
    unittest.main()
