# Capstone Project
# 12/23/2016
# Min-Jung Wang
# lib for Shiny APP 

rm(list=ls())
gc()

WD <- getwd()
if (!is.null(WD)) setwd(WD)
options(java.parameters = "- Xmx10240m")
library(tm) 
library(RWeka)

DEBUG = FALSE

PredictWord <- function(word, dictionary){  

  reverse <- rev(strsplit(word, split=" ")[[1]])
  
  word <- reverse[1]

  sub = dictionary[ with(dictionary,  grepl(paste('^',word, sep =""), terms)),]
  
  temp = sub[order(-sub$counts),]
  
  count = dim(temp)[1]
  if (count > 5)
    count = 5
  res = temp[1:count,]$terms
  
  if(DEBUG) {print(res)}
  
  return(res)
}


PredictnextWord <- function(sentence, df1, df2, df3, local_unigram, local_Bigram, local_Trigram){

  reverse <- rev(strsplit(sentence, split=" ")[[1]])
  
  if(length(reverse)==0){
    rc <- df1[order(-df1$Pcont),][1:3,]$term
    return(rc)
  }
  
  second <- reverse[1]
  first <- reverse[2]
  bigram <- paste(first, second)
  

  if(sum(df3$pre==bigram)!=0 | dim(local_Trigram[with(local_Trigram,grepl(paste('^',bigram, sep =""), terms)),])[1] != 0){
    
    if(DEBUG) {cat("using trigram\n")}
    
    a <- df3[df3$pre==bigram,]
    resTemp <- a[order(-a$PKN),][1:10,]

    resTemp$p <- 0.4*resTemp$PKN/sum(resTemp[!is.na(resTemp$PKN),]$PKN)
    
    tempTri <-local_Trigram[with(local_Trigram,grepl(paste('^',bigram, sep =""), terms)),]

    tempTri$p = 0.6*tempTri$counts/sum(tempTri$counts)
    resTemp <- resTemp[keeps <- c("terms", "counts", "p", "end")]

    ##################### remove duplicated items ###################
    
    r <- intersect(resTemp$end, tempTri$end)
    # remove duplicated item between local bigram and global trained bigram
    diff <- setdiff(resTemp$end,tempTri$end)
    diff2 <- setdiff(tempTri$end, resTemp$end)
    rightside <- resTemp[which(resTemp$end %in% r),]
    leftside <- tempTri[which(tempTri$end %in% r),]
    # leave the bigger proba. 
    resTempBigger <- rightside[rightside$p > leftside$p,]
    tempBiBigger <- leftside[rightside$p < leftside$p,]
    
    resTemp <- rbind(resTemp[which(resTemp$end %in% diff),], tempTri[which(tempTri$end %in% diff),])
    resTemp <- rbind(resTemp, tempTri[which(tempTri$end %in% diff2),])
    
    resTemp <- rbind(resTemp, resTempBigger)
    resTemp <- rbind(resTemp, tempBiBigger)
    
    ##################### remove duplicated items ###################

    
    resTemp <- resTemp[order(-resTemp$p),][1:5,]
    
    if(DEBUG) {print(resTemp)}
    
    rc <- resTemp$end
    
  }else if(sum(df2$start==second)!=0 | dim(local_Bigram[with(local_Bigram,grepl(paste('^',second, sep =""), terms)),])[1] != 0){
    if(DEBUG) {cat("using bigram\n")}
    
    a <- df2[df2$start==second,]
    resTemp <- a[order(-a$Pcont2),][1:10,]
    
    resTemp$p <- 0.4*resTemp$Pcont2/sum(resTemp[!is.na(resTemp$Pcont2),]$Pcont2)
    
    tempBi <-local_Bigram[with(local_Bigram,grepl(paste('^',second, sep =""), terms)),]
    
    tempBi$p = 0.6*tempBi$counts/sum(tempBi$counts)
    
    resTemp <- resTemp[keeps <- c("terms", "counts", "p", "end")]
    
    ##################### remove duplicated items ###################
    
    r <- intersect(resTemp$end, tempBi$end)
    # remove duplicated item between local bigram and global trained bigram
    diff <- setdiff(resTemp$end,tempBi$end)
    diff2 <- setdiff(tempBi$end, resTemp$end)
    rightside <- resTemp[which(resTemp$end %in% r),]
    leftside <- tempBi[which(tempBi$end %in% r),]
    # leave the bigger proba. 
    resTempBigger <- rightside[rightside$p > leftside$p,]
    tempBiBigger <- leftside[rightside$p < leftside$p,]
    
    resTemp <- rbind(resTemp[which(resTemp$end %in% diff),], tempBi[which(tempBi$end %in% diff),])
    resTemp <- rbind(resTemp, tempBi[which(tempBi$end %in% diff2),])
    
    resTemp <- rbind(resTemp, resTempBigger)
    resTemp <- rbind(resTemp, tempBiBigger)
    
    ##################### remove duplicated items ###################
    
    resTemp <- resTemp[order(-resTemp$p),][1:5,]    
    
    if(DEBUG) {print(resTemp)}
    rc  <- resTemp$end
  }else{
    if(DEBUG) {cat("using unigram\n")}
    resTemp <- df1[order(-df1$Pcont),][1:5,]
    
    # using local unigram to recalculate prob.
    # I use weight 0.6 to local unigram and 0.4 for unigram that I trained from web data
    
    resTemp$p <- 0.6*resTemp$Pcont/sum(resTemp$Pcont)
    local_unigram$p = 0.4*local_unigram$counts/sum(local_unigram$counts)
	
    resTemp <- resTemp[keeps <- c("terms", "counts", "p")]

    resTemp <- rbind(resTemp, local_unigram)
    
    resTemp <- resTemp[order(-resTemp$p),][1:5,]
    
    if(DEBUG) {print(resTemp)}
    # It can increaing 'the' with more local data 

    rc <- resTemp$terms
  }

  # filling out space
  # too many 'the'
  if(is.na(rc[1])) {
    rc <- df1[order(-df1$Pcont),][1:5,]$terms
  }else if(is.na(rc[2])){
    rc[2:5] <- df1[order(-df1$Pcont),][1:4,]$terms
  }else if(is.na(rc[3])){
    rc[3:5] <- df1[order(-df1$Pcont),][1:3,]$terms
  } else if(is.na(rc[4])){
    rc[4:5] <- df1[order(-df1$Pcont),][1:2,]$terms
  } else if(is.na(rc[5])){
    rc[5] <- df1[order(-df1$Pcont),][1,]$terms
  }
  
  return(rc)
}
