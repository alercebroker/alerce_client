import unittest
import os
from alerce.core import Alerce


class TestClientConfig(unittest.TestCase):
    def test_config_from_file_path(self):
        file_name = "test_config.json"
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, file_name)

        os.environ["ALERCE_CONFIG_PATH"] = file_path

        alerce_client = Alerce()
        print(alerce_client)

        # delete env variable after test
        del os.environ["ALERCE_CONFIG_PATH"]


if __name__ == "__main__":
    unittest.main()
