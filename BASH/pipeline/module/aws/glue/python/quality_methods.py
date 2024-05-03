# libs
import pyspark.sql.functions as F

##############################################
# Methods used to evaluate data quality
# Input is a spark df and output is a spark df
##############################################
class QualityMethods:
    def __init__(self, spark_df, col_types, test_date):
        self.spark_df = spark_df
        self.col_types = col_types
        self.test_date = test_date
    @classmethod
    def quality_formats(cls, spark_df, col_types, test_date):

        # get list of df_cols
        df_cols = spark_df.columns

        # regexes can be updated/ customized
        date_regex_pcs = "^(?:(?:19|20)[0-9]{2})[-](0[1-9]|1[012])[-](0[1-9]|[12][0-9]|3[01])$"  # pcs
        date_regex_evolve = "^(?:(?:19|20)[0-9]{2})(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])$"  # evolve memE
        number_regex = "^[0-9]+$"
        number_letter_regex = "^[a-zA-Z0-9]+$"
        src_member_regex = "^[0-9]+_[0-9]+$"
        gender_regex = "^[M|F]$"
        phone_regex = "^[0-9]{7}$"

        # transform col_type list to list of regexes for each col
        col_types_regex = list(map(lambda x: date_regex_pcs if x == "date_pcs" else
                                    (number_regex if x == "number" else
                                        (src_member_regex if x == "src_member" else
                                            (number_letter_regex if x == "number_letter" else
                                             (gender_regex if x == "gender" else
                                              (phone_regex if x == "phone" else
                                               date_regex_evolve))))), col_types))

        # create tuple to associate the correct regex with each col -- instead of leaving it as 2 lists.
        # This ensures the col name and regex stay together.
        col_tuple = tuple(map(lambda x, y: (x, y), df_cols, col_types_regex))

        # iterate through each column
        result_format_df = spark_df
        for i in range(len(df_cols)):
            result_format_df = result_format_df.withColumn(col_tuple[i][0] + "_fmt",
                                                           F.col(col_tuple[i][0]).rlike(col_tuple[i][1]))

         # add cols for testing for dupes and adding test date
        result_format_df = result_format_df \
            .join(spark_df.groupBy(spark_df.columns).agg((F.count("*") > 1).cast("int").alias("dupe")), on=spark_df.columns,
                  how="left") \
            .withColumn("test_date", F.lit(test_date))
        return result_format_df

    @classmethod
    def quality_general_stats(cls,spark_df, test_date):
        """ Perform quality check -- general stats"""
        df_cols = spark_df.columns  # list object

        # no of nulls per col
        null_ct = spark_df.agg(*[F.count(F.when(F.isnull(c), c)).alias(c) for c in df_cols]) \
            .withColumn("stat", F.lit("ct_null")) \
            .withColumn("test_date", F.lit(test_date))

        # no of rows populated per col
        row_ct = spark_df.agg(*[F.count(c).alias(c) for c in df_cols]) \
            .withColumn("stat", F.lit("ct_row")) \
            .withColumn("test_date", F.lit(test_date))

        # no of distinct values per col
        distinct_ct = spark_df.agg(*[F.countDistinct(c).alias(c) for c in df_cols]) \
            .withColumn("stat", F.lit("ct_distinct")) \
            .withColumn("test_date", F.lit(test_date))

        # max value per col
        max_val = spark_df.agg(*[F.max(c).alias(c) for c in df_cols]) \
            .withColumn("stat", F.lit("max")) \
            .withColumn("test_date", F.lit(test_date))

        # min value per col
        min_val = spark_df.agg(*[F.min(c).alias(c) for c in df_cols]) \
            .withColumn("stat", F.lit("min")) \
            .withColumn("test_date", F.lit(test_date))

        result_general = row_ct.union(distinct_ct).union(null_ct).union(max_val).union(min_val)
        return result_general