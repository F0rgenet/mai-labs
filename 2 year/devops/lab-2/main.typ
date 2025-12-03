#import "@preview/codly:1.3.0": *
#import "@preview/codly-languages:0.1.1": *
#import "@preview/modern-g7-32:0.1.0": gost, abstract, title-templates, structure-heading, annexes

#codly(zebra-fill: none, display-name: false, display-icon: false, number-format: none)

#show figure: set block(breakable: true)

#show: codly-init.with()

#show: gost.with(
  title-template: title-templates.mai-university-lab,
  performers: (
    (name: "Елисеев П.А.", position: "Студент М3О-221Б-23"),
  ),
  institute: (number: 3, name: "Системы управления, информатика и электроэнергетика"),
  department: (number: 307, name: "Цифровые технологии и информационные системы"),
  report-type: [Лабораторная работа №2],
  about: [По дисциплине "Администрирование linux"],
  bare-subject: true,
  subject: "Работа с файловыми системами и разделами диска в Linux",
  manager: (name: "Боровской К.И.", position: "Ассистент кафедры 307"),
  city: "Москва",
  pagebreaks: false,
)

#outline()

#pagebreak()

= Введение

*Цели рабооты:*
1.  Освоить методику расширения дискового пространства для виртуальной машины.
2.  Получить практические навыки изменения размера разделов диска и файловых систем в Linux.
3.  Научиться использовать режим восстановления (rescue mode) для выполнения низкоуровневых операций с диском.

= Ход работы

== Начальная настройка и установка ОС

Установлена ОС Debian с одним корневым разделом (`/`). Зафиксировано исходное состояние диска.

#figure(image("assets/vm.png", width: 90%), caption: [Виртуальная машина с Debian])
#figure(image("assets/lsblk.png", width: 90%), caption: [Исходное состояние разделов диска (`lsblk`)])

== Расширение дискового пространства

Размер виртуального жесткого диска увеличен в настройках гипервизора.

#figure(image("assets/setsize.png", width: 60%), caption: [Увеличение размера виртуального диска])
#figure(image("assets/lsblk-after.png", width: 90%), caption: [Состояние диска после увеличения в гипервизоре (до rescue mode)])

== Работа в режиме восстановления (Rescue Mode)

Виртуальная машина загружена в "Rescue mode".

#figure(image("assets/rescue.png", width: 90%), caption: [Вход в командную оболочку в Rescue mode])

== Изменение размера раздела с помощью parted

С помощью `parted /dev/vda` удалены разделы `/dev/vda6` (логический), `/dev/vda5` (swap) и `/dev/vda2` (расширенный). Затем корневой раздел `/dev/vda1` расширен до конца диска (`resizepart 1 100%` или `resizepart 1 24.7GB`). Скриншот `assets/parted.png` показывает состояние таблицы разделов до этих изменений, но после увеличения диска в гипервизоре.

#figure(image("assets/parted.png", width: 90%), caption: [Таблица разделов в `parted` до изменения размера корневого раздела])

== Изменение размера файловой системы с resize2fs

Утилита `resize2fs /dev/vda1` применена для расширения файловой системы `ext4`. Команда сообщила "nothing to do", что указывает на возможное автоматическое расширение или осведомленность ядра о новом размере раздела.

#figure(image("assets/resize2fs.png", width: 90%), caption: [Вывод команды `resize2fs /dev/vda1`])

= Проверка результатов

После перезагрузки в обычном режиме, команда `df -h` подтвердила успешное увеличение размера корневой файловой системы.

#figure(image("assets/df-h.png", width: 90%), caption: [Результат `df -h` после всех операций])

= Заключение

В ходе работы освоена методика расширения дискового пространства виртуальной машины Linux. С использованием `parted` в rescue mode изменен размер корневого раздела, а `resize2fs` использована для файловой системы.