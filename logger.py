import configparser, os, sys
import logging
import time
from logging.handlers import TimedRotatingFileHandler

version = "VComCaster v0.4.1.2"


def create_confgi_ini():
    try:
        # Создание объекта парсера
        config = configparser.ConfigParser()

        # Создание секций
        config['app'] = {}
        config['device'] = {}
        config['service'] = {}

        # Запись значения в секцию и ключ
        config['app']['autostart_listing'] = '0'
        config['app']['autoreconnect'] = '0'
        config['app']['logs-autoclear-days'] = '3'
        config['device']['device_id'] = ''
        config['device']['input_port'] = 'COM'
        config['device']['output_port'] = 'COM'
        config['device']['port_baudrate'] = '115200'
        config['device']['cr'] = '0'
        config['device']['lf'] = '0'
        config['service']['amount_rm_char_id'] = '0'
        config['service']['timeout_clearcash'] = '2'
        config['service']['timeout_autoreconnect'] = '5'
        config['service']['timeout_reconnect'] = '5'

        # Запись изменений в файл
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

        logger_vcc.info("Создан 'config.ini' по умолчанию")
    except Exception:
        logger_vcc.critical("Не удалось пересоздать 'config.ini', продолжение работы невозможно.", exc_info=True)
        time.sleep(2)
        os._exit(1)

def read_config_ini(ini_file):
    try:
        config = configparser.ConfigParser()
        config.read(ini_file)
        return config
    except FileNotFoundError:
        logger_vcc.warning("Файл'config.ini' не найден, будет создан новый конфиг.")
        create_confgi_ini()
    except Exception:
        logger_vcc.error("Произошло исключение при чтении 'config.ini', будет создан новый конфиг.", exc_info=True)
        create_confgi_ini()

def set_config_ini(ini_file, section, option, value):
    try:
        # Читаем текущий конфиг
        config = read_config_ini(ini_file)

        # Проверяем наличие секции, если нужно, добавляем ее
        if not config.has_section(section):
            config.add_section(section)

        # Устанавливаем новое значение
        config.set(section, option, value)

        # Сохраняем изменения в файл
        with open(ini_file, "w") as configfile:
            config.write(configfile)
        logger_vcc.info(f"Значение '{option}' в '{ini_file}' успешно обновлено на '{value}'.")
    except Exception:
        logger_vcc.error(f"Произошла ошибка при обновлении '{ini_file}'", exc_info=True)

class StdoutRedirectHandler(logging.StreamHandler):
    def __init__(self):
        # Вызываем StreamHandler с sys.stdout, если он определен, иначе используем None
        super().__init__(stream=sys.stdout if hasattr(sys, 'stdout') else None)

    def emit(self, record):
        # Проверяем, что sys.stdout все еще доступен
        if hasattr(sys, 'stdout') and sys.stdout:
            # Форматируем сообщение перед выводом
            msg = self.format(record)
            # Пишем сообщение в sys.stdout (перехватывается виджетом)
            sys.stdout.write(msg + '\n')


def logger(file_name, with_console=False):
    ini_file = "config.ini"
    config = read_config_ini(ini_file)
    days = int(config.get("app", "logs-autoclear-days"))

    log_folder = "logs"

    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Создаем логгер
    logger = logging.getLogger(file_name)
    logger.setLevel(logging.DEBUG)  # Устанавливаем уровень логирования

    # Проверяем, не был ли уже добавлен обработчик для этого логгера
    if not logger.hasHandlers():
        # Создаем обработчик для вывода в файл с ротацией
        file_handler = TimedRotatingFileHandler(
            f"{log_folder}\\{file_name}.log",
            when="D",         # Ротация раз в день
            interval=1,       # Интервал: 1 день
            backupCount=days,     # Хранить архивы не дольше 7 дней
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)

        # Форматтер для настройки формата сообщений
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        file_handler.setFormatter(formatter)

        # Добавляем обработчик к логгеру
        logger.addHandler(file_handler)

        # Добавляем обработчик для вывода на консоль
        if with_console:
            #console_handler = logging.StreamHandler() # вывод в стандартный обработчик бибилиотеки
            console_handler = StdoutRedirectHandler() # в системный вывод
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

    return logger

logger_vcc = logger(f"vcc", with_console=True)
logger_vcc_of = logger(f"vcc", with_console=False)



# logger.debug("сообщение отладки")
# logger.info("информационное сообщение")
# logger.warning("предупреждение")
# logger.error("ошибка")
# logger.critical("критическое сообщение")
#logger.error("Сообщение с включенным стеком", exc_info=True)
# logger.exception("стек исключений")
