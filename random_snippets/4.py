import os
import logging
import logging.handlers
import zipfile
import datetime

from conf import LOGS_DIRECTORY, LOGS_BACKUP_DIRECTORY


def setup_logger(name, level=logging.INFO):
    log_file = os.path.join('logs/', f'{name}.log')

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    handler = logging.handlers.TimedRotatingFileHandler(
        log_file, when="midnight", interval=1, backupCount=7)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


LOGGER = setup_logger('main_log', level=logging.INFO)
DEBT_LOGGER = setup_logger('debt_log', level=logging.INFO)
CALL_LOGGER = setup_logger('call_log', level=logging.INFO)
LOADING_LOGGER = setup_logger('loading_log', level=logging.INFO)


backup_performed_today = False


def recreate_deleted_log_files(deleted_log_files):
    for log_file in deleted_log_files:
        file_path = os.path.join(LOGS_DIRECTORY, log_file)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                pass


def backup_logs():
    global backup_performed_today
    if not backup_performed_today:

        current_date = datetime.datetime.now().strftime('%Y-%m-%d')

        zip_file_name = f'{LOGS_BACKUP_DIRECTORY}/{current_date}.zip'

        log_files = [f for f in os.listdir(LOGS_DIRECTORY) if f.endswith('.log')]

        with zipfile.ZipFile(zip_file_name, 'w') as zipf:
            for log_file in log_files:
                file_path = os.path.join(LOGS_DIRECTORY, log_file)
                if os.path.exists(file_path):
                    zipf.write(file_path, os.path.basename(file_path))
                    os.remove(file_path)

        recreate_deleted_log_files(log_files)

        backup_performed_today = True
