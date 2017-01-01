WD <- getwd()
if (!is.null(WD)) setwd(WD)

smallData = FALSE

set.seed(1000)

sampleRatio <- 0.6

if(smallData){
  sampleRatio=.020
}


conTwitter <- file("k://final//en_US//en_US.twitter.txt", "r")
length <- length(dataTwitter <- readLines(conTwitter, encoding="UTF-8", warn = FALSE))
while (length > 0) {
  
  sampleData1 <- sample(dataTwitter,length*sampleRatio)
  if(smallData){
    write(sampleData1,"D:\\Dropbox\\Coursera\\Data Science\\10_Capstone\\DataSet\\SamllDataSetTwiiter.txt",append=TRUE)
  } else {  
    write(sampleData1,"D:\\Dropbox\\Coursera\\Data Science\\10_Capstone\\BigDataSet\\DataSetTwiiter.txt",append=TRUE)
  }
  
  length <- length(dataTwitter <- readLines(conTwitter, encoding="UTF-8", warn = FALSE))
}


conUSBlogs <- file("k://final//en_US//en_US.blogs.txt", "r")
length <- length(dataUSBlogs <- readLines(conUSBlogs, encoding="UTF-8" , warn = FALSE))

while (length> 0) {
  sampleData1 <- sample(dataUSBlogs,length*sampleRatio)
  
  if(smallData){
    write(sampleData1,"D:\\Dropbox\\Coursera\\Data Science\\10_Capstone\\DataSet\\SamllDataSetBlog.txt",append=TRUE)
  } else {  
    write(sampleData1,"D:\\Dropbox\\Coursera\\Data Science\\10_Capstone\\BigDataSet\\DataSetBlog.txt",append=TRUE)
  }
  
  length <- length(dataUSBlogs <- readLines(conUSBlogs, encoding="UTF-8", warn = FALSE))
}

conUSNews <- file("k://final//en_US//en_US.news.txt", "r")
length<- length(dataUSNews <- readLines(conUSNews, encoding="UTF-8", warn = FALSE)) 
while (length> 0) {
  sampleData1 <- sample(dataUSNews,length*sampleRatio)
  
  if(smallData){
    write(sampleData1,"D:\\Dropbox\\Coursera\\Data Science\\10_Capstone\\DataSet\\SamllDataSetUSNews.txt",append=TRUE)
  } else {  
    write(sampleData1,"D:\\Dropbox\\Coursera\\Data Science\\10_Capstone\\BigDataSet\\DataSetUSNews.txt",append=TRUE)
  }
  
  
  length<- length(dataUSNews <- readLines(conUSNews, encoding="UTF-8", warn = FALSE)) 
}

close(conUSNews)
close(conUSBlogs)
close(conTwitter)
