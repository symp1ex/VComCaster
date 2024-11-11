import os
import sys
import traceback
from datetime import datetime, timedelta
import configparser

version = "VComCaster v0.2.4.10"

def create_confgi_ini():
    try:
        # Создание объекта парсера
        config = configparser.ConfigParser()

        # Создание секций
        config['global'] = {}
        config['device'] = {}

        # Запись значения в секцию и ключ
        config['global']['autostart'] = '0'
        config['global']['logs-autoclear-days'] = '7'
        config['device']['input_port'] = ''
        config['device']['output_port'] = ''
        config['device']['port_baudrate'] = ''
        config['device']['device_id'] = ''
        config['device']['timeout_reconnect'] = '10'

        # Запись изменений в файл
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

        log_console_out("Создан 'config.ini' по умолчанию", "vcc")
    except Exception as e:
        log_console_out("Error: Не удалось пересоздать 'config.ini', продолжение работы невозможно.", "vcc")
        exception_handler(type(e), e, e.__traceback__, "vcc")
        os._exit(1)

def read_config_ini(ini_file):
    try:
        config = configparser.ConfigParser()
        config.read(ini_file)
        return config
    except FileNotFoundError:
        log_console_out("Error: 'config.ini' не найден, будет создан новый конфиг.", "vcc")
        create_confgi_ini()
    except Exception as e:
        log_console_out("Error: Произошло исключение при чтении 'config.ini', будет создан новый конфиг.", "vcc")
        exception_handler(type(e), e, e.__traceback__, "vcc")
        create_confgi_ini()

def log_with_timestamp(message, name):
    try:
        ini_file = "config.ini"
        config = read_config_ini(ini_file)

        log_folder = 'logs'
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)

        # Получаем текущую дату
        current_date = datetime.now()

        days = int(config.get("global", "logs-autoclear-days", fallback=7))
        # Определяем дату, старше которой логи будут удаляться
        old_date_limit = current_date - timedelta(days=days)

        # Удаляем логи старше 14 дней
        for file_name in os.listdir(log_folder):
            file_path = os.path.join(log_folder, file_name)
            file_creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
            if file_creation_time < old_date_limit:
                os.remove(file_path)

        timestamp = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(log_folder, f"{timestamp}-{name}.log")
        default_stdout = sys.stdout
        sys.stdout = open(log_file, 'a')

        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S.%f")[:-3]+"]"
        print(f"{timestamp} {message}")
        sys.stdout.close()
        sys.stdout = default_stdout
    except:
        pass


def log_console_out(message, name):
    try:
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S.%f")[:-3]+"]"
        print(f"{timestamp} {message}")
        log_with_timestamp(message, name)
    except:
        pass
    
    
def exception_handler(exc_type, exc_value, exc_traceback, name):
    try:
        error_message = f"ERROR: An exception occurred + \n"
        error_message += ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        log_with_timestamp(error_message, name)
        # Вызываем стандартный обработчик исключений для вывода на экран
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
    except:
        pass

def exception_handler_console_out(exc_type, exc_value, exc_traceback, name):
    try:
        error_message = f"ERROR: An exception occurred + \n"
        error_message += ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        log_console_out(error_message, name)
        # Вызываем стандартный обработчик исключений для вывода на экран
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
    except:
        pass