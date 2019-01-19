#Importing the libraries
import pandas as pd
import string as STR
import sys


#using the from command to import necessary modules
from os import listdir as LDR
from sklearn.feature_extraction.text import CountVectorizer as CnVt
from sklearn.linear_model import SGDClassifier as SGDC
from sklearn.feature_extraction.text import TfidfVectorizer as TfVt


#defining training path for terminal
#and #defining test path
train_path = "../resource/lib/publicdata/aclImdb/train/"     # use terminal to ls files under this directory
test_path = "../resource/lib/publicdata/imdb_te.csv"         # test data for grade evaluation

#train_path = "C:/Programming/EDX/MicroMaster/MicroMaster ColumbiaX Artificial Intelligence/Modules/Artificial Intelligence/My solutions/Project 5/"
#test_path = "C:/Programming/EDX/MicroMaster/MicroMaster ColumbiaX Artificial Intelligence/Modules/Artificial Intelligence/My solutions/Project 5/"

#defining Stop_Words func
StpWrds = open("stopwords.en.txt", "r", encoding = "utf8")
Stop_Words = StpWrds.read()

StpWrds.close()
Stop_Words = Stop_Words.split("\n")

#defining the way we are going to do it
def Way2do(string_set):
    #defining shobdo as the string set
    Shobdo = string_set
    Shobdo = Shobdo.replace("<br />", " ")
    Shobdo = Shobdo.rstrip()
    replace = str.maketrans(STR.punctuation, ' '*len(STR.punctuation))
    #translate and replace
    Shobdo = Shobdo.translate(replace)
    Shobdo = Shobdo.lower()
    Shobdo = Shobdo.split()
    Shobdo = [SH for SH in Shobdo if SH not in Stop_Words]
    Shobdo = ' '.join(Shobdo)

    return Shobdo

#defining the function for preprocessing
def imdb_data_preprocess(inpath, outpath="./", name="imdb_tr.csv", mix=False):
    fil_open = open(name, "w", encoding = 'utf8')
    fil_open.write("row_number,text,polarity\n")
    '''Implement this module to extract
    combine text files under train_path directory into 
    imdb_tr.csv. Each text file in train_path should be stored 
    as a row in imdb_tr.csv. And imdb_tr.csv should have two 
    columns, "text" and label'''

    #creating the counter
    Cnter = 0
    
    #creating the for loops
    for text in LDR(inpath + "pos"):
        fil_in = open(inpath + "pos/" + text, "r", encoding = 'utf8')
        text = Way2do(fil_in.read())
        fil_open.write(str(Cnter) + "," + text + ",1" + "\n")
        Cnter += 1
        fil_in.close()
    
    #2nd loop
    for text in LDR(inpath + "neg"):
        fil_in = open(inpath + "neg/" + text, "r", encoding = 'utf8')
        text = Way2do(fil_in.read())
        fil_open.write(str(Cnter) + "," + text + ",0" + "\n")
        Cnter += 1
        fil_in.close()
    pass


#creating the main 
if "__main__" == __name__:
    imdb_data_preprocess(train_path)

    Training_data = pd.read_csv("imdb_tr.csv")
    
    Test_Set = pd.read_csv(test_path, encoding="ISO-8859-1")
    Test_Set['text'] = Test_Set['text'].apply(Way2do)

    '''train a SGD classifier using unigram representation,
    predict sentiments on imdb_te.csv, and write output to
    unigram.output.txt'''
    Vcounter = CnVt(stop_words = Stop_Words)
    TrainNTransform = Vcounter.fit_transform(Training_data['text'])
    
    ClassifieR = SGDC(loss = "hinge", penalty = "l1")
    ClassifieR.fit(TrainNTransform, Training_data['polarity'])

    # test set 
    #classification for the outputs
    TestNTransform = Vcounter.transform(Test_Set['text'])
    fin_Res = ClassifieR.predict(TestNTransform)
    with open("unigram.output.txt", "w") as f:
        for FIN in fin_Res:
            f.write(str(FIN) + "\n")


    '''train a SGD classifier using bigram representation,
    predict sentiments on imdb_te.csv, and write output to
    bigram.output.txt'''
    Vcounter = CnVt(stop_words = Stop_Words, ngram_range = (1, 2))
    TrainNTransform = Vcounter.fit_transform(Training_data['text'])
    
    ClassifieR = SGDC(loss = "hinge", penalty = "l1")
    ClassifieR.fit(TrainNTransform, Training_data['polarity'])

    # test set 
    #classification for the outputs
    TestNTransform = Vcounter.transform(Test_Set['text'])
    fin_Res = ClassifieR.predict(TestNTransform)

    with open("bigram.output.txt", "w") as f:
        for FIN in fin_Res:
            f.write(str(FIN) + "\n")
    
    '''train a SGD classifier using unigram representation
    with tf-idf, predict sentiments on imdb_te.csv, and write 
    output to unigramtfidf.output.txt'''    
    Vcounter = TfVt(stop_words = Stop_Words)
    TrainNTransform = Vcounter.fit_transform(Training_data['text'])
    
    ClassifieR = SGDC(loss="hinge", penalty="l1")
    ClassifieR.fit(TrainNTransform, Training_data['polarity'])

    # test set 
    #classification for the outputs    
    TestNTransform = Vcounter.transform(Test_Set['text'])
    fin_Res = ClassifieR.predict(TestNTransform)
    
    with open("unigramtfidf.output.txt", "w") as f:
        for FIN in fin_Res:
            f.write(str(FIN) + "\n")

    '''train a SGD classifier using bigram representation
    with tf-idf, predict sentiments on imdb_te.csv, and write 
    output to bigramtfidf.output.txt'''    
    Vcounter = TfVt(stop_words = Stop_Words, ngram_range = (1, 2))
    TrainNTransform = Vcounter.fit_transform(Training_data['text'])
    
    ClassifieR = SGDC(loss = "hinge", penalty = "l1")
    ClassifieR.fit(TrainNTransform, Training_data['polarity'])

    # test set 
    #classification for the outputs    
    TestNTransform = Vcounter.transform(Test_Set['text'])
    fin_Res = ClassifieR.predict(TestNTransform)

    with open("bigramtfidf.output.txt", "w") as f:
        for FIN in fin_Res:
            f.write(str(FIN) + "\n")
    pass        

#end of project