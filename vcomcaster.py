from logger import logger_vcc, read_config_ini
from icon import icon_data_start, icon_data_stop
from proxycom import start_listen_port, stop_port_forwarding, status_forwarding_thread, update_port_device
from winsettings import WinSettingsUi
from winterminal import WinTerminalUi
import about
import time
import pystray
import io
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading

stop_event = threading.Event()
icon = None  # Глобальная переменная для иконки
stop_tag = 1

def set_stop_tag(value):
    global stop_tag
    stop_tag = value

# Функция для обработки первого пункта меню
def reconnetion_action():
    try:
        config = read_config_ini("config.ini")
        timeout = float(config.get("service", "timeout_reconnect", fallback="10"))

        global stop_tag
        from proxycom import listing_status
        if listing_status == 1:
            stop_tag = 1
            time.sleep(1) # или блокировать интерфейс на весь тайм-аут перед повтроным запуском прослушивания?
            stop_port_forwarding(stop_event)
            logger_vcc.info(f"Повторное подключение через ({timeout}) секунд")
            stop_event.clear()
            threading.Timer(timeout, start_listen_port, args=(stop_event,)).start()
            threading.Timer(timeout + 1, lambda: set_stop_tag(0)).start()
        else:
            update_port_device()
            start_listen_port(stop_event)
            time.sleep(1)
            stop_tag = 0
    except Exception:
        logger_vcc.error(f"Не удалось инициировать переподключение к устройству.",
                         exc_info=True)

def reconnetion_auto():
    try:
        while True:
            config = read_config_ini("config.ini")
            autoreconnect = int(config.get("app", "autoreconnect", fallback="0"))
            timeout = float(config.get("service", "timeout_autoreconnect", fallback="10"))

            if autoreconnect == 1:
                from proxycom import listing_status
                if listing_status == 0 and stop_tag != 1:
                    stop_port_forwarding(stop_event)
                    logger_vcc.info(f"Повторное подключение через ({timeout}) секунд")
                    stop_event.clear()
                    time.sleep(timeout)
                    update_port_device()
                    time.sleep(1)
                    start_listen_port(stop_event)
            else:
                pass
            time.sleep(timeout)
    except Exception:
        logger_vcc.error(f"Не удалось запустить функцию автоматического переподключения к устройству.", exc_info=True)

def stop_listing():
    try:
        global stop_tag
        from proxycom import listing_status
        if listing_status == 0:
            stop_tag = 1
            message_error_box("Прослушивание портов не запущено")
            logger_vcc.error(f"Прослушивание портов не запущено")
        else:
            stop_tag = 1
            stop_port_forwarding(stop_event)
            time.sleep(2)
            stop_event.clear()
    except Exception:
        logger_vcc.error(f"Не удалось инициировать освобождение портов.",
                         exc_info=True)

# Функция для выхода из программы
def exit_action(icon):
    try:
        global stop_tag
        # Создаём дочернее окно подтверждения
        root = tk.Toplevel()
        root.wm_attributes('-alpha', 0) # Делаем окно полностью прозрачным
        root.withdraw()  # Скрываем окно до установки иконки

        # Загружаем иконку для окна
        stop_icon_image = Image.open(io.BytesIO(icon_data_stop))
        stop_icon_image_tk = ImageTk.PhotoImage(stop_icon_image)

        # Устанавливаем иконку для окна подтверждения
        root.stop_icon_image = stop_icon_image_tk
        root.iconphoto(False, stop_icon_image_tk)

        # Показать диалоговое окно подтверждения
        response = tk.messagebox.askyesno("Выход", "Вы уверены, что хотите выйти?", parent=root)

        if response:
            stop_tag = 1
            stop_port_forwarding(stop_event)
            time.sleep(2)
            icon.stop()  # Останавливаем иконку в трее
            root.quit()  # Закрываем окно подтверждения
            os._exit(0)
        else:
            root.destroy()
    except Exception:
        logger_vcc.critical(f"Не удалось инициализировать окно подтверждения закрытия приложения.", exc_info=True)
        os._exit(1)

def message_error_box(message):
    root = tk.Toplevel()
    root.wm_attributes('-alpha', 0)  # Делаем окно полностью прозрачным
    root.withdraw()  # Скрываем окно до установки иконки

    stop_icon_image = Image.open(io.BytesIO(icon_data_stop))
    stop_icon_image_tk = ImageTk.PhotoImage(stop_icon_image)

    # Устанавливаем иконку для окна подтверждения
    root.stop_icon_image = stop_icon_image_tk
    root.iconphoto(False, stop_icon_image_tk)

    # Захватываем все события ввода, чтобы сделать окно модальным
    root.grab_set()

    tk.messagebox.showerror("Ошибка", message, parent=root)

    # Освобождаем захват после закрытия окна сообщения
    root.grab_release()
    root.destroy()

# Функция для создания иконки
def setup_icon_tray():
    try:
        global icon
        config = read_config_ini("config.ini")
        autostart_listing = int(config.get("app", "autostart_listing", fallback="0"))

        if autostart_listing == True:
            icon_image = Image.open(io.BytesIO(icon_data_start))
        else:
            icon_image = Image.open(io.BytesIO(icon_data_stop))

        # Создаём основной пункт меню, который будет активироваться по левому клику
        settings_item = pystray.MenuItem(
            "Настройки",
            WinSettingsUi().init_win_settings,
            default=True  # Делаем этот пункт меню действием по умолчанию
        )

        # Создаём меню
        menu = pystray.Menu(
            settings_item,  # Добавляем пункт настроек первым
            pystray.MenuItem("Переподключиться", reconnetion_action),
            pystray.MenuItem("Стоп", stop_listing),
            pystray.MenuItem("Окно терминала", WinTerminalUi().init_win_terminal),
            pystray.MenuItem("Выход", exit_action)
        )

        # Создаём иконку
        icon = pystray.Icon(
            "icon",
            icon_image,
            menu=menu,
            title=f"{about.version}"
        )

    except Exception:
        logger_vcc.critical(f"Не удалось инициализировать основной интерфейс.", exc_info=True)
        os._exit(1)

# Функция для запуска tkinter в отдельном потоке
def run_tkinter():
    try:
        root = tk.Tk()
        root.withdraw()  # Скрываем основное окно
        root.mainloop()
    except Exception:
        logger_vcc.critical(f"Не удалось инициализировать основной интерфейс.", exc_info=True)
        os._exit(1)

def check_listing_status():
    status_forwarding_thread()
    try:
        def swap_icon():
            up = None
            while True:
                from proxycom import listing_status
                if listing_status == 0 and up != 0:
                    icon.icon = Image.open(io.BytesIO(icon_data_stop))
                    up = 0
                elif listing_status == 1 and up != 1:
                    icon.icon = Image.open(io.BytesIO(icon_data_start))
                    up = 1
                time.sleep(2)

        swap_icon = threading.Thread(target=swap_icon)
        swap_icon.start()
    except Exception:
        logger_vcc.error(f"Не удалось запустить отдельный поток на обновление иконки в системном трее.", exc_info=True)

# Запускаем иконку и tkinter в отдельных потоках
if __name__ == "__main__":
    config = read_config_ini("config.ini")
    autostart_listing = int(config.get("app", "autostart_listing", fallback="0"))

    # Запускаем tkinter в отдельном потоке
    tkinter_thread = threading.Thread(target=run_tkinter, daemon=True)
    tkinter_thread.start()

    reconnetion_auto = threading.Thread(target=reconnetion_auto, daemon=True)
    reconnetion_auto.start()

    setup_icon_tray()  # Создаем иконку
    if autostart_listing == True:
        start_listen_port(stop_event)
        stop_tag = 0
    check_listing_status()
    icon.run()
