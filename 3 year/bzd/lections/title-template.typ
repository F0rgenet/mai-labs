#import "@preview/modern-g7-32:0.2.0": custom-title-template
#import "utils.typ": overlay

#import custom-title-template: *

#let white-block(body) = {
  if (body.has("children") and body.children == ()) { return }
  align(center)[#block(fill: white.transparentize(15%), radius: 10pt, inset: 10pt)[#body]]
}

#let arguments(..args, year: auto) = {
  let args = args.named()
  args.organization = fetch-field(
    args.at("organization", default: none),
    default: (
      full: "Московский авиационный институт",
      short: "Национальный исследовательский университет",
    ),
    ("*full", "short"),
    hint: "организации",
  )
  args.agreed-by = fetch-field(
    args.at("agreed-by", default: none),
    ("name*", "position*", "year"),
    hint: "утверждения",
  )
  args.approved-by = fetch-field(
    args.at("approved-by", default: none),
    ("name*", "position*", "year"),
    hint: "согласования",
  )
  args.stage = fetch-field(
    args.at("stage", default: none),
    ("type*", "num"),
    hint: "этапа",
  )
  args.manager = fetch-field(
    args.at("manager", default: none),
    ("position*", "name*", "title"),
    default: (title: "Руководитель НИР,"),
    hint: "руководителя",
  )

  if args.approved-by.year == auto {
    args.approved-by.year = year
  }
  if args.agreed-by.year == auto {
    args.approved-by.year = year
  }
  return args
}

#let template(
  ministry: none,
  organization: (
    full: "Московский авиационный институт",
    short: "Национальный исследовательский университет",
  ),
  performer: none,
  approved-by: (name: none, position: none, year: auto),
  agreed-by: (name: none, position: none, year: none),
  report-type: "Отчёт",
  about: "О лабораторной работе",
  part: none,
  bare-subject: false,
  research: none,
  subject: none,
  stage: none,
  manager: (position: none, name: none),
  city: none,
) = {
  set page(background: overlay(image("assets/background.png", width: 100%, height: 120%), rgb("#fff").transparentize(85%)))

  set page(footer: context {
    let year = int(datetime.today().display("[year]"))
    white-block[#align(center)[#city #year]]
  })

  white-block[
    #per-line(
      indent: 0pt,
      ministry,
      (
        value: upper(text(size: 18pt)[#organization.full]),
        when-present: organization.full,
      ),
      (
        value: [#upper(organization.short)],
        when-present: organization.short,
      ),
    )
  ]

  white-block[#approved-and-agreed-fields(approved-by, agreed-by)]

  v(1fr)

  white-block[
    #per-line(
      align: center,
      indent: 2fr,
      (value: upper(report-type), when-present: report-type),
      (value: upper(about), when-present: about),
      (value: research, when-present: research),
      (value: [по теме:], when-rule: not bare-subject),
      (value: upper(subject), when-present: subject),
      (
        value: [(#stage.type)],
        when-rule: (stage.type != none and stage.num == none),
      ),
      (
        value: [(#stage.type, этап #stage.num)],
        when-present: (stage.type, stage.num),
      ),
      (value: [\ Книга #part], when-present: part),
    )
  ]

  v(1fr)

  if manager.name != none {
    let title = if type(manager.title) == str and manager.title != "" {
      manager.title + linebreak()
    } else {
      none
    }
    white-block[#sign-field(manager.at("name"), [#title #manager.at("position")])]
  }
  
  if performer != none {
    let title = if type(performer.title) == str and manager.title != "" {
      performer.title + linebreak()
    } else {
      none
    }
    white-block[#sign-field(
      performer.at("name", default: none),
      [#title #performer.at("position", default: none)],
      part: performer.at("part", default: none),
    )]
  }
}