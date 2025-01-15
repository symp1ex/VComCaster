from icon import icon_data_start
from logger import logger_vcc, set_config_ini, read_config_ini
import tkinter as tk
from PIL import Image, ImageTk
import io


def toggle_checkbox_autoreconnect(autoreconnect_checkbox_var):
    # Переключаем состояние чекбокса
    if autoreconnect_checkbox_var.get() == 1:
        autoreconnect_checkbox_var.set(0)  # Убираем галочку
    else:
        autoreconnect_checkbox_var.set(1)  # Устанавливаем галочку

def toggle_checkbox_autostart_listing(listing_checkbox_var):
    # Переключаем состояние чекбокса
    if listing_checkbox_var.get() == 1:
        listing_checkbox_var.set(0)  # Убираем галочку
    else:
        listing_checkbox_var.set(1)  # Устанавливаем галочку

def toggle_checkbox_lf(lf_checkbox_var):
    # Переключаем состояние чекбокса
    if lf_checkbox_var.get() == 1:
        lf_checkbox_var.set(0)  # Убираем галочку
    else:
        lf_checkbox_var.set(1)  # Устанавливаем галочку

def toggle_checkbox_cr(cr_checkbox_var):
    # Переключаем состояние чекбокса
    if cr_checkbox_var.get() == 1:
        cr_checkbox_var.set(0)  # Убираем галочку
    else:
        cr_checkbox_var.set(1)  # Устанавливаем галочку

def toggle_checkbox(cr_checkbox_var, lf_checkbox_var, listing_checkbox_var, autoreconnect_checkbox_var):
    toggle_checkbox_cr(cr_checkbox_var)
    toggle_checkbox_lf(lf_checkbox_var)
    toggle_checkbox_autostart_listing(listing_checkbox_var)
    toggle_checkbox_autoreconnect(autoreconnect_checkbox_var)

def valdiate_num_values(value, paramname):
    try:
        value = float(value)
        if value > 0:
            return value
        else:
            logger_vcc.warn(f"Значение параметра {paramname} должно быть положительным числом.")
    except ValueError:
        logger_vcc.error(f"Не удалось получить значение параметра {paramname}.", exc_info=True)
    except Exception:
        logger_vcc.error(f"Значение параметра {paramname} должно быть положительным числом", exc_info=True)


class WinSettingsUi(object):
    def __init__(self):
        self.settings_window = None

    def on_close(self, settings_window):
        self.settings_window = None
        settings_window.destroy()

    def create_win_settings(self):
        self.config = read_config_ini("config.ini")
        self.device_id = self.config.get("device", "device_id", fallback=None)
        self.input_port = self.config.get("device", "input_port", fallback=None)
        self.output_port = self.config.get("device", "output_port", fallback=None)
        self.port_baudrate = self.config.get("device", "port_baudrate", fallback="9600")
        self.cr_value = int(self.config.get("device", "cr", fallback="0"))
        self.lf_value = int(self.config.get("device", "lf", fallback="0"))
        self.autostart_listing = int(self.config.get("app", "autostart_listing", fallback="0"))
        self.autoreconnect = int(self.config.get("app", "autoreconnect", fallback="0"))
        self.timeout_autoreconnect = self.config.get("service", "timeout_autoreconnect", fallback="5")
        self.timeout_reconnect = self.config.get("service", "timeout_reconnect", fallback=5)
        self.timeout_clearcash = self.config.get("service", "timeout_clearcash", fallback="1.5")
        self.logs_autoclear_days = self.config.get("app", "logs-autoclear-days", fallback="3")

        try:
            self.settings_window = tk.Toplevel()
            self.settings_window.protocol("WM_DELETE_WINDOW", lambda: self.on_close(self.settings_window))
            self.settings_window.geometry("400x550")

            self.settings_window.minsize(width=400, height=560)
            self.settings_window.maxsize(width=400, height=550)
            self.settings_window.title("Настройки")

            # Загружаем иконку для окна
            self.start_icon_image = Image.open(io.BytesIO(icon_data_start))
            self.start_icon_image_tk = ImageTk.PhotoImage(self.start_icon_image)


            # Устанавливаем иконку для окна подтверждения
            self.settings_window.start_icon_image = self.start_icon_image_tk
            self.settings_window.iconphoto(False, self.start_icon_image_tk)

            self.settings_window.transient()  # Устанавливает окно дочерним для основного

            # Создаем фрейм для кнопок
            self.button_frame = tk.Frame(self.settings_window)
            self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=10)

            self.save_button = tk.Button(self.button_frame, text="Сохранить", command=self.on_save)
            self.cancel_button = tk.Button(self.button_frame, text="Выйти", command=self.on_cancel)

            # Располагаем кнопки внутри фрейма
            self.save_button.pack(side=tk.RIGHT, padx=5)
            self.cancel_button.pack(side=tk.RIGHT, padx=5)

            # Добавляем подпись к device_id
            self.device_id_label = tk.Label(self.settings_window, text="Путь к экземпляру устройства:")
            self.device_id_label.place(relx=0.007, rely=0.0, height=21, width=184)
            # поле для ид устройства
            self.device_id_entry = tk.Entry(self.settings_window, width=999)
            self.device_id_entry.place(relx=0.025, rely=0.036, height=20, relwidth=0.951)
            self.device_id_entry.insert(0, self.device_id)  # Устанавливаем текущее значение

            self.paste_button = tk.Button(self.settings_window, text="Вставить", command=self.paste_clipboard)
            self.paste_button.place(relx=0.825, rely=0.034, height=22, relwidth=0.15)  # Размещаем кнопку рядом с полем ввода

            self.input_port_label = tk.Label(self.settings_window, text="Входной порт:")
            self.input_port_label.place(relx=0.008, rely=0.107, height=22, width=94)
            self.input_port_entry = tk.Entry(self.settings_window, width=8)
            self.input_port_entry.place(relx=0.326, rely=0.107, height=20, relwidth=0.211)
            self.input_port_entry.insert(0, self.input_port)  # Устанавливаем текущее значение

            self.outport_label = tk.Label(self.settings_window, text="Выходной порт:")
            self.outport_label.place(relx=0.018, rely=0.161, height=22, width=94)
            self.outport_entry = tk.Entry(self.settings_window, width=8)
            self.outport_entry.place(relx=0.326, rely=0.161, height=20, relwidth=0.211)
            self.outport_entry.insert(0, self.output_port)  # Устанавливаем текущее значение

            self.baudrate_label = tk.Label(self.settings_window, text="Скорость передачи:")
            self.baudrate_label.place(relx=0.008, rely=0.214, height=21, width=124)
            self.baudrate_entry = tk.Entry(self.settings_window, width=8)
            self.baudrate_entry.place(relx=0.326, rely=0.214, height=20, relwidth=0.211)
            self.baudrate_entry.insert(0, self.port_baudrate)  # Устанавливаем текущее значение

            # Переменная для хранения состояния чекбокса
            self.cr_checkbox_var = tk.IntVar()
            self.cr_checkbox_var.set(self.cr_value)
            self.cr_checkbox = tk.Checkbutton(self.settings_window, text="Суффикс CR", variable=self.cr_checkbox_var)
            self.cr_checkbox.place(relx=0.707, rely=0.125, relheight=0.045, relwidth=0.253)

            self.lf_checkbox_var = tk.IntVar()
            self.lf_checkbox_var.set(self.lf_value)
            self.lf_checkbox = tk.Checkbutton(self.settings_window, text="Суффикс LF", variable=self.lf_checkbox_var)
            self.lf_checkbox.place(relx=0.704, rely=0.196, relheight=0.045, relwidth=0.253)

            self.listing_checkbox_var = tk.IntVar()
            self.listing_checkbox_var.set(self.autostart_listing)
            self.listing_checkbox = tk.Checkbutton(self.settings_window, text="Подключение к устройству при запуске ",
                                              variable=self.listing_checkbox_var)
            self.listing_checkbox.place(relx=0.003, rely=0.304, relheight=0.045, relwidth=0.654)

            self.autoreconnect_checkbox_var = tk.IntVar()
            self.autoreconnect_checkbox_var.set(self.autoreconnect)
            self.autoreconnect_checkbox = tk.Checkbutton(self.settings_window,
                                                    text="Переподключение к устройству при потери связи",
                                                    variable=self.autoreconnect_checkbox_var)
            self.autoreconnect_checkbox.place(relx=0.005, rely=0.393, relheight=0.045, relwidth=0.779)

            # если бы мы знали что это такое
            sb = tk.Button(self.settings_window,
                           command=lambda: toggle_checkbox(self.cr_checkbox_var,
                                                           self.lf_checkbox_var,
                                                           self.listing_checkbox_var,
                                                           self.autoreconnect_checkbox_var))
            sb.place(relx=0, rely=0, height=0, width=0)
            # но мы не знаем что это такое

            self.Label_autoreconnect_timeout = tk.Label(self.settings_window,
                                                   text="Интервал автоматического переподключения (c.):")
            self.Label_autoreconnect_timeout.place(relx=0.018, rely=0.518, height=21, width=284)
            self.Label_autoreconnect_timeout.configure(anchor='w')
            self.Label_autoreconnect_timeout.configure(compound='left')
            self.autoreconnect_timeout_Entry = tk.Entry(self.settings_window)
            self.autoreconnect_timeout_Entry.place(relx=0.777, rely=0.518, height=20, relwidth=0.11)
            self.autoreconnect_timeout_Entry.insert(0, self.timeout_autoreconnect)

            self.Label_timeout_reconnect = tk.Label(self.settings_window,
                                                    text="Задержка перед ручным переподключением (c.):")
            self.Label_timeout_reconnect.place(relx=0.018, rely=0.589, height=22, width=284)
            self.Label_timeout_reconnect.configure(anchor='w')
            self.Label_timeout_reconnect.configure(compound='left')
            self.timeout_reconnect_Entry = tk.Entry(self.settings_window)
            self.timeout_reconnect_Entry.place(relx=0.777, rely=0.589, height=20, relwidth=0.11)
            self.timeout_reconnect_Entry.insert(0, self.timeout_reconnect)

            self.Label_timeout_clearcash = tk.Label(self.settings_window, text="Время жизни данных в буфере (с.):")
            self.Label_timeout_clearcash.place(relx=0.018, rely=0.661, height=21, width=204)
            self.Label_timeout_clearcash.configure(anchor='w')
            self.Label_timeout_clearcash.configure(compound='left')
            self.timeout_clearcash_Entry = tk.Entry(self.settings_window)
            self.timeout_clearcash_Entry.place(relx=0.563, rely=0.661, height=20, relwidth=0.11)
            self.timeout_clearcash_Entry.insert(0, self.timeout_clearcash)

            self.Label1_logs_days = tk.Label(self.settings_window, text="Удалять логи старше")
            self.Label1_logs_days.place(relx=0.019, rely=0.732, height=21, width=124)
            self.Label1_logs_days.configure(anchor='w')
            self.Label1_logs_days.configure(compound='left')
            self.logs_days_Entry = tk.Entry(self.settings_window)
            self.logs_days_Entry.place(relx=0.354, rely=0.732, height=20, relwidth=0.11)
            self.logs_days_Entry.insert(0, self.logs_autoclear_days)
            self.Label2_logs_day = tk.Label(self.settings_window, text="дней")
            self.Label2_logs_day.place(relx=0.489, rely=0.732, height=21, width=34)
            self.Label2_logs_day.configure(anchor='w')
            self.Label2_logs_day.configure(compound='left')
        except Exception:
            logger_vcc.error(f"Не удалось инициализировать окно настроек.", exc_info=True)

    def init_win_settings(self):
        if not self.settings_window:
            self.create_win_settings()
        else:
            self.settings_window.destroy()
            self.settings_window = None

    def paste_clipboard(self):
        try:
            clipboard_content = self.settings_window.clipboard_get()  # Получаем содержимое буфера обмена
            self.device_id_entry.delete(0, tk.END)  # Очищаем поле ввода
            self.device_id_entry.insert(0, clipboard_content)  # Вставляем содержимое буфера обмена
        except Exception:
            logger_vcc.warning("Не удалось получить содержимое буфера обмена", exc_info=True)

    def on_save(self):
        from vcomcaster import message_error_box

        new_device_id = self.device_id_entry.get()
        if self.device_id != new_device_id:
            set_config_ini("config.ini", "device", "device_id", new_device_id)

        new_input_port = self.input_port_entry.get()
        if self.input_port != new_input_port:
            set_config_ini("config.ini", "device", "input_port", new_input_port)

        new_output_port = self.outport_entry.get()
        if self.output_port != new_output_port:
            set_config_ini("config.ini", "device", "output_port", new_output_port)

        new_port_baudrate = self.baudrate_entry.get()
        if self.port_baudrate != new_port_baudrate:
            set_config_ini("config.ini", "device", "port_baudrate", new_port_baudrate)

        cr_checkbox = self.cr_checkbox_var.get()
        if cr_checkbox != self.cr_value:
            set_config_ini("config.ini", "device", "cr", str(cr_checkbox))

        lf_checkbox = self.lf_checkbox_var.get()
        if lf_checkbox != self.lf_value:
            set_config_ini("config.ini", "device", "lf", str(lf_checkbox))

        listing_checkbox = self.listing_checkbox_var.get()
        if listing_checkbox != self.autostart_listing:
            set_config_ini("config.ini", "app", "autostart_listing", str(listing_checkbox))

        autoreconnect_checkbox = self.autoreconnect_checkbox_var.get()
        if autoreconnect_checkbox != self.autoreconnect:
            set_config_ini("config.ini", "app", "autoreconnect", str(autoreconnect_checkbox))

        new_timeout_autoreconnect = valdiate_num_values(self.autoreconnect_timeout_Entry.get(), "timeout_autoreconnect")
        if not new_timeout_autoreconnect:
            message_error_box(f"Значение тайм-аута для автоматического переподключения должно быть положительным числом.")
            return
        elif str(new_timeout_autoreconnect) != self.timeout_autoreconnect:
            set_config_ini("config.ini", "service", "timeout_autoreconnect", str(new_timeout_autoreconnect))

        new_timeout_reconnect = valdiate_num_values(self.timeout_reconnect_Entry.get(), "timeout_reconnect")
        if not new_timeout_reconnect:
            message_error_box(f"Значение тайм-аута для ручного переподключения должно быть положительным числом.")
            return
        elif str(new_timeout_reconnect) != self.timeout_reconnect:
            set_config_ini("config.ini", "service", "timeout_reconnect", str(new_timeout_reconnect))

        new_timeout_clearcash = valdiate_num_values(self.timeout_clearcash_Entry.get(), "timeout_clearcash")
        if not new_timeout_clearcash:
            message_error_box(f"Значение тайм-аута для хранения данных в буфере должно быть положительным числом.")
            return
        elif str(new_timeout_clearcash) != self.timeout_clearcash:
            set_config_ini("config.ini", "service", "timeout_clearcash", str(new_timeout_clearcash))

        new_logs_autoclear_days = valdiate_num_values(self.logs_days_Entry.get(), "logs-autoclear-days")
        if not new_logs_autoclear_days:
            message_error_box(f"Количество дней хранения логов должно быть положительным числом.")
            return
        elif str(int(new_logs_autoclear_days)) != self.logs_autoclear_days:
            set_config_ini("config.ini", "app", "logs-autoclear-days", str(int(new_logs_autoclear_days)))

        self.settings_window.destroy()
        self.settings_window = None

    def on_cancel(self):
        self.settings_window.destroy()
        self.settings_window = None
