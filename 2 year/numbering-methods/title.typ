#import "@preview/modern-g7-32:0.1.0": gost, title-templates

#set page(paper: "a5")

#show: gost.with(
  title-template: title-templates.mai-university-lab,
  performers: (
    (name: "Лисняк А.О.", position: "Студент М3О-221Б-23"),
  ),
  manager: (name: "Зверев Н.А.", position: "Доцент каф. 311"),
  institute: (number: 3, name: "Системы управления, информатика и электроэнергетика"),
  department: (number: 311, name: "Прикладные программные средства и математические методы"),
  about: [О лабораторных работах],
  bare-subject: true,
  subject: [По дисциплине "Численные методы"\ \ Вариант №9],
  city: "Москва",
  text-size: (default: 9pt, small: 5pt),
  pagebreaks: false,
  margin: (left: 15mm, right: 5mm, top: 10mm, bottom: 10mm),
)