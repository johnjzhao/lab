import json
import logging
import os
import sys
import boto3
from typing import List
from configparser import ConfigParser, NoOptionError, NoSectionError

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s - %(levelname)s - %(name)s:%(lineno)s - %(funcName)s ] - %(message)s')
handler.setFormatter(formatter)

lib_logger = logging.getLogger(f"GlueLogs-{__name__}")
lib_logger.setLevel(logging.INFO)
lib_logger.addHandler(handler)
lib_logger.info(f"Logger Initialized for the {__name__} module.")

class GlueConfigParser(object):
    def __init__(self):
        self.parser = ConfigParser()

    def read_conf(self, conf_file, runtime=None):
        """
        Function to read config file
        :param runtime:
        :param conf_file:
        :return:
        """
        if runtime == 'pythonshell':
            for r, d, f in os.walk('.'):
                for files in f:
                    if files == conf_file:
                        abs_path = os.path.abspath(os.path.join(r, files))
                        lib_logger.info(f"File found in local filesystem, absolute path: {f}")
            self.parser.read(abs_path)
        else:
            self.parser.read(conf_file)

    def conf_get(self, sec, key=None):
        """
        This method is used to fetch the values from config file. Requires
        cls.conf_file variable.
        :param sec: Section name
        :param key: Key name
        :return: value from config
        """
        try:
            if key:
                value = self.parser.get(sec, key)
            else:
                value = self.parser.sections()
            return value
        except NoOptionError:
            lib_logger.warning(f"No options found for Section: {sec}, Key: {key}.")
            return None
        except NoSectionError:
            lib_logger.warning(
                f"The section, {sec}, was not found in the configuration file.")
            return None


class GlueUtilities(object):
    conf_file = None
    parser = ConfigParser()

    def __init__(self):
        pass

    @classmethod
    def initialize_logger(cls, runtime: str, logger_name: str):
        """
        This function will configure s logging object with basic configurations.
        :param runtime:
        :param logger_name:
        :return:
        """
        if runtime == 'pythonshell':
            lib_logger.info('Initializing logger for python shell runtime.')
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                '[%(asctime)s - %(levelname)s - %(name)s:%(lineno)s - %(funcName)s ] - %(message)s')
            handler.setFormatter(formatter)

            root = logging.getLogger(logger_name)
            root.setLevel(logging.INFO)
            root.addHandler(handler)
            root.info('Root logger initialized.')
        elif runtime == 'spark':
            lib_logger.info('Initializing logger for PySpark runtime.')
            logging.basicConfig(
                level=logging.INFO,
                format='[%(asctime)s - %(levelname)s - %(name)s:%(lineno)s - %(funcName)s ] - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            root = logging.getLogger(logger_name)
            root.info('Root logger initialized.')
        else:
            raise Exception('Please specify either pythonshell or spark for the runtime.')

        return root

    @classmethod
    def split_queries(cls, file: str, delimiter: str):
        """
        Split sql file into individual queries.
        :param file:
        :param delimiter:
        :return: list of queries
        """
        lib_logger.info(
            f"Finding queries in file delimited by {delimiter}: {file}")
        queries = file.split(delimiter) if file else []
        lib_logger.info(f"Found {len(queries)} queries: {queries}")
        return queries

    @classmethod
    def prep_copy_command(cls, iam_role: str, csv_bucket: str, csv_folder: str,
                          manifest_file_name: str, columns: List[str],
                          schema: str, tbl: str) -> str:
        """
        Prepares a copy command to load data from S3 to target Redshift table. Column list is parsed using ddlparser.
        :param iam_role:
        :param csv_bucket:
        :param csv_folder:
        :param manifest_file_name:
        :param columns:
        :param schema:
        :param tbl:
        :return:
        """
        col_str = ','.join(columns)
        lib_logger.info(f"Columns: {col_str} ")
        copy_cmd = f"copy {schema}.{tbl}(" + col_str + ") "
        manifest_path = f"from 's3://{csv_bucket}/{csv_folder}/{manifest_file_name}' "
        # TODO: Suggesting that the copy configuration should be a parameter to offer flexibility when calling this function.
        copy_config = f"iam_role '{iam_role}'  dateformat 'auto' manifest  csv COMPUPDATE ON TRUNCATECOLUMNS;"
        copy_command = copy_cmd + manifest_path + copy_config
        return copy_command

    @classmethod
    def prep_copy_command_computeoff(cls, iam_role: str, csv_bucket: str, csv_folder: str,
                          manifest_file_name: str, columns: List[str],
                          schema: str, tbl: str) -> str:
        """
        Prepares a copy command to load data from S3 to target Redshift table. Column list is parsed using ddlparser.
        :param iam_role:
        :param csv_bucket:
        :param csv_folder:
        :param manifest_file_name:
        :param columns:
        :param schema:
        :param tbl:
        :return:
        """
        col_str = ','.join(columns)
        lib_logger.info(f"Columns: {col_str} ")
        copy_cmd = f"copy {schema}.{tbl}(" + col_str + ") "
        manifest_path = f"from 's3://{csv_bucket}/{csv_folder}/{manifest_file_name}' "
        # TODO: Suggesting that the copy configuration should be a parameter to offer flexibility when calling this function.
        copy_config = f"iam_role '{iam_role}'  dateformat 'auto' manifest  csv COMPUPDATE OFF TRUNCATECOLUMNS;"
        copy_command = copy_cmd + manifest_path + copy_config
        return copy_command

    @classmethod
    def prep_unload_command(cls, iam_role: str, csv_bucket: str, csv_folder: str,
                            date_folder: str, schema: str, tbl: str, aws_lck: str,
                            unload_filter: str = '', unload_parameters: str = '') -> str:
        """
        Prepares an unload command to unload records as a CSV into an S3 bucket.
        :param iam_role:
        :param csv_bucket:
        :param csv_folder:
        :param date_folder:
        :param schema:
        :param tbl:
        :param aws_lck:
        :param unload_filter:
        :param unload_parameters:
        :return:
        """
        unload_cmd = f"unload ('select * from {schema}.{tbl} {unload_filter}')"
        csv_archive_path = f"s3://{csv_bucket}/{csv_folder}/{date_folder}/{aws_lck}/"
        unload_config = f" to '{csv_archive_path}' iam_role '{iam_role}' {unload_parameters}"
        unload_command = unload_cmd + unload_config
        return unload_command

    @classmethod
    def publish_metrics(cls, metrics_bucket: str, aws_lck: str, step_id: int, payload: dict):
        """
        Used to upload a json containing data load metrics to an S3 bucket.
        :param metrics_bucket:
        :param aws_lck:
        :param step_id:
        :param payload:
        :return:
        """
        lib_logger.info('Sending metrics to ABC Process')
        bucket = metrics_bucket
        file = str(aws_lck) + str(step_id) + '.json'
        lib_logger.info(f"Writing metrics to S3 bucket: {bucket}, file: {file}")
        client = boto3.client('s3', verify=False, region_name='us-east-1')

        lib_logger.info(f"Payload: {payload}")
        response = client.put_object(Body=json.dumps(payload),
                                     Bucket=bucket, Key=file)
        lib_logger.info(f"Response: {response}")
        status = response['ResponseMetadata']['HTTPStatusCode']
        if status != 200:
            msg = 'Failed to create metrics s3 file'
            raise Exception(msg)


def get_glue_runner() -> str:
    """
    Parses glue job role for database user name to connect to Redshift.
    :return: etlrole: DB User to be used to connect to Redshift.
    """
    client = boto3.client('sts')
    response = client.get_caller_identity()
    arn = response['Arn']
    etlrole = arn.split("/")[1].lower()
    return etlrole


def fetch_file_path(file_name: str) -> str:
    """
    Fetches the absolute path of a file attached to python shell Glue jobs.
    :param file_name:
    :return:
    """
    abs_path = None
    for r, d, f in os.walk('.'):
        for files in f:
            if files == file_name:
                abs_path = os.path.abspath(os.path.join(r, files))
                lib_logger.info(f"Absolute path of the file {abs_path}")

    return abs_path
    