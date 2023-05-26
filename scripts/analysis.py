import pandas as pd
import time
import nltk
from nltk.tokenize import sent_tokenize
from googletrans import Translator
from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer,AutoConfig
import numpy as np
from scipy.special import softmax
from multi_rake import Rake

def get_keyword(string):
    rake = Rake()
    keywords = rake.apply(string)
    if len(keywords) > 0:
        keyword = keywords[0]
    else:  
        keyword = ""
    return keyword

def get_sentiment_analysis(dataframe):
    MODEL = f"clampert/multilingual-sentiment-covid19"
    #MODEL = f"cardiffnlp/twitter-xlm-roberta-base-sentiment"
    dict = {}
    dict1 = {}

    dataframe['comentario_completo'].str.count()##### FRECUENCIA ENCONTRAR
    
    for row in dataframe.index:

        tokenizer = AutoTokenizer.from_pretrained(MODEL)
        config = AutoConfig.from_pretrained(MODEL)
        
        text = dataframe.iat[row,5]
        sentences = sent_tokenize(text)
        sentences = list(filter(None,sentences))

        model = AutoModelForSequenceClassification.from_pretrained(MODEL)
        # model.save_pretrained(MODEL)
        # tokenizer.save_pretrained(MODEL)
        
        polarity_list = []
        keyword_list = []
        review_polarity = 0
        print(sentences)
            
        for sent in sentences:
            keyword = get_keyword(sent) 
            frecuency = dataframe['comentario_completo'].str.count(keyword)         
            keyword_list.append(keyword)

            encoded_input = tokenizer(sent, return_tensors ='pt')
            output = model(**encoded_input)
            scores = output[0][0].detach().numpy()
            scores = softmax(scores)
            polarity = np.round(float(scores[1]),4)
            review_polarity += polarity
            print(polarity)
            polarity_list.append(polarity)
        
        review_polarity = float(review_polarity/len(sentences))
        print(review_polarity)
        
        
    return (review_polarity,keyword_list,polarity_list,frecuency)

    

df = pd.read_csv("dataBooking.csv", sep = ";", index_col=False)

(review_polarity,keyword_list,keyword_polarity_list,frecuency_list) = get_sentiment_analysis(df)




# tokenizer = AutoTokenizer.from_pretrained(MODEL)
# config = AutoConfig.from_pretrained(MODEL)

# model = AutoModelForSequenceClassification.from_pretrained(MODEL)
# model.save_pretrained(MODEL)
# tokenizer.save_pretrained(MODEL)

# rake = Rake()
# print("Muy malo el hotel, no nos ha gustado absolutamente nada")
# #text = df.iat[78,5]
# text = "Muy malo el hotel, no nos ha gustado absolutamente nada"
# keywords = rake.apply(text)
# print(keywords[0])
# encoded_input = tokenizer(text, return_tensors ='pt')
# output = model(**encoded_input)
# scores = output[0][0].detach().numpy()
# print(scores)
# scores = softmax(scores)
# print(np.round(float(scores[1]),4))
# ranking = np.argsort(scores)
# print(ranking)
# ranking = ranking[::-1]
# print(ranking)
# for i in range(scores.shape[0]):
#     l = config.id2label[ranking[i]]
#     s = scores[ranking[i]]
#     print(np.round(float(s),4))
#     print(f"{i+1} {l} {np.round(float(s),4)}")
    
    









