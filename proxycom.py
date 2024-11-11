import time
from logger import log_console_out, exception_handler, read_config_ini
import serial
import threading
import os

forwarding_thread = None
icon_status = 0

def start_port_forwarding(input_com_port, output_com_port, baud_rate, stop_event):
    log_console_out(f"Открываем порты: '{input_com_port}' и '{output_com_port}'...", "vcc")
    try:
        # Открываем входной и выходной COM-порты
        input_ser = serial.Serial(input_com_port, baud_rate, timeout=0.1)
    except Exception as e:
        log_console_out(f"Error: Ошибка при попытке открыть порт: {input_com_port}", "vcc")
        exception_handler(type(e), e, e.__traceback__, "vcc")
    if input_ser:
        log_console_out(f"Порт '{input_com_port}'открыт", "vcc")

    try:
        # Открываем входной и выходной COM-порты
        output_ser = serial.Serial(output_com_port, baud_rate, timeout=0.1)
    except Exception as e:
        log_console_out(f"Error: Ошибка при попытке открыть порт: {output_com_port}", "vcc")
        exception_handler(type(e), e, e.__traceback__, "vcc")
    if output_ser :
        log_console_out(f"Порт '{output_com_port}'открыт", "vcc")

    try:
        while not stop_event.is_set():  # Добавлена проверка флага stop_event
            if input_ser.in_waiting > 0:  # Проверяем, есть ли данные для чтения
                data = input_ser.readline().decode('utf-8').rstrip()  # Читаем строку
                log_console_out(f"На вход получены данные: {data}", "vcc")

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
            log_console_out(f"Порт '{input_com_port}' освобожден", "vcc")
        except Exception as e:
            log_console_out(f"Error: Не удалось освободить порт: '{input_com_port}'", "vcc")
            exception_handler(type(e), e, e.__traceback__, "vcc")
        try:
            output_ser.close()  # Закрываем выходной COM-порт
            log_console_out(f"Порт '{output_com_port}' освобожден", "vcc")
        except Exception as e:
            log_console_out(f"Error: Не удалось освободить порт: '{output_com_port}'", "vcc")
            exception_handler(type(e), e, e.__traceback__, "vcc")




def stop_port_forwarding(stop_event):
    """
    Функция для остановки прослушивания COM-порта, устанавливая флаг завершения.

    :param stop_event: Объект threading.Event для остановки потока.
    """
    log_console_out("Остановка прослушивания COM-портов...", "vcc")
    stop_event.set()
    time.sleep(2)

def check_thread_status(thread):
    global icon_status
    try:
        if thread.is_alive():
            icon_status = 1
        else:
            icon_status = 0
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
            time.sleep(1)

    check_teard = threading.Thread(target=check_teard)

    # Запуск прослушивания в отдельном потоке
    check_teard.start()
