import unittest
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession


class PySparkTestSession(unittest.TestCase):
    """Local spark session for testing"""

    @classmethod
    def setUpClass(cls):
        cls.spark = (SparkSession
                     .builder
                     .appName("PySpark unit test")
                     .getOrCreate())

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()


def test_data(df1: DataFrame, df2: DataFrame):
    """Compares data in two DataFrames. Returns true if equal.
        df1: result dataframe
        df2: expected dataframe
        return: boolean """
    data1 = df1.collect()
    data2 = df2.collect()
    return set(data1) == set(data2)