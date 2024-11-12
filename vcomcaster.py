#0.2.5.3
from logger import logger_vcc, read_config_ini, version
from icon import icon_data_start, icon_data_stop
from proxycom import start_listen_port, stop_port_forwarding, status_forwarding_thread
from winsettings import init_win_settings
from winterminal import win_terminal
import time
import pystray
import io, os, sys, ctypes
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading

stop_event = threading.Event()
icon = None  # Глобальная переменная для иконки

# Функция для обработки первого пункта меню
def reconnetion_action():
    config = read_config_ini("config.ini")
    timeout = int(config.get("device", "timeout_reconnect", fallback=None))

    from proxycom import listing_status
    if listing_status == 1:
        stop_port_forwarding(stop_event)

    logger_vcc.info(f"Повторное подключение через ({timeout}) секунд")
    stop_event.clear()
    threading.Timer(timeout, start_listen_port, args=(stop_event,)).start()


def stop_listing():
    from proxycom import listing_status
    if listing_status == 0:
        root = tk.Toplevel()
        root.wm_attributes('-alpha', 0) # Делаем окно полностью прозрачным
        root.withdraw()  # Скрываем окно до установки иконки

        stop_icon_image = Image.open(io.BytesIO(icon_data_stop))
        stop_icon_image_tk = ImageTk.PhotoImage(stop_icon_image)

        # Устанавливаем иконку для окна подтверждения
        root.stop_icon_image = stop_icon_image_tk
        root.iconphoto(False, stop_icon_image_tk)

        tk.messagebox.showerror("Ошибка", "Прослушивание портов не запущено", parent=root)
        logger_vcc.error(f"Прослушивание портов не запущено")
    else:
        stop_port_forwarding(stop_event)
        time.sleep(3)
        stop_event.clear()


# Функция для обработки второго пункта меню
def open_settings():
    init_win_settings()


# Функция для выхода из программы
def exit_action(icon):
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
        stop_port_forwarding(stop_event)
        time.sleep(5)
        icon.stop()  # Останавливаем иконку в трее
        root.quit()  # Закрываем окно подтверждения
        os._exit(0)
    else:
        root.destroy()

# Функция для создания иконки
def setup_icon_tray():
    global icon  # Используем глобальную переменную для иконки
    config = read_config_ini("config.ini")

    autostart_listing = int(config.get("app", "autostart_listing", fallback=None))
    input_com_port = config.get("device", "input_port", fallback=None)
    output_com_port = config.get("device", "output_port", fallback=None)

    if autostart_listing == True:
        # Преобразуем бинарные данные для иконки
        icon_image = Image.open(io.BytesIO(icon_data_start))
    else:
        icon_image = Image.open(io.BytesIO(icon_data_stop))

    # Создаём меню
    menu = pystray.Menu(
        pystray.MenuItem("Переподключиться", reconnetion_action),
        pystray.MenuItem("Стоп", stop_listing),
        pystray.MenuItem("Окно терминала", win_terminal),
        pystray.MenuItem("Настройки", open_settings),
        pystray.MenuItem("Выход", exit_action)
    )

    # Создаём иконку и добавляем подсказку (tooltip) при наведении
    icon = pystray.Icon("icon", icon_image, menu=menu, title=f"{version} \nПрослушиваются порты: {input_com_port}, {output_com_port}")  # Подсказка при наведении


# Функция для запуска tkinter в отдельном потоке
def run_tkinter():
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно
    root.mainloop()

def check_listing_status():
    status_forwarding_thread()
    def swap_icon():
        up = None
        while True:
            from proxycom import listing_status
            if listing_status == 0 and up != 0:
                icon.icon = Image.open(io.BytesIO(icon_data_stop))
                up = 0
            elif listing_status == 1 and up != 1:
                icon.icon = Image.open(io.BytesIO(icon_data_start))
                up =1
            time.sleep(2)

    swap_icon = threading.Thread(target=swap_icon)
    swap_icon.start()

# Запускаем иконку и tkinter в отдельных потоках
if __name__ == "__main__":
    config = read_config_ini("config.ini")
    autostart_listing = int(config.get("app", "autostart_listing", fallback=None))

    # Запускаем tkinter в отдельном потоке
    tkinter_thread = threading.Thread(target=run_tkinter, daemon=True)
    tkinter_thread.start()

    setup_icon_tray()  # Создаем иконку
    if autostart_listing == True:
        start_listen_port(stop_event)
    check_listing_status()
    icon.run()