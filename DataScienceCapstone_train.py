#-------------------------------------------------------------------------------
# Name:        NLP projects
# Purpose:
#
# Author:      Nonlining
#
# Created:     04/12/2016
# Copyright:   (c) Nonlining 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

stopwords = []
stopwordFectbit = 1

def ngram(df, n, col):
    global stopwordFectbit
    global stopwords

    word_vectorizer = CountVectorizer(ngram_range=(n,n), analyzer='word', stop_words= 'english')
    sparse_matrix = word_vectorizer.fit_transform(df[col])
    if stopwordFectbit:
        stopwords = word_vectorizer.get_stop_words()
        stopwordFectbit = 0
        print stopwords

    frequencies = sum(sparse_matrix).toarray()[0]
    ngram = pd.DataFrame(frequencies, index=word_vectorizer.get_feature_names(), columns=['frequency'])

    return ngram


def loadfile(filelist , features, size):

    dataframelist = []
    for i in filelist:
        print 'load file' , i
        dataframelist.append(pd.read_table(i, header = None, encoding = 'utf-8'))
        dataframelist[-1].columns = [features]

    weblines = dataframelist[0]
    if len(dataframelist) > 1:
        weblines = weblines.append(dataframelist[1:])#, newslines, how = 'outer')
    np.random.seed(47)

    s = np.random.choice(weblines.index, size, replace = False)
    sampleBlogDF =weblines.ix[s]

    return sampleBlogDF

def ngramModel(data, features):

    unigram = ngram(data, 1, 'description')
    unigram['string'] = unigram.index
    unigram = unigram[unigram.string.str.contains('^[a-zA-Z]+$')]
    #unigram = unigram[unigram['frequency'] > 1]
    unigram.sort(columns = 'frequency',ascending = False ,inplace = True)


    bigram = ngram(data, 2, 'description')
    bigram['string'] = bigram.index
    bigram = bigram[bigram.string.str.contains('^[a-zA-Z]+ +[a-zA-Z]+$')]
    bigram.sort(columns = 'frequency',ascending = False ,inplace = True)


    trigram = ngram(data, 3, 'description')
    trigram['string'] = trigram.index
    trigram = trigram[trigram.string.str.contains('^[a-zA-Z]+ [a-zA-Z]+ [a-zA-Z]+$')]
    trigram.sort(columns = 'frequency',ascending = False ,inplace = True)

    print len(unigram), len(bigram),len(trigram)

    return [unigram, bigram, trigram]


def StrPredict(s1, strlist, models):
    unigramModel = models[0]
    twogramModel = models[1]
    threegramModel = models[2]

    preTwo = s1.split(' ')[-1]

    preThree = s1.split(' ')[-2:]
    preThree =  ' '.join(preThree)
    for i in strlist:
        p1 = 0
        p2 = 0
        p3 = 0
        if sum(unigramModel['string'] == i) > 0 :
            p1 = unigramModel[unigramModel['string'] == i]['frequency']/float(unigramModel['frequency'].sum())
        print (preTwo +' ' +i)
        if sum(twogramModel['string'] == (preTwo +' ' +i)) > 0 :
            p2 = twogramModel[twogramModel['string'] == (preTwo +' ' +i)]['frequency']/float(twogramModel['frequency'].sum())
        print (preThree +' ' +i)
        if sum(threegramModel['string'] == (preThree +' ' +i)) > 0 :
            p3 = threegramModel[threegramModel['string'] == (preThree +' ' +i)]['frequency']/float(threegramModel['frequency'].sum())
        print i, p1, p2 ,p3

def StrPredict(st, anslist, models):
    unigram = models[0]
    bigram  = models[1]
    trigram = models[2]





def Week3():

    filelist = ["K:\\final\\en_US\\en_US.blogs.txt","K:\\final\\en_US\\en_US.news.txt","K:\\final\\en_US\\en_US.twitter.txt" ]

    ngramslist = loadfile(filelist,'description', 5000)

    Q1 = "   ==>The guy in front of me just bought a pound of bacon, a bouquet, and a case of"
    print Q1
    Option1 = ['cheese', 'beer','soda','pretzels']
    StrPredict(Q1, Option1, ngramslist)

    Q2 = "   ==>You're the reason why I smile everyday. Can you follow me please? It would mean the"
    print Q2
    Option2 = ['world', 'universe','best','most']
    StrPredict(Q2, Option2, ngramslist)

    Q3 = "   ==>Hey sunshine, can you follow me and make me the"
    print Q3
    Option3 = ['happiest', 'smellest','saddest','bluest']
    StrPredict(Q3, Option3, ngramslist)

    Q4 = "   ==>Very early observations on the Bills game: Offense still struggling but the"
    print Q4
    Option4 = ['crowd', 'players','referees','defense']
    StrPredict(Q4, Option4, ngramslist)

    Q5 = "   ==>Go on a romantic date at the"
    print Q5
    Option5 = ['beach', 'mall','movies','grocery']
    StrPredict(Q5, Option5, ngramslist)

    Q6 = "   ==>Well I'm pretty sure my granny has some old bagpipes in her garage I'll dust them off and be on my"
    print Q6
    Option6 = ['horse', 'phone','motorcycle','way']
    StrPredict(Q6, Option6, ngramslist)

    Q7 = "   ==>Ohhhhh #PointBreak is on tomorrow. Love that film and haven't seen it in quite some"
    print Q7
    Option7 = ['thing', 'weeks','time','years']
    StrPredict(Q7, Option7, ngramslist)

    Q8 = "   ==>After the ice bucket challenge Louis will push his long wet hair out of his eyes with his little"
    print Q8
    Option8 = ['fingers', 'eyes','toes','ears']
    StrPredict(Q8, Option8, ngramslist)

    Q9 = "   ==>Be grateful for the good times and keep the faith during the"
    print Q9
    Option9 = ['hard', 'bad','sad','worse']
    StrPredict(Q9, Option9, ngramslist)


    Q10 = "   ==>If this isn't the cutest thing you've ever seen, then you must be"
    print Q10
    Option10 = ['insane', 'insensitive','callous','asleep']
    StrPredict(Q10, Option10, ngramslist)


def validationModel(testData, ngramslist, lamda):
    print lamda
    unigram = ngramslist[0]
    bigram = ngramslist[1]
    trigram = ngramslist[2]

    hitCount = 0
    totalData = len(testData)
    for i in testData:
        words = i.split(' ')
        if len(trigram[trigram.string.str.contains('^'+words[0]+' '+words[1]+' .')]) > 0:
            d = trigram[trigram.string.str.contains('^'+words[0]+' '+words[1]+' .')]['frequency'].sum()
            #d = int(bigram.ix[words[0]+' '+words[1]]['frequency'])

            best3string = trigram[trigram.string.str.contains('^'+words[0]+' '+words[1]+' .')].head(3)['string']
            best3stringCount = trigram[trigram.string.str.contains('^'+words[0]+' '+words[1]+' .')].head(3)['frequency']

            maxWord2 = None
            maxWord2P = 0

            for k in range(len(best3string)):
                word2 = best3string[k].split(' ')
                d2 = int(bigram.ix[word2[1]+' '+word2[2]]['frequency'])
                singleWordcount = 0
                if  sum(unigram['string']== word2[2]) > 0:
                    singleWordcount = int(unigram[unigram['string']== word2[2]]['frequency'])

                p = lamda[0]*singleWordcount/float(len(unigram)) + lamda[1]*d2/float(singleWordcount) + lamda[2]*best3stringCount[k]/float(d)
                if p > maxWord2P:
                    maxWord2P = p
                    maxWord2 = word2[2]

            if maxWord2 == words[2]:
                print maxWord2
                hitCount = hitCount + 1
    return hitCount/float(totalData)


def LinearInter_trainData():

    filelist = ["K:\\final\\en_US\\en_US.blogs.txt","K:\\final\\en_US\\en_US.news.txt","K:\\final\\en_US\\en_US.twitter.txt" ]

    data = loadfile(filelist,'description', 10000)
    print len(data)
    msk = np.random.rand(len(data)) < 0.8
    train = data[msk]
    print 'train set ', len(train)
    test =  data[~msk]
    print 'test set ', len(test)

    ngramslist = ngramModel(train, 'description')

    testData = ngram(test, 3, 'description')
    testData['string'] = testData.index
    testData = testData[testData.string.str.contains('^[a-zA-Z]+ [a-zA-Z]+ [a-zA-Z]+$')]

    testData = list(testData.index)

    v1 = validationModel(testData, ngramslist, lamda = [.5, .3 , .2])
    v2 = validationModel(testData, ngramslist, lamda = [.6, .3 , .1])
    v3 = validationModel(testData, ngramslist, lamda = [.4, .3 , .3])
    v4 = validationModel(testData, ngramslist, lamda = [.33, .33 ,.33])
    v5 = validationModel(testData, ngramslist, lamda = [.3, .3 , .4])
    v6 = validationModel(testData, ngramslist, lamda = [.2, .3 , .5])
    v7 = validationModel(testData, ngramslist, lamda = [.1, .3 , .6])
    print v1, v2, v3, v4, v5, v6, v7
    # 0.00489059556586 0.00481814229822 0.00489059556586 0.00489059556586 0.00489059556586 0.00485436893204 0.00489059556586
    # 0.00464522122866 0.00460651105176 0.00468393140557 0.00468393140557 0.00468393140557 0.00464522122866 0.00468393140557
    # 0.00909995132584 0.00899413793833 0.00912111400334 0.00914227668085 0.00914227668085 0.00914227668085 0.00914227668085 (10000 size)

def KatzBOO(ngrams, discounts, words, tp = 5):
    unigram = ngrams[0]
    bigram = ngrams[1]
    trigram = ngrams[2]
    totoalUnigramSum = unigram['frequency'].sum()
    bigramsDiscount = discounts[0]
    trigramDiscount = discounts[1]
    resultAll = unigram.head(10)
    result_bigram = bigram[bigram.string.str.contains('^'+words[1]+' .')]
    result_trigram = trigram[trigram.string.str.contains('^'+words[0]+' '+words[1]+' .')]
    bigram_a = 1.
    trigram_a = 1.

    if len(result_bigram) > 0:
        totalBigramSum = result_bigram['frequency'].sum()
        bigram_a = bigramsDiscount*len(result_bigram)/float(result_bigram['frequency'].sum())
        resultAll['frequency'] = resultAll['frequency']*bigram_a/totoalUnigramSum
        result_bigram['frequency'] = (result_bigram['frequency'] - bigramsDiscount)/totalBigramSum
        result_bigram.index = [i.split(' ')[1] for i in list(result_bigram.index)]
        #print result_bigram
        resultAll = resultAll.append(result_bigram)

    if len(result_trigram) > 0:
        totalTrigramSum = result_trigram['frequency'].sum()
        trigram_a = trigramDiscount*len(result_trigram)/float(result_trigram['frequency'].sum())

        resultAll['frequency'] = resultAll['frequency']*trigram_a/resultAll['frequency'].sum()
        result_trigram['frequency'] = (result_trigram['frequency'] - trigramDiscount)/totalTrigramSum
        result_trigram.index = [i.split(' ')[2] for i in list(result_trigram.index)]

        resultAll = resultAll.append(result_trigram)

    return resultAll


def Smoothing_trainData():

    discounts = [0.5, 0.5]

    filelist = ["K:\\final\\en_US\\en_US.blogs.txt","K:\\final\\en_US\\en_US.news.txt","K:\\final\\en_US\\en_US.twitter.txt" ]

    data = loadfile(filelist,'description', 6000)
    print len(data)
    msk = np.random.rand(len(data)) < 0.8
    train = data[msk]
    print 'train set ', len(train)
    test =  data[~msk]
    print 'test set ', len(test)

    ngramslist = ngramModel(train, 'description')
    print 'training size ',len(ngramslist[0]),len(ngramslist[1]),len(ngramslist[2])


    testData = ngram(test, 3, 'description')
    testData['string'] = testData.index
    testData = testData[testData.string.str.contains('^[a-zA-Z]+ [a-zA-Z]+ [a-zA-Z]+$')]

    testData = list(testData.index)
    #discountList = [[0.2,0.8],[0.3,0.7],[0.4,0.6],[0.5,0.5],[0.6,0.4],[0.7,0.3],[0.8,0.2],[0.3,0.3],[0.4,0.4],[0.6,0.6],[0.7,0.7]]
    discountList = [[0.2,0.8],[0.6, 0.4]]
    # [0.023696877442711976, 0.023696877442711976, 0.023696877442711976, 0.023696877442711976, 0.023696877442711976, 0.023696877442711976, 0.023696877442711976, 0.023696877442711976, 0.023696877442711976, 0.023696877442711976, 0.023696877442711976]
    # [0.0249817334121986] for 10000 sample size (0.5, 0.5)
    # [0.0249817334121986, 0.0249817334121986]



    acclist = []
    for d in discountList:
        hit = 0
        print d

        for i in testData:

            w = i.split(' ')
            pred = KatzBOO(ngramslist, discounts, [w[0],w[1]])
            pred.sort(columns = 'frequency',ascending = False ,inplace = True)

            if len(pred) > 0:
                pred_list = list(pred.index)
                if w[2] in pred_list[0]:
                    hit = hit + 1
                    print i, d , hit/float(len(testData))

        acclist.append(hit/float(len(testData)))

    print acclist

def PredictNextWord(str, anslist, models, discounts):
    trigram = models[2]
    bigram  = models[1]
    unigram = models[0]

    str = str.lower()
    s1split = str.split(' ')

    newStr = []
    for s in s1split:
        if s not in stopwords:
            newStr.append(s)
    print newStr

    preThree = newStr[-2:]

    preThree =  ' '.join(preThree)
    plist = dict()

    totoalUnigramSum = unigram['frequency'].sum()
    bigramsDiscount = discounts[0]
    trigramDiscount = discounts[1]




    for i in anslist:

        bigram_a = 1.
        trigram_a = 1.
        result_unigram = unigram[unigram['string'] == i]
        result_bigram = bigram[bigram.string.str.contains('^'+newStr[-1]+' .')]
        result_trigram = trigram[trigram.string.str.contains('^'+newStr[-2]+' '+newStr[-1]+' .')]
        print newStr[-2]+' '+newStr[-1] +' '+i

        if len(result_trigram[result_trigram['string'] == preThree+' '+i]) > 0:
            totalTrigramSum = result_trigram['frequency'].sum()
            plist[i] = float(result_trigram[result_trigram['string'] == preThree+' '+i]['frequency'] - trigramDiscount)/totalTrigramSum
            print "3 " + preThree+' '+i
            continue
        elif len(result_trigram) > 0:
            totalTrigramSum = result_trigram['frequency'].sum()
            trigram_a = trigramDiscount*len(result_trigram)/float(result_trigram['frequency'].sum())

        if len(result_bigram[result_bigram['string'] == newStr[-1]+' '+i]) > 0:
            totalBigramSum = result_bigram['frequency'].sum()
            #print result_bigram[result_bigram['string'] == newStr[-1]+' '+i]['frequency']
            plist[i] = trigram_a*float(result_bigram[result_bigram['string'] == newStr[-1]+' '+i]['frequency'] - bigramsDiscount)/totalBigramSum
            print "2 " + preThree+' '+i
            continue
        elif len(result_bigram) > 0:
            totalBigramSum = result_bigram['frequency'].sum()
            bigram_a = bigramsDiscount*len(result_bigram)/float(totalBigramSum)


        if len(result_unigram) > 0:
            plist[i] = float(bigram_a*trigram_a*result_unigram['frequency'])/totoalUnigramSum


    maxValue = 0
    maxItem = None

    for i in plist:
        if plist[i] > maxValue:
            maxValue = plist[i]
            maxItem = i
    print plist
    print maxItem, maxValue



def Week4():

    discounts = [0.5, 0.5]

    filelist = ["K:\\final\\en_US\\en_US.blogs.txt","K:\\final\\en_US\\en_US.news.txt","K:\\final\\en_US\\en_US.twitter.txt" ]

    data = loadfile(filelist,'description', 10000)
    ngramslist = ngramModel(data, 'description')

    discount = [0.5 , 0.5]

    Q1 = "When you breathe, I want to be the air for you. I'll be there for you, I'd live and I'd"
    A1 = ["sleep" ,"die","eat","give"]

    PredictNextWord(Q1, A1, ngramslist, discount)

    Q2 = "Guy at my table's wife got up to go to the bathroom and I asked about dessert and he started telling me about his"
    A2 = ["financial" ,"horticultural","marital", "spiritual"]

    PredictNextWord(Q2, A2, ngramslist, discount)

    Q3 = "I'd give anything to see arctic monkeys this"
    A3 = ["decade", "weekend" ,"morning" ,"month"]
    PredictNextWord(Q3, A3, ngramslist, discount)

    Q4 = "Talking to your mom has the same effect as a hug and helps reduce your"
    A4 = ["happiness", "sleepiness" ,"stress" ,"hunger"]
    PredictNextWord(Q4, A4, ngramslist, discount)

    Q5 = "When you were in Holland you were like 1 inch away from me but you hadn't time to take a"
    A5 = ["look", "picture" ,"minute" ,"walk"]
    PredictNextWord(Q5, A5, ngramslist, discount)

    Q6 = "I'd just like all of these questions answered, a presentation of evidence, and a jury to settle the"
    A6 = ["matter", "account" ,"case" ,"incident"]
    PredictNextWord(Q6, A6, ngramslist, discount)

    Q7 = "I can't deal with unsymetrical things. I can't even hold an uneven number of bags of groceries in each"
    A7 = ["toe", "finger" ,"arm" ,"hand"]
    PredictNextWord(Q7, A7, ngramslist, discount)

    Q8 = "Every inch of you is perfect from the bottom to the"
    A8 = ["middle", "side" ,"top" ,"center"]
    PredictNextWord(Q8, A8, ngramslist, discount)

    Q9 = "I'm thankful my childhood was filled with imagination and bruises from playing"
    A9 = ["weekly", "outside" ,"daily" ,"inside"]
    PredictNextWord(Q9, A9, ngramslist, discount)

    Q10 = "I like how the same people are in almost all of Adam Sandler"
    A10 = ["movies", "pictures" ,"stories" ,"novels"]
    PredictNextWord(Q10, A10, ngramslist, discount)


if __name__ == '__main__':
    Smoothing_trainData()
    #LinearInter_trainData()
    #Week4()


