# Data Science Project Shiny APP
# Min-Jung Wang
library(shiny)
library(datasets)
library(stringi)

# load library files for this project
source("CapstoneProjectlib.R")

datadir <- "."

load(file=paste(datadir, "DataUnigram.data",  sep="/"), verbose=T)
load(file=paste(datadir, "DataBigram.data", sep="/"), verbose=T)
load(file=paste(datadir, "DataTrigram.data", sep="/"), verbose=T)

# local unigram bigram ,and trigram for online training data

local_Unigram <- data.frame(terms=character(),
                 counts=as.integer(character()),
                 stringsAsFactors=FALSE)

local_Bigram <- data.frame(terms=character(),
                            counts=as.integer(character()),
                            end=character(),
                            stringsAsFactors=FALSE) 				 

local_Trigram <- data.frame(terms=character(),
                            counts=as.integer(character()),
                            end=character(),
                            stringsAsFactors=FALSE) 


t_unigram <- trained_unigram
t_bigram <- trained_bigram
t_trigram <- trained_trigram

trim.leading <- function (x)  sub("^\\s+", "", x)
myTolower <- function(x) stri_trans_tolower(x, "en_US")

getPrediction <-function(string, df1, df2, df3 ,tolower=T){
  if(tolower){
    string <- myTolower(string)
  }
    
  if(substr(string, nchar(string),nchar(string)) == " "){
    reverse <- rev(strsplit(string, split=" ")[[1]])
    
    if(!is.na(reverse[2])){
      biString = paste(reverse[2],reverse[1], sep =" ")
    }
    
    if(!is.na(reverse[3])){
      triString = paste(reverse[3], paste(reverse[2],reverse[1], sep =" "), sep =" ")
    }
    
    # function to predict next word 
    res <- PredictnextWord(string, df1, df2, df3, local_Unigram, local_Bigram, local_Trigram)
    
    # online data save to local file
    # for unigram -------------------------------------------------------------
    if(sum(local_Unigram$terms == reverse[1]) != 0){
      local_Unigram[local_Unigram$terms == reverse[1], ]$counts <<- 1 + local_Unigram[local_Unigram$terms == reverse[1], ]$counts 
    } else {
      newRow <- data.frame(terms=reverse[1],counts = 1)
      local_Unigram <<- rbind(local_Unigram, newRow)
    }
    # for bigram --------------------------------------------------------------
    if(!is.na(reverse[2])){
      if(sum(local_Bigram$terms == biString) != 0){
        local_Bigram[local_Bigram$terms == biString, ]$counts <<- 1 + local_Bigram[local_Bigram$terms == biString, ]$counts 
      } else {
        newRow <- data.frame(terms=biString,counts = 1, end = reverse[1])
        local_Bigram <<- rbind(local_Bigram, newRow)
      }
    }
    # for trigram -------------------------------------------------------------
    if(!is.na(reverse[3])){
       if(sum(local_Trigram$terms == triString) != 0){
         local_Trigram[local_Trigram$terms == triString, ]$counts <<- 1 + local_Trigram[local_Trigram$terms == triString, ]$counts 
       } else {
         newRow <- data.frame(terms=triString,counts = 1, end = reverse[1])
         local_Trigram <<- rbind(local_Trigram, newRow)
       }
    }
    
    return(res)
  
  }else if (string == ""){
    
    return ("")
  
  }else {
    # incompleted string to predict word
    res <- PredictWord(string, trained_unigram)
    return(res)
  
  }
}

# Define server logic required to summarize and view the selected
# dataset
shinyServer(function(input, output, session) {
  
  updateString <- function(val) updateTextInput(session, "inputText", value = val)

  output$inputText <- renderText({
    
    res <- getPrediction(input$inputText, t_unigram, t_bigram, t_trigram, tolower=T)

    res <- paste(res, collapse=" , ")
    
    paste0("  ", res)

  })

  
})