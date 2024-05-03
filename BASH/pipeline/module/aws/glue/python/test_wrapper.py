#Test wrapper
import sys, logging
import teradatasql
from awsglue.utils import getResolvedOptions
import boto3
import time
from connector import TdvConnector
from logger import ScriptLogger

ACTION = "testing"
logger = ScriptLogger("tdv_to_s3_extract_broker_commissions_sircon_pshell").get_logger(action = ACTION)
TDV_CONN_WAIT_TIMES = [2**i for i in range(5, 9)]
args = getResolvedOptions(sys.argv, ['region_name', 'host', 'tdv_env', 'username', 'tdv_secretsmanager'])

region_name = args['region_name']
tdv_user = args['username']
tdv_secretsmanager = args['tdv_secretsmanager']
tdv_host = args['host']
oss_env = args['tdv_env']

def initialize_connection():
    session = boto3.session.Session()
    logger.info("Client session established")
    tdvconn_obj = TdvConnector(tdv_host, tdv_user, region_name, session, logger, tdv_secretsmanager)
    logger.info("TDV connector object instantiated")

    return tdvconn_obj.connect()

def retry_connection():
    tdv_conn = None

    for delay in TDV_CONN_WAIT_TIMES:
        try:
            logger.info(f"Waiting for {delay} seconds before attempting another connection")
            time.sleep(delay)
            tdv_conn = initialize_connection()
        except Exception as error:
            logger.error(f"Error in TDV connection retry: {error}")
        else:
            break

    return tdv_conn

def get_connection():

    tdv_conn = None

    try:
        tdv_conn = initialize_connection()
    except Exception as error:
        logger.error(f"Error in TDV connection: {error}. Retrying connection...")
        tdv_conn = retry_connection()       
        
    if tdv_conn is None:
        raise Exception("TDV connection not established")

    return tdv_conn


def main():
    logger.info("tdv host: %s" % tdv_host)
    logger.info("tdv env: %s" % oss_env)
    logger.info("Main execution ...")
    tdvconn = get_connection()
    tdvconn.close()

if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        raise err