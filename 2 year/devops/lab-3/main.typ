#import "@preview/codly:1.3.0": *
#import "@preview/codly-languages:0.1.1": *
#import "@preview/modern-g7-32:0.1.0": gost, abstract, title-templates, structure-heading, annexes

// Настройки для блоков с кодом
#codly(zebra-fill: none, display-name: false, display-icon: false, number-format: none)

// Разрешаем разрыв страниц внутри figure
#show figure: set block(breakable: true)

#show: codly-init.with()

// Настройки титульного листа по ГОСТ
#show: gost.with(
  title-template: title-templates.mai-university-lab,
  performers: (
    (name: "Елисеев П.А.", position: "Студент М3О-221Б-23"),
  ),
  institute: (number: 3, name: "Системы управления, информатика и электроэнергетика"),
  department: (number: 307, name: "Цифровые технологии и информационные системы"),
  report-type: [Лабораторная работа №3],
  about: [По дисциплине "Администрирование linux"],
  bare-subject: true,
  subject: [Работа с файловой системой Btrfs],
  manager: (name: "Боровской К.И.", position: "Ассистент кафедры 307"),
  city: "Москва",
)

= Введение

Цель работы — получить практические навыки работы с файловой системой Btrfs. Задачи включают управление подразделами (subvolumes), создание и восстановление из снэпшотов, а также настройку дисковых квот.

= Ход работы

== Анализ системы и создание подраздела

С помощью утилит `lsblk` и `df` был определен раздел с Btrfs (`/dev/nvme0n1p3`), смонтированный в `/` и `/home`. Далее были просмотрены существующие подразделы и их свойства.

#figure(image("assets/lsblk.png", width: 90%), caption: [Определение раздела с btrfs])
#figure(image("assets/dfth.png", width: 90%), caption: [Обзор использования дискового пространства])
#figure(image("assets/btrfs-subvolume.png", width: 90%), caption: [Перечисление Btrfs-подразделов])
#figure(image("assets/btrfs params.png", width: 90%), caption: [Проверка свойств подразделов])

Был создан новый подраздел `btrfs-lab`, его владелец изменен с `root` на текущего пользователя, после чего в него был записан тестовый файл.

#figure(image("assets/create-subvol.png", width: 90%), caption: [Создание подраздела и настройка прав])
#figure(image("assets/show-subvolume.png", width: 90%), caption: [Просмотр детальной информации о подразделе])


== Монтирование, снэпшоты и сжатие

Для демонстрации была создана отдельная точка монтирования `/mnt/btrfs-lab` и проверено ее состояние.

#figure(image("assets/create-mount.png", width: 90%), caption: [Создание директории для монтирования])
#figure(image("assets/mount.png", width: 90%), caption: [Проверка точек монтирования Btrfs])

Для проверки работы сжатия были созданы тестовые файлы.

#figure(image("assets/create-files-with-compression.png", width: 90%), caption: [Запись файлов])

Продемонстрирована работа со снэпшотами: создан снимок, внесены изменения в оригинал, затем исходный файл был "испорчен" и успешно восстановлен из снэпшота.

#figure(image("assets/snapshots.png", width: 90%), caption: [Создание снэпшотов, изменение и восстановление файла])

== Управление квотами

Была настроена система квот: активирована (`quota enable`), создана группа (`qgroup create`) и установлен лимит на использование пространства.

#figure(image("assets/quota-activate.png", width: 90%), caption: [Активация квот и создание qgroup])

Попытка превысить установленный лимит с помощью утилиты `dd` привела к ожидаемой ошибке `Disk quota exceeded`, что подтвердило корректную работу механизма.

#figure(image("assets/quota-exceeded.png", width: 90%), caption: [Сообщение об ошибке при превышении квоты])

= Заключение

В ходе работы были освоены ключевые операции с файловой системой Btrfs: управление подразделами, использование снэпшотов для резервного копирования и восстановления данных, а также настройка дисковых квот для ограничения используемого пространства.