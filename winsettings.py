from icon import icon_data_start
from logger import logger_vcc, set_config_ini, read_config_ini
import tkinter as tk
from PIL import Image, ImageTk
import io

def init_win_settings():
    config = read_config_ini("config.ini")
    device_id = config.get("device", "device_id", fallback=None)
    input_port = config.get("device", "input_port", fallback=None)
    output_port = config.get("device", "output_port", fallback=None)
    port_baudrate = config.get("device", "port_baudrate", fallback=None)
    cr_value = int(config.get("device", "cr", fallback=None))
    lf_value = int(config.get("device", "lf", fallback=None))
    autostart_listing = int(config.get("app", "autostart_listing", fallback=None))
    autoreconnect = int(config.get("app", "autoreconnect", fallback=None))
    timeout_autoreconnect = config.get("service", "timeout_autoreconnect", fallback=None)
    timeout_reconnect = config.get("service", "timeout_reconnect", fallback=None)
    timeout_clearcash = config.get("service", "timeout_clearcash", fallback=None)
    logs_autoclear_days = config.get("app", "logs-autoclear-days", fallback=None)

    def toggle_checkbox_cr(cr_checkbox_var):
        # Переключаем состояние чекбокса
        if cr_checkbox_var.get() == 1:
            cr_checkbox_var.set(0)  # Убираем галочку
        else:
            cr_checkbox_var.set(1)  # Устанавливаем галочку

    def toggle_checkbox_lf(lf_checkbox_var):
        # Переключаем состояние чекбокса
        if lf_checkbox_var.get() == 1:
            lf_checkbox_var.set(0)  # Убираем галочку
        else:
            lf_checkbox_var.set(1)  # Устанавливаем галочку

    def toggle_checkbox_autostart_listing(listing_checkbox_var):
        # Переключаем состояние чекбокса
        if listing_checkbox_var.get() == 1:
            listing_checkbox_var.set(0)  # Убираем галочку
        else:
            listing_checkbox_var.set(1)  # Устанавливаем галочку

    def toggle_checkbox_autoreconnect(autoreconnect_checkbox_var):
        # Переключаем состояние чекбокса
        if autoreconnect_checkbox_var.get() == 1:
            autoreconnect_checkbox_var.set(0)  # Убираем галочку
        else:
            autoreconnect_checkbox_var.set(1)  # Устанавливаем галочку

    def toggle_checkbox(cr_checkbox_var, lf_checkbox_var, listing_checkbox_var, autoreconnect_checkbox_var):
        toggle_checkbox_cr(cr_checkbox_var)
        toggle_checkbox_lf(lf_checkbox_var)
        toggle_checkbox_autostart_listing(listing_checkbox_var)
        toggle_checkbox_autoreconnect(autoreconnect_checkbox_var)


    try:
        def on_save():
            new_device_id = device_id_entry.get()
            if device_id != new_device_id:
                set_config_ini("config.ini", "device", "device_id", new_device_id)

            new_input_port = input_port_entry.get()
            if input_port != new_input_port:
                set_config_ini("config.ini", "device", "input_port", new_input_port)

            new_output_port = outport_entry.get()
            if output_port != new_output_port:
                set_config_ini("config.ini", "device", "output_port", new_output_port)

            new_port_baudrate = baudrate_entry.get()
            if port_baudrate != new_port_baudrate:
                set_config_ini("config.ini", "device", "port_baudrate", new_port_baudrate)

            cr_checkbox = cr_checkbox_var.get()
            if cr_checkbox != cr_value:
                set_config_ini("config.ini", "device", "cr", str(cr_checkbox))

            lf_checkbox = lf_checkbox_var.get()
            if lf_checkbox != lf_value:
                set_config_ini("config.ini", "device", "lf", str(lf_checkbox))

            listing_checkbox = listing_checkbox_var.get()
            if listing_checkbox != autostart_listing:
                set_config_ini("config.ini", "app", "autostart_listing", str(listing_checkbox))

            autoreconnect_checkbox = autoreconnect_checkbox_var.get()
            if autoreconnect_checkbox != autoreconnect:
                set_config_ini("config.ini", "app", "autoreconnect", str(autoreconnect_checkbox))

            new_timeout_autoreconnect = autoreconnect_timeout_Entry.get()
            if new_timeout_autoreconnect != timeout_autoreconnect:
                set_config_ini("config.ini", "service", "timeout_autoreconnect", new_timeout_autoreconnect)

            new_timeout_reconnect = timeout_reconnect_Entry.get()
            if new_timeout_reconnect != timeout_reconnect:
                set_config_ini("config.ini", "service", "timeout_reconnect", new_timeout_reconnect)

            new_timeout_clearcash = timeout_clearcash_Entry.get()
            if new_timeout_clearcash != timeout_clearcash:
                set_config_ini("config.ini", "service", "timeout_clearcash", new_timeout_clearcash)

            new_logs_autoclear_days = logs_days_Entry.get()
            if new_logs_autoclear_days != logs_autoclear_days:
                set_config_ini("config.ini", "app", "logs-autoclear-days", new_logs_autoclear_days)

            settings_window.destroy()


        def on_cancel():
            settings_window.destroy()

        settings_window = tk.Toplevel()
        settings_window.geometry("400x550")
        settings_window.minsize(width=400, height=560)
        settings_window.maxsize(width=400, height=550)
        settings_window.title("Настройки")

        # Загружаем иконку для окна
        start_icon_image = Image.open(io.BytesIO(icon_data_start))
        start_icon_image_tk = ImageTk.PhotoImage(start_icon_image)

        # Устанавливаем иконку для окна подтверждения
        settings_window.start_icon_image = start_icon_image_tk
        settings_window.iconphoto(False, start_icon_image_tk)

        settings_window.transient()  # Устанавливает окно дочерним для основного

        # Создаем фрейм для кнопок
        button_frame = tk.Frame(settings_window)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=10)

        save_button = tk.Button(button_frame, text="Сохранить", command=on_save)
        cancel_button = tk.Button(button_frame, text="Выйти", command=on_cancel)

        # Располагаем кнопки внутри фрейма
        save_button.pack(side=tk.RIGHT, padx=5)
        cancel_button.pack(side=tk.RIGHT, padx=5)

        # Добавляем подпись к device_id
        device_id_label = tk.Label(settings_window, text="Путь к экземпляру устройства:")
        device_id_label.place(relx=0.007, rely=0.0, height=21, width=184)
        #поле для ид устройства
        device_id_entry = tk.Entry(settings_window, width=999)
        device_id_entry.place(relx=0.025, rely=0.036, height=20, relwidth=0.951)
        device_id_entry.insert(0, device_id)  # Устанавливаем текущее значение

        def paste_clipboard():
            try:
                clipboard_content = settings_window.clipboard_get()  # Получаем содержимое буфера обмена
                device_id_entry.delete(0, tk.END)  # Очищаем поле ввода
                device_id_entry.insert(0, clipboard_content)  # Вставляем содержимое буфера обмена
            except Exception:
                logger_vcc("Не удалось получить содержимое буфера обмена", exc_info=True)

        paste_button = tk.Button(settings_window, text="Вставить", command=paste_clipboard)
        paste_button.place(relx=0.825, rely=0.034, height=22, relwidth=0.15)  # Размещаем кнопку рядом с полем ввода

        input_port_label = tk.Label(settings_window, text="Входной порт:")
        input_port_label.place(relx=0.008, rely=0.107, height=22, width=94)
        input_port_entry = tk.Entry(settings_window, width=8)
        input_port_entry.place(relx=0.326, rely=0.107, height=20, relwidth=0.211)
        input_port_entry.insert(0, input_port)  # Устанавливаем текущее значение

        outport_label = tk.Label(settings_window, text="Выходной порт:")
        outport_label.place(relx=0.018, rely=0.161, height=22, width=94)
        outport_entry = tk.Entry(settings_window, width=8)
        outport_entry.place(relx=0.326, rely=0.161, height=20, relwidth=0.211)
        outport_entry.insert(0, output_port)  # Устанавливаем текущее значение

        baudrate_label = tk.Label(settings_window, text="Скорость передачи:")
        baudrate_label.place(relx=0.008, rely=0.214, height=21, width=124)
        baudrate_entry = tk.Entry(settings_window, width=8)
        baudrate_entry.place(relx=0.326, rely=0.214, height=20, relwidth=0.211)
        baudrate_entry.insert(0, port_baudrate)  # Устанавливаем текущее значение

        # Переменная для хранения состояния чекбокса
        cr_checkbox_var = tk.IntVar()
        cr_checkbox_var.set(cr_value)
        cr_checkbox = tk.Checkbutton(settings_window, text="Суффикс CR", variable=cr_checkbox_var)
        cr_checkbox.place(relx=0.707, rely=0.125, relheight=0.045, relwidth=0.253)

        lf_checkbox_var = tk.IntVar()
        lf_checkbox_var.set(lf_value)
        lf_checkbox = tk.Checkbutton(settings_window, text="Суффикс LF", variable=lf_checkbox_var)
        lf_checkbox.place(relx=0.704, rely=0.196, relheight=0.045, relwidth=0.253)

        listing_checkbox_var = tk.IntVar()
        listing_checkbox_var.set(autostart_listing)
        listing_checkbox = tk.Checkbutton(settings_window, text="Подключение к устройству при запуске ", variable=listing_checkbox_var)
        listing_checkbox.place(relx=0.003, rely=0.304, relheight=0.045, relwidth = 0.654)

        autoreconnect_checkbox_var = tk.IntVar()
        autoreconnect_checkbox_var.set(autoreconnect)
        autoreconnect_checkbox = tk.Checkbutton(settings_window, text="Переподключение к устройству при потери связи", variable=autoreconnect_checkbox_var)
        autoreconnect_checkbox.place(relx=0.005, rely=0.393, relheight=0.045, relwidth = 0.779)

        sb = tk.Button(settings_window, command=lambda: toggle_checkbox(cr_checkbox_var, lf_checkbox_var, listing_checkbox_var, autoreconnect_checkbox_var)) # если бы мы знали что это такое =)
        sb.place(relx=0, rely=0, height=0, width=0) # но мы не знаем что это такое =)

        Label_autoreconnect_timeout = tk.Label(settings_window, text="Интервал автоматического переподключения (c.):")
        Label_autoreconnect_timeout.place(relx=0.018, rely=0.518, height=21, width=284)
        Label_autoreconnect_timeout.configure(anchor='w')
        Label_autoreconnect_timeout.configure(compound='left')
        autoreconnect_timeout_Entry = tk.Entry(settings_window)
        autoreconnect_timeout_Entry.place(relx=0.777, rely=0.518, height=20, relwidth=0.11)
        autoreconnect_timeout_Entry.insert(0, timeout_autoreconnect)

        Label_timeout_reconnect = tk.Label(settings_window, text="Задержка перед ручным переподключением (c.):")
        Label_timeout_reconnect.place(relx=0.013, rely=0.589, height=22, width=284)
        Label_autoreconnect_timeout.configure(anchor='w')
        Label_autoreconnect_timeout.configure(compound='left')
        timeout_reconnect_Entry = tk.Entry(settings_window)
        timeout_reconnect_Entry.place(relx=0.777, rely=0.589, height=20, relwidth=0.11)
        timeout_reconnect_Entry.insert(0, timeout_reconnect)

        Label_timeout_clearcash = tk.Label(settings_window, text="Время жизни данных в буфере (с.):")
        Label_timeout_clearcash.place(relx=0.018, rely=0.661, height=21, width=204)
        Label_timeout_clearcash.configure(anchor='w')
        Label_timeout_clearcash.configure(compound='left')
        timeout_clearcash_Entry = tk.Entry(settings_window)
        timeout_clearcash_Entry.place(relx=0.551, rely=0.661, height=20, relwidth=0.11)
        timeout_clearcash_Entry.insert(0, timeout_clearcash)

        Label1_logs_days = tk.Label(settings_window, text="Хранить логи")
        Label1_logs_days.place(relx=0.019, rely=0.732, height=21, width=84)
        Label1_logs_days.configure(anchor='w')
        Label1_logs_days.configure(compound='left')
        logs_days_Entry = tk.Entry(settings_window)
        logs_days_Entry.place(relx=0.244, rely=0.732, height=20, relwidth=0.11)
        logs_days_Entry.insert(0, logs_autoclear_days)
        Label2_logs_day = tk.Label(settings_window, text="дней")
        Label2_logs_day.place(relx=0.369, rely=0.732, height=21, width=34)
        Label2_logs_day.configure(anchor='w')
        Label2_logs_day.configure(compound='left')
    except Exception:
        logger_vcc.error(f"Не удалось инициализировать окно настроек.", exc_info=True)
