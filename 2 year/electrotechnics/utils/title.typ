#import "@preview/modern-g7-32:0.1.0": custom-title-template
#import custom-title-template: *

#let arguments(..args, year: auto) = {
  let args = args.named()
  args.organization = fetch-field(
      args.at("organization", default: none), 
      default: (
          full: "Московский авиационный институт", 
          short: "Национальный исследовательский университет"), 
      ("*full", "short"), 
      hint: "организации"
  )
  args.approved-by = fetch-field(
      args.at("approved-by", default: none),
      ("name*", "position*", "year"),
      default: (year: auto),
      hint: "согласования"
  )
  args.agreed-by = fetch-field(
      args.at("agreed-by", default: none),
      ("name*", "position*", "year"),
      default: (year: auto),
      hint: "утверждения"
  )
  args.stage = fetch-field(args.at(
      "stage", default: none),
      ("type*", "num"),
      hint: "этапа"
  )
  args.manager = fetch-field(
      args.at("manager", default: none),
      ("position*", "name*"),
      hint: "руководителя"
  )

  if args.approved-by.year == auto {
      args.approved-by.year = year
  }
  if args.agreed-by.year == auto {
      args.agreed-by.year = year
  }
  return args
}

#let template(
  ministry: none,
  organization: (
      full: "Московский авиационный институт", 
      short: "Национальный исследовательский университет"
  ),
  institute: (number: none, name: none),
  department: (number: none, name: none),
  udk: none,
  research-number: none,
  report-number: none,
  approved-by: (name: none, position: none, year: auto),
  agreed-by: (name: none, position: none, year: none),
  part: none,
  research: none,
  subject: none,
  stage: none,
  manager: (position: none, name: none),
  performer: none,
) = {
  per-line(
    indent: none,
    ministry,
    (value: upper(text(size: 18pt)[#organization.full]),
        when-present: organization.full),
    (value: [#upper(organization.short)], 
        when-present: organization.short),
  )

  v(1fr)

  per-line(
      indent: v(2fr),
      align: center,
      (value: [Институт №#institute.number – «#institute.name»],
          when-present: (institute.number, institute.name)),
      (value: [Кафедра #department.number – «#department.name»],       
          when-present: (department.number, department.name)),
  )

  per-line(
    text(size: 16pt)[Кафедра Теоретической электротехники],
    text(size: 14pt)[Лаборатория ТОЭ]
  )

  approved-and-agreed-fields(approved-by, agreed-by)

  per-line(
      align: center,
      indent: v(2fr),
      upper([отчёт по работе №#report-number]),
      (value: research, when-present: research),
      (value: upper(subject), when-present: subject),
      (
          value: [(#stage.type)],
          when-rule: (stage.type != none and stage.num == none)),
      (
          value: [(#stage.type, этап #stage.num)], 
          when-present: (stage.type, stage.num)
      ),
      (value: [\ Книга #part], when-present: part),
  )

  if manager.name != none {
      sign-field(manager.at("name"), [Принял:\ #manager.at("position")])
  }

  if performer != none {
      sign-field(performer.at("name", default: none), [Выполнил:\ #performer.at("position", default: none)], part: performer.at("part", default: none))
  }

  v(0.5fr)
}