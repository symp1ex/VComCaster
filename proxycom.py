import time
from logger import logger_vcc, read_config_ini
import serial
import threading
import os

forwarding_thread = None
listing_status = 0

def start_port_forwarding(input_com_port, output_com_port, baud_rate, stop_event):
    logger_vcc.info(f"Открываем порты: '{input_com_port}' и '{output_com_port}'...")
    try:
        # Открываем входной и выходной COM-порты
        input_ser = serial.Serial(input_com_port, baud_rate, timeout=0.1)
    except Exception:
        logger_vcc.error(f"Ошибка при попытке открыть порт {e}: {input_com_port}", exc_info=True)
    if input_ser:
        logger_vcc.info(f"Порт '{input_com_port}'открыт")

    try:
        # Открываем входной и выходной COM-порты
        output_ser = serial.Serial(output_com_port, baud_rate, timeout=0.1)
    except Exception:
        logger_vcc.error(f"Ошибка при попытке открыть порт: {output_com_port}", exc_info=True)
    if output_ser :
        logger_vcc.info(f"Порт '{output_com_port}'открыт")

    try:
        while not stop_event.is_set():  # Добавлена проверка флага stop_event
            if input_ser.in_waiting > 0:  # Проверяем, есть ли данные для чтения
                data = input_ser.readline().decode('utf-8').rstrip()  # Читаем строку
                logger_vcc.info(f"На вход получены данные: {data}")

                # Пересылаем данные на выходной COM-порт
                output_ser.write((data + '\r\n').encode('utf-8'))  # Отправляем данные
            #     time.sleep(0.01)
            # if output_ser.in_waiting > 0:  # Проверяем, есть ли данные для чтения
            #     data = output_ser.readline().decode('utf-8').rstrip()  # Читаем строку
            #     log_console_out(f"На вход получены данные: {data}", "vcc")
            #
            #     # Пересылаем данные на выходной COM-порт
            #     input_ser.write((data + '\r\n').encode('utf-8'))  # Отправляем данные
            else:
                time.sleep(0.01)
    finally:
        try:
            input_ser.close()  # Закрываем входной COM-порт
            logger_vcc.info(f"Порт '{input_com_port}' освобожден")
        except Exception:
            logger_vcc.error(f"Не удалось освободить порт: '{input_com_port}'", exc_info=True)
        try:
            output_ser.close()  # Закрываем выходной COM-порт
            logger_vcc.info(f"Порт '{output_com_port}' освобожден")
        except Exception:
            logger_vcc.error(f"Не удалось освободить порт: '{output_com_port}'", exc_info=True)




def stop_port_forwarding(stop_event):
    """
    Функция для остановки прослушивания COM-порта, устанавливая флаг завершения.

    :param stop_event: Объект threading.Event для остановки потока.
    """
    logger_vcc.info("Остановка прослушивания COM-портов...")
    stop_event.set()
    time.sleep(2)

def check_thread_status(thread):
    global listing_status
    try:
        if thread.is_alive():
            listing_status = 1
        else:
            listing_status = 0
    except:
        pass

def start_listen_port(stop_event):
    global forwarding_thread
    config = read_config_ini("config.ini")
    # Настройки COM-портов
    input_com_port = config.get("device", "input_port", fallback=None)
    output_com_port = config.get("device", "output_port", fallback=None)
    baud_rate = config.get("device", "port_baudrate", fallback=None)

    forwarding_thread = threading.Thread(target=start_port_forwarding, args=(input_com_port, output_com_port, baud_rate, stop_event), daemon=True)

    # Запуск прослушивания в отдельном потоке
    forwarding_thread.start()

def status_forwarding_thread():
    def check_teard():
        while True:
            check_thread_status(forwarding_thread)
            time.sleep(0.5)

    check_teard = threading.Thread(target=check_teard)

    # Запуск прослушивания в отдельном потоке
    check_teard.start()