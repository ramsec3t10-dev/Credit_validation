import os,sys
from Credit_validation.logging.logger import logging


class CreditDataException(Exception):
    def __init__(self,error_message,error_details:sys):
        self.error_message = error_message
        _,_,exc_tb = error_details.exc_info()
        self.lineno = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return "error occurred in python script [{0}] line no [{1}] error message [{2}]".format(self.file_name,self.lineno,str(self.error_message))
    
if __name__ == "__main__":
    try:
        logging.info("exception error check")
        a=1/0
        print("This out will not be printed",a)
    except Exception as e:
        raise CreditDataException(e,sys)

        