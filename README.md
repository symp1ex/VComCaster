# VComCaster
Данная утилита призванна решить проблему связи устройств, использующих драйвер usb virtual com (например 2D сканер штрих-кодов) и тяжёлого ПО (например кассовое ПО). Часто сканер, в приведённом примере, может отваливаться и после его переподключения, чтобы заново занять зависший порт, приходится перезапускать использующее его ПО, что может занимать много времени. Утилита сама переподключается к сканеру и сама способная его найти на новом com-порту, если он изменился. Кассовое ПО же слушает вирутальный com-порт, который постоянен, не меняется и не зависает, что избавляет от необходимости перезапуска ПО.

Чтобы начать пользоваться:

1. Создать пару виртуальных com-портов, использовать для этого можно программу com0com*. При установке снять галку с "CNCA0 <-> CNCB0".

2. Один из созданных вирутальных com-портов указываем в файле настроек iikoFrtont (config.xml) вместо сканера.

3. Второй вирутальный порт указываем в config.ini самой утилиты в параметр "output_port".

4. Физический порт сканера указываем в том же конфиге в параметр "input_port".

5. Запустить от админа "autorun_exclusion.bat"

6. Если хотим, чтобы сканер при смене порта продолжал автоматически переподключаться, в параметр "device_id" вписываем "ИД оборудования" из свойств сканера в диспетчере устройств Винды.** Для отключения функции, просто оставьте значение пустым.

7. Перед запуском убедиться, что параметр "autostart_listing" = 1. Если настраиваем через интерфейс, перед сохранением проверить что активирована галочка "Подключение к устройству при запуске".

8. Сохраняем конфиг и запускаем. (если уже запущена: щёлкнуть правой кнопкой по иконке в трее, нажать "стоп" и нажать "переподключиться")

После изменении настроек в конфиге при запущенном приложении, всегда стоит нажать на "переподключиться".
<br>
<br>
<br>

Настройка на примере подключения сканера к iikoFront:
![README](https://github.com/user-attachments/assets/05d50390-bec1-460e-9390-7d052a3a4bb2)
<br>
<br>
<br>
<br>
<br>
На Win7 и Embedded может появиться сообщение об ошибке, тогда понадобиться установка обновления безопасности KB3063858. (гуглится по номеру обновления и названию Винды, весит 900кб. Для Win7 отдельный установщик, для Embedded отдельный.)
<br>
<br>
*При установке com0com нужно поставить галочку напротив пункта "COM# <-> COM#" и снять напротив пункта "CNCA0 <-> CNCB0", если она стоит. Останется только зайти в диспетчер устройств и посмотреть номера созданных портов. С программой на этом всё.
Хотя... если в BIOS включена настройка "SecureBoot", то Винда будет ругаться на отсутствие подписи у драйверов наших виртуальных портов. Придётся либо выключить настройку, либо пытаться загружать систему без обязательной проверки подписи драйверов, либо использовать другую программу, драйвера которой будут нравиться Винде. Вроде существуют платные альтернативы. ¯\_(ツ)_/¯<br><br>
Так же нет проблем с подписью в com0com 2.2.2.0, но там можно создать только порты типа "CNCA0 <-> CNCB0", придётся зайти в интерфейс программы и переименовать эти порты в формате "COM# <-> COM#", указав свободные номера и включить для обоих настройку "emulate baud rate". В диспетчере устройств эти порты отображаться не будут, но передача данных будет работать корректно.
<br>
<br>
**Поиск идёт по "Путь к экземпляру устройства" из свойств сканера в диспетчере устройств Винды, но не по полному значению, а по маске. От значения нужно откинуть последние 5-7 символов (т.к. они могут меняться, если поменялся номер порта). Параметр "amount_rm_char_id = 0" определяет сколько символов откидывать от "device_id" перед поиском. Можно оставить 0, но тогда придётся вручную убрать лишние 5-7 символов из пути к устройству.
Я не знаю от чего зависит, но обычно при переключении устройства между соседними usb-портами в "Путь к экземпляру устройства" меняются только последние несколько символов и всё отрабатывает как надо. Если переключить устройство, например, из передней панели ПК в заднюю, то поменяется вся часть пути после "ИД обородувания" и сканер уже находиться не будет. Если такое происходит, то можно указывать именно "ИД обородувания" (он идентичен первой половине "Путь к экземпляру устройства") из диспетчера устройств, только убедитесь что нет других устройств использующих тот же драйвер (тогда "ИД обородувания" будет совпадать) и не забудьте выставить параметр "amount_rm_char_id" строго на 0.
<br>
<br>
Параметром "timeout_clearcash = 1.5" определяется сколько в секундах могут жить данные в буфере, до того как будут прочитаны. Пока данные в буфере хранятся, без перезапуска утилиты порт освободить нереально, даже отключив сканер от ПК. У меня при тестах всё корректно передавалось при значении 0.01. В теории, на ооооооооооооооооооооооочень(ну вы поняли) медленном железе, 1.5 секунд может оказать мало и марка будет передаваться не полностью, в таком случае пробуйте увеличить это значение. Это только в теории, слабо представляю что такое вообще возможно. (но параметр всё равно вынесен в конфиг)
<br>
<br>
При первом запуске утилита не сможет сама найти сканер по "device_id", пока не будет нажата кнопка "переподключиться". Когда включен "autoreconnect", то утилита сделает это за вас. Если не используется "autoreconnect", порт устройства лучше сразу указывать вручную. Хотя лучше это делать в любом случае.)
<br>
<br>
В "окно терминала" полностью дублируются логи в реальном времени, при подключении и настройки нет необходимости смотреть лог-файл.

