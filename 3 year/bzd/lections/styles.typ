#import "utils.typ": overlay

#let style(it) = {
  show table: set par(justify: false)
  show table: set text(size: 13pt)

  set page(background: [
    #overlay(image("assets/background.png", height: 100%, width: 100%, fit: "cover"), rgb("#fff").transparentize(15%))
  ])

  let title = [Безопасность жизнидеятельности]

  set page(paper: "a4", margin: (y: 4em), header: context {
    set par(spacing: 10pt)
    align(center)[#title]
    line(length: 100%)
  })

  it
}

#let info(text) = {
  rect(inset: 10pt, width: 100%, radius: 5pt, stroke: rgb(36, 36, 166))[#text]
}