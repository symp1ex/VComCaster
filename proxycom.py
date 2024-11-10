from logger import log_console_out, exception_handler, read_config_ini
import serial
import threading
import os


def start_port_forwarding(input_com_port, output_com_port, baud_rate, stop_event):
    try:
        # Открываем входной и выходной COM-порты
        input_ser = serial.Serial(input_com_port, baud_rate)
        output_ser = serial.Serial(output_com_port, baud_rate)
    except Exception as e:
        log_console_out(f"Error: Ошибка при попытке занять com-порты", "vcc")
        exception_handler(type(e), e, e.__traceback__, "vcc")


    log_console_out(f"Слушаем '{input_com_port}' и перенаправляем на '{output_com_port}'...", "vcc")
    try:
        while not stop_event.is_set():  # Добавлена проверка флага stop_event
            if input_ser.in_waiting > 0:  # Проверяем, есть ли данные для чтения
                data = input_ser.readline().decode('utf-8').rstrip()  # Читаем строку
                log_console_out(f"На вход получены данные: {data}", "vcc")

                # Пересылаем данные на выходной COM-порт
                output_ser.write((data + '\r\n').encode('utf-8'))  # Отправляем данные
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
    stop_event.set()
    log_console_out("Остановка прослушивания COM-портов...", "vcc")


def start_listen_port(stop_event):
    config = read_config_ini("config.ini")
    # Настройки COM-портов
    input_com_port = config.get("device", "input_port", fallback=None)
    output_com_port = config.get("device", "output_port", fallback=None)
    baud_rate = config.get("device", "port_baudrate", fallback=None)

    forwarding_thread = threading.Thread(target=start_port_forwarding, args=(input_com_port, output_com_port, baud_rate, stop_event))

    # Запуск прослушивания в отдельном потоке
    forwarding_thread.start()