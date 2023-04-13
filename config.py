from dotenv import load_dotenv
import os
import logging

load_dotenv('.env')


try:
    DB_HOST = os.getenv('DB_HOST')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
except (TypeError, ValueError) as ex:
    logging.error("Error while reading config:", ex)
