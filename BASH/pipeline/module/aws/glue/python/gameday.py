from logger import ScriptLogger

logger = ScriptLogger("gameday").get_logger(action = "testing")

if __name__ == "__main__":
    logger.exception("Raising Gameday Glue Job Failure")
    raise Exception("Glue Job Failure")