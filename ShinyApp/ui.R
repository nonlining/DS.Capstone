library(shiny)
boxstyle <- "border: 1px solid;box-shadow: 1px 1px 1px #FF0000;"


shinyUI(fluidPage(

  titlePanel("Data Science Project"),
  
  mainPanel(
    textInput("inputText",  "A text box:(must press space key to predict the next word)", width = '100%'), 
    br(),
    div(textOutput("inputText"), style=boxstyle),
    br(),
    h2("Functionalities:"),
    p("1. Predict Next Word (must press space key to predict the next word)"),
    p("2. Predict word with incomplete string"),
    p("3. Using local data to train model (it will save unigram , bigram and trigram temporarily, after closing the windows all models will be disappeared)"),
    p("Source code: https://github.com/nonlining/DS.Capstone ")

  )
))