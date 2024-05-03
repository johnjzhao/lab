import unittest
from unittest import TestCase

# from Cigna.gov-solutions.gov-solutions-commissions.module.aws.glue.python.tdv_to_s3_dataextract_mem_dim_pshell import get_connection
from tdv_to_s3_dataextract_mem_dim_pshell import retry, get_connection



class TestExample(TestCase):
    def test_logging(self):
        with self.assertLogs() as captured:
            get_connection()
            retry()
          
        self.assertEqual(len(captured.records), 2) # check that there is only two log message
        self.assertEqual(captured.records[0].getMessage(), "Connection Succeded!") # and it is the proper one





if __name__ == '__main__':
    unittest.main()