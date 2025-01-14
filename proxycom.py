import time
from logger import logger_vcc, read_config_ini, set_config_ini
import serial
import threading
import win32com.client
import pythoncom

forwarding_thread = None
listing_status = 0

def start_port_forwarding(input_com_port, output_com_port, baud_rate, stop_event):
    config = read_config_ini("config.ini")
    cr = int(config.get("device", "cr", fallback="0"))
    lf = int(config.get("device", "lf", fallback="0"))
    # Определяем символ конца строки на основе значений cr и lf
    line_endings = {
        (1, 1): b'\r\n',
        (1, 0): b'\r',
        (0, 1): b'\n',
        (0, 0): b''
    }
    try:
        logger_vcc.info(f"Открываем порты: '{input_com_port}' и '{output_com_port}'...")
        # Открываем входной и выходной COM-порты
        input_ser = serial.Serial(input_com_port, baud_rate, timeout=0.1)
        if input_ser:
            logger_vcc.info(f"Порт '{input_com_port}' открыт")
            try:
                # Открываем входной и выходной COM-порты
                output_ser = serial.Serial(output_com_port, baud_rate, timeout=0.1)
                if output_ser:
                    logger_vcc.info(f"Порт '{output_com_port}' открыт")
            except Exception:
                logger_vcc.error(f"Ошибка при попытке открыть порт: {output_com_port}", exc_info=True)
    except Exception:
        logger_vcc.error(f"Ошибка при попытке открыть порт: {input_com_port}", exc_info=True)

    try:
        while not stop_event.is_set():  # Добавлена проверка флага stop_event
            config = read_config_ini("config.ini")
            timeout_clearcash = float(config.get("service", "timeout_clearcash", fallback="1.5"))

            output_ser.write_timeout = timeout_clearcash  # Tайм-аут записи в 2 секунды
            input_ser.write_timeout = timeout_clearcash
            ending = line_endings.get((cr, lf), b'')

            if input_ser.in_waiting > 0:  # Проверяем, есть ли данные для чтения
                data = input_ser.readall()  # Читаем строку
                logger_vcc.info(f"На порт '{input_com_port}' получены данные: {data}")
                # Пересылаем данные на выходной COM-порт
                try:
                    output_ser.write(data + ending)
                except serial.SerialTimeoutException:
                    logger_vcc.warning(f"Нет слушателя на порту '{output_com_port}'. Данные отброшены.")
            if output_ser.in_waiting > 0:  # Проверяем, есть ли данные для чтения
                data = output_ser.readall()  # Читаем строку
                logger_vcc.info(f"На порт '{output_com_port}' получены данные: {data}")
                # Пересылаем данные на выходной COM-порт
                try:
                    input_ser.write(data + ending)
                except serial.SerialTimeoutException:
                    logger_vcc.warning(f"Нет слушателя на порту '{input_com_port}'. Данные отброшены.")
            time.sleep(0.01)
    except UnboundLocalError:
        pass
    except Exception:
        logger_vcc.error(f"Произошла ошибка при попытке установить связь между портами '{input_com_port}' и '{output_com_port}'.", exc_info=True)
    finally:
        try:
            input_ser.close()  # Закрываем входной COM-порт
            logger_vcc.info(f"Порт '{input_com_port}' освобожден")
        except UnboundLocalError:
            pass
        except Exception:
            logger_vcc.error(f"Не удалось освободить порт: '{input_com_port}'", exc_info=True)
        try:
            output_ser.close()  # Закрываем выходной COM-порт
            logger_vcc.info(f"Порт '{output_com_port}' освобожден")
        except UnboundLocalError:
            pass
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
        if thread.is_alive() and listing_status !=1:
            listing_status = 1
        elif not thread.is_alive() and listing_status !=0:
            listing_status = 0
    except:
        pass

def start_listen_port(stop_event):
    try:
        global forwarding_thread
        config = read_config_ini("config.ini")
        # Настройки COM-портов
        input_com_port = config.get("device", "input_port", fallback=None)
        output_com_port = config.get("device", "output_port", fallback=None)
        baud_rate = config.get("device", "port_baudrate", fallback="9600")

        forwarding_thread = threading.Thread(target=start_port_forwarding, args=(input_com_port, output_com_port, baud_rate, stop_event), daemon=True)

        # Запуск прослушивания в отдельном потоке
        forwarding_thread.start()
    except Exception:
        logger_vcc.error(f"Не удалось запустить отдельный поток на прослушивание com-портов.", exc_info=True)

def status_forwarding_thread():
    try:
        def check_teard():
            while True:
                check_thread_status(forwarding_thread)
                time.sleep(0.5)

        check_teard = threading.Thread(target=check_teard)
        # Запуск прослушивания в отдельном потоке
        check_teard.start()
    except Exception:
        logger_vcc.error(f"Не удалось запустить отдельный поток на проверку статуса подключения к устройству.", exc_info=True)

def get_ports_from_wmi_by_partial_id(device_id, chars_to_remove):
    device_id_partial = device_id[:-chars_to_remove] if chars_to_remove > 0 else device_id
    ports = []
    try:
        # Инициализируем COM для текущего потока
        pythoncom.CoInitialize()
        # Создаем WMI объект
        wmi = win32com.client.Dispatch("WbemScripting.SWbemLocator")
        wmi_service = wmi.ConnectServer(".", "root\\cimv2")
        logger_vcc.info(f"Поиск устройства с ID, содержащим '{device_id_partial}'")

        # Выполняем запрос WMI для получения информации о всех PnP устройствах
        query = "SELECT * FROM Win32_PnPEntity"
        devices = wmi_service.ExecQuery(query)

        # Проверяем каждый PnP объект на соответствие заданной подстроке в PNPDeviceID
        for device in devices:
            if device_id_partial in device.PNPDeviceID:
                # Извлекаем и добавляем номер COM-порта из Caption, если он есть
                caption = device.Caption
                if "COM" in caption:
                    port_name = caption.split("(")[-1].split(")")[0]
                    logger_vcc.info(f"Найдено устройство. ID:'{device.PNPDeviceID}'. Порт:'{port_name}'.")
                    ports.append(port_name)
        if not ports:
            logger_vcc.warning(f"Устройства с ID, содержащим '{device_id_partial}', не найдены")
        return ports
    except Exception:
        logger_vcc.error(f"Не удалось получить номера COM-портов для ID, содержащего '{device_id_partial}'", exc_info=True)
    finally:
        pythoncom.CoUninitialize()

def update_port_device():
    config = read_config_ini("config.ini")
    input_com_port = config.get("device", "input_port", fallback=None)
    device_id = config.get("device", "device_id", fallback=None)
    chars_to_remove = int(config.get("service", "amount_rm_char_id", fallback="0"))

    if device_id != "":
        device_com_port = get_ports_from_wmi_by_partial_id(device_id, chars_to_remove)
        if device_com_port and device_com_port[0] != input_com_port:
            set_config_ini("config.ini", "device", "input_port", device_com_port[0])
