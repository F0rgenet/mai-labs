#import "@preview/codly:1.3.0": *
#import "@preview/codly-languages:0.1.1": *
#import "@preview/modern-g7-32:0.1.0": gost, abstract, title-templates, structure-heading, annexes

#codly(zebra-fill: none, display-name: false, display-icon: false, number-format: none)

#show figure: set block(breakable: true)

#show: codly-init.with()

#let variant = 37

#show: gost.with(
  title-template: title-templates.mai-university-lab,
  performers: (
    (name: "Елисеев П.А.", position: "Студент М3О-221Б-23"),
  ),
  institute: (number: 3, name: "Системы управления, информатика и электроэнергетика"),
  department: (number: 307, name: "Цифровые технологии и информационные системы"),
  report-type: [Лабораторная работа №1ы],
  about: [По дисциплине "Администрирование linux"],
  research: [Вариант №#variant],
  bare-subject: true,
  subject: "",
  manager: (name: "Боровской К.И.", position: "Ассистент кафедры 307"),
  city: "Москва",
)

#outline()

#structure-heading[Задание]

*Цель лабораторной работы:* Освоить процесс развертывания и администрирования серверного приложения OpenTTD в ОС Linux, используя возможности системы инициализации Systemd для управления сервисом, его безопасностью и ресурсами.

*Задачи работы:* В рамках лабораторной работы необходимо исследовать и подготовить проект OpenTTD к запуску, включая его сборку и ручную настройку. Далее следует создать systemd-юнит для автоматизации управления сервисом, реализовать два варианта автоматического резервного копирования его данных (через Cron и systemd-таймеры). После этого потребуется усилить безопасность сервиса, применив встроенные в Systemd механизмы харденинга, и, наконец, создать systemd-slice для выделения и ограничения потребляемых сервисом системных ресурсов.

= Описание сервиса
OpenTTD — компьютерная игра, портированная версия известной игры Transport Tycoon Deluxe. OpenTTD является бесплатной и свободной программой.

Суть игры в создании и успешном развитии транспортного предприятия, которым руководит игрок. Развитие происходит благодаря извлечению прибыли, которая получается от перевозок грузов и пассажиров разнообразным транспортом (железнодорожным, авто, авиа и водным). Игроки могут прокладывать мосты и тоннели, строить дороги, железные дороги, станции, аэропорты, каналы и акведуки.

#figure(image("assets/game.png", width: 100%), caption: [Интерфейс игры OpenTTD])

OpenTTD поддерживает многопользовательский режим, есть возможность использовать dedicated server для хостинга сетевых игр. В этой лабораторной работе я разверну такой сервер. Главная задача - войти в сетевой матч с моего устройства.

В этой работе будет использоваться версия игры *14.1*.

= Характеристики проекта
OpenTTD написана на C++, для сборки используется CMake.
Зависимости: `build-essential`, `cmake`, `libsdl2-dev`, `zlib1g-dev`, `liblzma-dev`, `liblzo2-dev`, `libfontconfig1-dev`, `libicu-dev`, `libpng-dev`, `libfreetype6-dev`, `libzstd-dev`.

Для работы движка требуются:
- Графический сет (OpenGFX)
- Звуковой сет (OpenSFX)
- Музыкальный сет (OpenMSX)

База данных не требуется, сохранения и конфиги хранятся как файлы.
Кеширование также не требуется.

== Конфигурация проекта
С помощью файла openttd.cfg. Обычно он находится в `~/.openttd/` или в системном пути как `/etc/openttd/` или указан с помощью опции `-c <path/to/config>` командной строки.

= Подготовка оборудования
Для выполнения лабораторной работы мной было принято решение арендовать VDS у хостинг-провайдера timeweb, это решение обусловлено тем, что в результате выполнения лабораторной работы я получу готовый снапшот полностью настроенного VDS для сервера OpenTTD, который смогу переиспользовать.

Я выбрал сервер с параметрами, которые указаны на рисунке @характеристики-сервера, стоимость указана там же.
#figure(image("assets/specs.png", width: 40%), caption: [Характеристики арендуемого сервера]) <характеристики-сервера>

В качестве операционной системы под будущий сервис была выбрана Ubuntu 22.04, поскольку с ней я работал чаще всего.

#figure(image("assets/ubuntu.png", width: 70%), caption: [Выбор операционной системы])

После настройки сервера со стороны хостинга, я получил к нему доступ через SSH.

#figure(image("assets/terminal.png", width: 90%), caption: [Терминал на сервере])

= Сборка исходников

Сперва я склонировал проект и переключился на стабильный релиз версии 14.1.

#figure(image("assets/clone.png", width: 90%), caption: [Клонирование проекта])

Затем я установил необходимые внешние библиотеки игры.

#figure(image("assets/libs.png", width: 94%), caption: [Установка внешних библиотек])

Я установил `cmake`, `build-essential`, а также `libsdl2-dev`, `liblzma-dev`, `libpng-dev` и `libcurl4-openssl-dev` для сборки игры:

```bash
sudo apt install cmake build-essential libsdl2-dev liblzma-dev libpng-dev libcurl4-openssl-dev
```

После этого я собрал проект в релизной конфигурации для выделенных серверов:

```bash
cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo -DOPTION_DEDICATED=ON
make
```

#figure(image("assets/build.png", width: 90%), caption: [Сборка OpenTTD])

Для сборки не хватило оперативной памяти, пришлось использовать swap.

= Первый запуск
#figure(image("assets/error.png"), caption: [Ошибка при запуске])

После сборки проекта я получил ошибку в консоли:

```bash
Error: Failed to find a graphics set. Please acquire a graphics set for OpenTTD. See section 1.4 of README.md.
```

Это было ожидаемо, требуется установить графический сет OpenGFX.

== Установка OpenGFX

#figure(image("assets/install-gfx.png", width: 70%), caption: [Установка OpenGFX])

Для установки OpenGFX необходимо скачать архив c официального сайта перейти в директорию с ним, затем перенести файл `opengfx-7.1/opengfx.obg` в каталог `~/.openttd/baseset/`.

Архив: https://cdn.openttd.org/opengfx-releases/7.1/opengfx-7.1-all.zip

#figure(image("assets/cpgfx.png", width: 70%), caption: [Перенос OpenGFX в каталог])

#figure(```bash 
~/openttd_source/build/openttd -D
```,
caption: [Запуск OpenTTD с установленным OpenGFX])

#figure(image("assets/working.png", width: 70%), caption: [Работающий сервер OpenTTD])

#pagebreak()

== Проверка в игре

#figure(image("assets/ingame.png", width: 90%), caption: [Проверка работы сервера в игре])

Сервер работает и доступен.

= Создание Systemd юнита

== Создание пользователя и группы для сервиса
Рекомендуется запускать службы от имени выделенного непривилегированного пользователя для повышения безопасности. Создадим пользователя `openttd` и группу `openttd`:
#figure(
```bash
sudo groupadd --system openttd
sudo useradd --system -g openttd -d /opt/openttd -s /sbin/nologin -c "OpenTTD Server" openttd
```,
caption: [Создание системного пользователя и группы openttd]
)

== Исполняемый файл

#figure(
```bash
cp ~/openttd_source/build/openttd /opt/openttd/bin
cp ~/openttd_source/build/lang /opt/openttd/bin/
```,
caption: [Копирование бинарника в требуемую директорию]
)

== Файл конфигурации
```bash
cp ~/.config/openttd/openttd.cfg /etc/openttd/
```

== Наборы ресурсов
```bash
cp -r ~/.openttd/baseset/ /opt/openttd/.openttd/
```
#pagebreak()

== Конфигурация systemd
```
[Unit]
Description=OpenTTD Dedicated Server
After=network.target

[Service]
Type=simple
User=openttd
Group=openttd

Environment="HOME=/opt/openttd"

ExecStart=/opt/openttd/bin/openttd -D -c /etc/openttd/openttd.cfg

WorkingDirectory=/opt/openttd/data

Restart=on-failure
RestartSec=5s

ConfigurationDirectory=openttd
StateDirectory=openttd
LogsDirectory=openttd
CacheDirectory=openttd

StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Юнит с харденингом будет рассмотрен в @hardening.

= Бекапы

== Systemd юнит для бекапов
```bash
#!/bin/bash

SOURCE_FILE="/var/lib/openttd/saves/save.sav"
BACKUP_DIR="/var/lib/openttd/backups/"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="${BACKUP_DIR}/save_${TIMESTAMP}.sav.gz"

if [ ! -f "$SOURCE_FILE" ]; then
  exit 1
fi

mkdir -p "$BACKUP_DIR"
gzip -c "$SOURCE_FILE" > "$BACKUP_FILE"

find "$BACKUP_DIR" -type f -name "*.sav.gz" -mtime +14 -delete
```

Сделал скрипт исполняемым:
```bash
sudo chmod +x /usr/local/bin/backup-openttd.sh
```

= Slice для ограничения ресурсов
```bash
[Unit]
Description=Slice for the OpenTTD Application

[Slice]
CPUAccounting=true
MemoryAccounting=true
CPUQuota=50%
MemoryMax=1G
```
Указал ограничение в 50% CPU и один гигабайт памяти

== Харденинг сервиса со слайсом <hardening>
```bash
[Unit]
Description=OpenTTD Dedicated Server
After=network.target

[Service]
Type=simple
User=openttd
Group=openttd
Slice=app-openttd.slice

ExecStart=/opt/openttd/bin/openttd -D -c /etc/openttd/openttd.cfg -g /var/lib/openttd/saves/save.sav
Restart=on-failure
RestartSec=5s

NoNewPrivileges=true
LockPersonality=true
MemoryDenyWriteExecute=true
RemoveIPC=true
RestrictNamespaces=true
RestrictRealtime=true
RestrictSUIDSGID=true
CapabilityBoundingSet=
RestrictAddressFamilies=AF_INET AF_INET6
SystemCallArchitectures=native
SystemCallFilter=@basic-io @file-system @process @signal @clock @network-io @ipc @memory-management

PrivateUsers=true
UMask=0077

PrivateTmp=true
PrivateDevices=true
ProtectSystem=strict
ProtectHome=true
ProtectClock=true
ProtectHostname=true
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectKernelLogs=true
ProtectControlGroups=true
ProtectProc=invisible
ProcSubset=pid

ReadWritePaths=/opt/openttd/data /var/lib/openttd /var/log/openttd /var/lib/openttd/saves /etc/openttd
ReadOnlyPaths=/opt/openttd

ConfigurationDirectory=openttd
StateDirectory=openttd
LogsDirectory=openttd
CacheDirectory=openttd

StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

== Юзер под бекапы
```bash
sudo useradd -r -s /bin/false backupuser
sudo mkdir -p /var/lib/openttd/backups/
sudo chown backupuser:backupuser /var/lib/openttd/backups/
```

== Systemd под бекапы
```bash
[Unit]
Description=OpenTTD Backup Service

[Service]
Type=oneshot
User=backupuser
Group=backupuser

ExecStart=/usr/local/bin/backup-openttd.sh

Environment="PATH=/bin:/usr/bin"
Environment="HOME=/tmp"

SystemCallArchitectures=native
RestrictAddressFamilies=AF_UNIX ~AF_INET ~AF_INET6

PrivateTmp=true
PrivateDevices=true
ProtectClock=true
ProtectHostname=true
ProtectKernelTunables=true

ReadWritePaths=/var/lib/openttd/backups/
ReadOnlyPaths=/var/lib/openttd/saves/save.sav

UMask=0077

StandardOutput=journal
StandardError=journal
```

#pagebreak()

== Работа с таймером
```bash
[Unit]
Description=Run OpenTTD Backup Service on schedule
Wants=openttd-backup.service

[Timer]
OnCalendar=*-*-* 03:00:00
Persistent=true

[Install]
WantedBy=timers.target
```
#figure(image("assets/times.png"), caption: [Работа с таймером])

= Заключение

В рамках этой лабораторной работы я успешно развернул и настроил выделенный сервер OpenTTD на арендованном VDS-сервере под управлением Linux. Основной задачей было освоить администрирование сервиса при помощи Systemd, и это удалось в полной мере. Я начал с того, что сам собрал игру из исходников, установил все необходимые компоненты и запустил сервер, убедившись в его работоспособности.

Ключевым этапом стало создание и настройка Systemd-юнита для автоматического запуска OpenTTD, его перезапуска при сбоях и запуска от имени отдельного, непривилегированного пользователя, что значительно повышает безопасность. Для защиты игровых данных я реализовал систему резервного копирования: написал скрипт для автоматического создания бэкапов и настроил Systemd-таймер для его регулярного запуска, при этом бэкапы также выполнялись от имени отдельного пользователя для большей безопасности.

Отдельное внимание уделил усилению защиты самого сервиса. Применил различные функции Systemd для "харденинга", ограничив доступ OpenTTD к системным ресурсам, файлам и командам, чтобы минимизировать потенциальные риски. Кроме того, чтобы сервер не потреблял слишком много ресурсов моего VDS, я создал Systemd-slice и установил лимиты на использование процессора и оперативной памяти.

В результате, я не только запустил полностью функциональный и доступный OpenTTD-сервер (успешно подключился к нему из игры), но и получил ценный опыт в настройке, обеспечении безопасности и управлении серверными приложениями в Linux, используя продвинутые возможности Systemd. Это дало мне глубокое понимание, как работают и как должны быть защищены реальные сервисы.