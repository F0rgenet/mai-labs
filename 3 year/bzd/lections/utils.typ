#let overlay(img, color) = layout(bounds => {
  let size = measure(img, ..bounds)
  img
  place(top + left, block(..size, fill: color))
})