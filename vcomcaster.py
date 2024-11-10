#0.1
from logger import log_console_out, exception_handler, read_config_ini
from icon import icon_data_start, icon_data_stop
from proxycom import start_listen_port, stop_port_forwarding
from winsettings import init_win_settings
import time
import pystray
import io, os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading

stop_event = threading.Event()

# Функция для обработки первого пункта меню
def reconnetion_action():
    config = read_config_ini("config.ini")
    timeout = int(config.get("device", "timeout_reconnect", fallback=None))

    stop_port_forwarding(stop_event)
    stop_event.clear()
    time.sleep(3)
    log_console_out(f"Повторное подключение через ({timeout}) секунд", "vcc")
    time.sleep(timeout)
    start_listen_port(stop_event)


# Функция для обработки второго пункта меню
def open_settings():
    init_win_settings()


# Функция для выхода из программы
def exit_action(icon):
    # Создаём дочернее окно подтверждения
    root = tk.Toplevel()
    root.withdraw()  # Скрываем окно до установки иконки

    # Загружаем иконку для окна
    stop_icon_image = Image.open(io.BytesIO(icon_data_stop))
    stop_icon_image_tk = ImageTk.PhotoImage(stop_icon_image)

    # Устанавливаем иконку для окна подтверждения
    root.stop_icon_image = stop_icon_image_tk
    root.iconphoto(False, stop_icon_image_tk)

    # Показать диалоговое окно подтверждения
    response = messagebox.askyesno("Выход", "Вы уверены, что хотите выйти?", parent=root)

    if response:
        icon.stop()  # Останавливаем иконку в трее
        root.quit()  # Закрываем окно подтверждения
        stop_port_forwarding(stop_event)
        stop_event.clear()
        time.sleep(3)
        os._exit(0)
    else:
        root.destroy()


# Функция для создания иконки
def setup_icon_tray():
    config = read_config_ini("config.ini")
    input_com_port = config.get("device", "input_port", fallback=None)

    # Преобразуем бинарные данные для иконки
    icon_image = Image.open(io.BytesIO(icon_data_start))

    # Создаём меню
    menu = pystray.Menu(
        pystray.MenuItem("Переподключиться", reconnetion_action),
        pystray.MenuItem("Настройки", open_settings),
        pystray.MenuItem("Выход", exit_action)
    )

    # Создаём иконку и добавляем подсказку (tooltip) при наведении
    icon = pystray.Icon("test_icon", icon_image, menu=menu, title=f"VComCaster v.0.1 \nПрослушивается порт: {input_com_port}")  # Подсказка при наведении
    icon.run()


# Функция для запуска tkinter в отдельном потоке
def run_tkinter():
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно
    root.mainloop()


# Запускаем иконку и tkinter в отдельных потоках
if __name__ == "__main__":
    # Запускаем tkinter в отдельном потоке
    tkinter_thread = threading.Thread(target=run_tkinter, daemon=True)
    tkinter_thread.start()

    start_listen_port(stop_event)
    # Запускаем иконку в основном потоке
    setup_icon_tray()