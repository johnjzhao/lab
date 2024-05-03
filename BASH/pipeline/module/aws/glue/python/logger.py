import logging, sys, re, os
from logging.handlers import RotatingFileHandler

LOG_OUTPUT_DIR = "logs/"
class ScriptLogger(logging.Logger):
    def __init__(self, logger_class):
        self.class_name = __name__
        self.logger_class_name = logger_class

    def get_logger(self, lob=None, action=None):
        try:  
            logger = logging.getLogger(self.logger_class_name)
            logger.propagate = False
            adapter = logging.LoggerAdapter(logger, {"LOB":lob, "Action":action})
            adapter.setLevel(logging.INFO)

            formatter = CustomFormatter(
                '{"timestamp": "%(asctime)s.%(msecs)03d", "level": "%(levelname)s", "lob": "%(LOB)s", "action": "%(Action)s", "function": "%(name)s.%(funcName)s:%(lineno)d", "message": "%(message)s"}', 
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setFormatter(formatter)
            
            self.__check_directory()
            file_handler = RotatingFileHandler(filename=f"{LOG_OUTPUT_DIR}{self.logger_class_name}.log", maxBytes=3000000, backupCount=20)
            file_handler.setFormatter(formatter)
            
            logger.handlers = [stream_handler, file_handler]
            return adapter
        except Exception as error:
            print("Could not get logger")
            raise error
        
    def __check_directory(self):
        if not os.path.exists(LOG_OUTPUT_DIR):
            os.makedirs(LOG_OUTPUT_DIR)
      
class CustomFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        arg_pattern = re.compile(r'%\((\w+)\)')
        arg_names = [x.group(1) for x in arg_pattern.finditer(self._fmt)]
        for field in arg_names:
            if field not in record.__dict__:
                record.__dict__[field] = ""

        return super().format(record)