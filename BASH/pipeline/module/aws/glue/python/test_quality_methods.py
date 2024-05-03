import pyspark.sql.types as T
from quality_methods import QualityMethods
from pyspark_test_utils import PySparkTestSession, test_data


class TestQualityGeneral(PySparkTestSession):

    def test_general_stats_null(self):
        input_df = self.spark.createDataFrame([
            (909444, "apple", "orange", 450222333, 20220453),
            (304985, "grapefruit", "pear", None, 3837676),
            (None, "red", "blue", 987777, None)],
            ['col1', 'col2', 'col3', 'col4', 'col5'])
        test_date = '20231205'

        expected_null = self.spark.createDataFrame(
            data=[
                (1, 0, 0, 1, 1, 'ct_null', '20231205')
            ],
            schema=T.StructType([
                T.StructField('col1', T.IntegerType(), False),
                T.StructField('col2', T.StringType(), False),
                T.StructField('col3', T.StringType(), False),
                T.StructField('col4', T.IntegerType(), False),
                T.StructField('col5', T.IntegerType(), False),
                T.StructField('stat', T.StringType(), False),
                T.StructField('test_date', T.StringType(), False),
                ])
        )

        result = QualityMethods.quality_general_stats(input_df, test_date)
        result_null = result.where("stat=='ct_null'") \
            .withColumn("col1", result.col1.cast(T.IntegerType())) \
            .withColumn("col4", result.col4.cast(T.IntegerType())) \
            .withColumn("col5", result.col5.cast(T.IntegerType()))

        self.assertTrue(test_data(result_null, expected_null))
        # pandas_expected_null = expected_null.toPandas()
        # pandas_result_null = result_null.toPandas()
        # can use assert_frame_equal instead of naming new test_data method

    def test_general_stats_rows(self):
        input_df = self.spark.createDataFrame([
            (909444, "apple", "orange", 450222333, 20220453),
            (304985, "grapefruit", "pear", None, 3837676),
            (None, "red", "blue", 987777, None)],
            ['col1', 'col2', 'col3', 'col4', 'col5'])
        test_date = '20231205'
        expected_row = self.spark.createDataFrame(
            data=[
                (2, 3, 3, 2, 2, 'ct_row', '20231205')
            ],
            schema=T.StructType([
                T.StructField('col1', T.IntegerType(), False),
                T.StructField('col2', T.IntegerType(), False),
                T.StructField('col3', T.IntegerType(), False),
                T.StructField('col4', T.IntegerType(), False),
                T.StructField('col5', T.IntegerType(), False),
                T.StructField('stat', T.StringType(), False),
                T.StructField('test_date', T.StringType(), False),
            ])
        )

        result = QualityMethods.quality_general_stats(input_df, test_date)
        result_row = result.where("stat=='ct_row'") \
                            .withColumn("col1", result.col1.cast(T.IntegerType())) \
                            .withColumn("col2", result.col2.cast(T.IntegerType())) \
                            .withColumn("col3", result.col3.cast(T.IntegerType())) \
                            .withColumn("col4", result.col4.cast(T.IntegerType())) \
                            .withColumn("col5", result.col5.cast(T.IntegerType()))
        self.assertTrue(test_data(result_row, expected_row))

    def test_general_stats_distinct(self):
        input_df = self.spark.createDataFrame([
            (909444, "apple", "orange", 450222333, 20220453),
            (304985, "grapefruit", "pear", None, 3837676),
            (None, "red", "blue", 987777, None)],
            ['col1', 'col2', 'col3', 'col4', 'col5'])
        test_date = '20231205'
        expected_distinct = self.spark.createDataFrame(
            data=[
                (2, 3, 3, 2, 2, 'ct_distinct', '20231205')
            ],
            schema=T.StructType([
                T.StructField('col1', T.IntegerType(), False),
                T.StructField('col2', T.IntegerType(), False),
                T.StructField('col3', T.IntegerType(), False),
                T.StructField('col4', T.IntegerType(), False),
                T.StructField('col5', T.IntegerType(), False),
                T.StructField('stat', T.StringType(), False),
                T.StructField('test_date', T.StringType(), False),
            ])
        )

        result = QualityMethods.quality_general_stats(input_df, test_date)
        result_distinct = result.where("stat=='ct_distinct'") \
            .withColumn("col1", result.col1.cast(T.IntegerType())) \
            .withColumn("col2", result.col2.cast(T.IntegerType())) \
            .withColumn("col3", result.col3.cast(T.IntegerType())) \
            .withColumn("col4", result.col4.cast(T.IntegerType())) \
            .withColumn("col5", result.col5.cast(T.IntegerType()))

        self.assertTrue(test_data(result_distinct, expected_distinct))

    def test_general_stats_max(self):
        input_df = self.spark.createDataFrame([
            (909444, "apple", "orange", 450222333, 20220453),
            (304985, "grapefruit", "pear", None, 3837676),
            (None, "red", "blue", 987777, None)],
            ['col1', 'col2', 'col3', 'col4', 'col5'])
        test_date = '20231205'
        expected_max = self.spark.createDataFrame(
            data=[
                (909444, 'red', 'pear', 450222333, 20220453, 'max', '20231205')
            ],
            schema=T.StructType([
                T.StructField('col1', T.IntegerType(), False),
                T.StructField('col2', T.StringType(), False),
                T.StructField('col3', T.StringType(), False),
                T.StructField('col4', T.IntegerType(), False),
                T.StructField('col5', T.IntegerType(), False),
                T.StructField('stat', T.StringType(), False),
                T.StructField('test_date', T.StringType(), False),
            ])
        )

        result = QualityMethods.quality_general_stats(input_df, test_date)
        result_max = result.where("stat=='max'") \
            .withColumn("col1", result.col1.cast(T.IntegerType())) \
            .withColumn("col4", result.col4.cast(T.IntegerType())) \
            .withColumn("col5", result.col5.cast(T.IntegerType()))

        self.assertTrue(test_data(result_max, expected_max))

    def test_general_stats_min(self):
        input_df = self.spark.createDataFrame([
            (909444, "apple", "orange", 450222333, 20220453),
            (304985, "grapefruit", "pear", None, 3837676),
            (None, "red", "blue", 987777, None)],
            ['col1', 'col2', 'col3', 'col4', 'col5'])
        test_date = '20231205'
        expected_min = self.spark.createDataFrame(
            data=[
                (304985, 'apple', 'blue', 987777, 3837676, 'min', '20231205')
            ],
            schema=T.StructType([
                T.StructField('col1', T.IntegerType(), False),
                T.StructField('col2', T.StringType(), False),
                T.StructField('col3', T.StringType(), False),
                T.StructField('col4', T.IntegerType(), False),
                T.StructField('col5', T.IntegerType(), False),
                T.StructField('stat', T.StringType(), False),
                T.StructField('test_date', T.StringType(), False),
            ])
        )

        result = QualityMethods.quality_general_stats(input_df, test_date)
        result_min = result.where("stat=='min'") \
            .withColumn("col1", result.col1.cast(T.IntegerType())) \
            .withColumn("col4", result.col4.cast(T.IntegerType())) \
            .withColumn("col5", result.col5.cast(T.IntegerType()))

        self.assertTrue(test_data(result_min, expected_min))

    def test_formats_true(self):
        input_df = self.spark.createDataFrame([
            (909444, "apple23", "222_222", "F", "255dd", "20221208", "2023-02-15", 5558942323)],
            ['number', 'number_letter', 'src_member', 'gender', 'number2', 'date_evolve', 'date_pcs', 'phone'])
        test_date = '20231205'
        col_types = ["number", "number_letter", "src_member", "gender", "number", "date_evolve", "date_pcs", "phone"]
        expected_formats = self.spark.createDataFrame(
            data=[
                (909444, "apple23", "222_222", "F", "255dd", "20221208", "2023-02-15", 5558942323, True, True, True,
                 True, False, True, True, True, 0, "20231205")],
            schema=T.StructType([
                T.StructField('number', T.IntegerType(), False),
                T.StructField('number_letter', T.StringType(), False),
                T.StructField('src_member', T.StringType(), False),
                T.StructField('gender', T.StringType(), False),
                T.StructField('number', T.StringType(), False),
                T.StructField('date_evolve', T.StringType(), False),
                T.StructField('date_pcs', T.StringType(), False),
                T.StructField('phone', T.LongType(), False),
                T.StructField('number_fmt', T.BooleanType(), False),
                T.StructField('number_letter_fmt', T.BooleanType(), False),
                T.StructField('src_member_fmt', T.BooleanType(), False),
                T.StructField('gender_fmt', T.BooleanType(), False),
                T.StructField('number2_fmt', T.BooleanType(), False),
                T.StructField('date_evolve_fmt', T.BooleanType(), False),
                T.StructField('date_pcs_fmt', T.BooleanType(), False),
                T.StructField('phone_fmt', T.BooleanType(), False),
                T.StructField('dupe', T.IntegerType(), False),
                T.StructField('test_date', T.StringType(), False)
            ])
        )
        expected_formats.show()

        result = QualityMethods.quality_formats(input_df, col_types, test_date)
        result.show()

        self.assertTrue(test_data(result, expected_formats))
    def test_formats_false_dupe(self):
        input_df = self.spark.createDataFrame([
            ("abc123", 6333, "2100_", 90, 58999, "17002123", "2023/02/15", 265454),
            ("abc123", 6333, "2100_", 90, 58999, "17002123", "2023/02/15", 265454)],
            ['number', 'number_letter', 'src_member', 'gender', 'number2', 'date_evolve', 'date_pcs', 'phone'])
        test_date = '20231205'
        col_types = ["number", "number_letter", "src_member", "gender", "number", "date_evolve", "date_pcs", "phone"]
        expected_formats = self.spark.createDataFrame(
            data=[
                ("abc123", 6333, "2100_", 90, 58999, "17002123", "2023/02/15", 265454, False, True, False,
                 False, True, False, False, False, 1, "20231205"),
                ("abc123", 6333, "2100_", 90, 58999, "17002123", "2023/02/15", 265454, False, True, False,
                 False, True, False, False, False, 1, "20231205")],
            schema=T.StructType([
                T.StructField('number', T.StringType(), False),
                T.StructField('number_letter', T.IntegerType(), False),
                T.StructField('src_member', T.StringType(), False),
                T.StructField('gender', T.IntegerType(), False),
                T.StructField('number', T.IntegerType(), False),
                T.StructField('date_evolve', T.StringType(), False),
                T.StructField('date_pcs', T.StringType(), False),
                T.StructField('phone', T.IntegerType(), False),
                T.StructField('number_fmt', T.BooleanType(), False),
                T.StructField('number_letter_fmt', T.BooleanType(), False),
                T.StructField('src_member_fmt', T.BooleanType(), False),
                T.StructField('gender_fmt', T.BooleanType(), False),
                T.StructField('number2_fmt', T.BooleanType(), False),
                T.StructField('date_evolve_fmt', T.BooleanType(), False),
                T.StructField('date_pcs_fmt', T.BooleanType(), False),
                T.StructField('phone_fmt', T.BooleanType(), False),
                T.StructField('dupe', T.IntegerType(), False),
                T.StructField('test_date', T.StringType(), False)
            ])
        )
        expected_formats.show()

        result = QualityMethods.quality_formats(input_df, col_types, test_date)
        result.show()

        self.assertTrue(test_data(result, expected_formats))