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
from email.mime import base
import sys
import re
import requests
import os.path
from unicodedata import normalize
from datetime import date
from bs4 import BeautifulSoup
from datetime import datetime
from api.models import Review,Keyword,Stay


MONTH_ES = {
    "enero" : 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12     
}

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


def normalize_text(string):
    #funcion para normalizar el texto antes de incorporarlo al dataframe

    s = string.strip()
    s = s.strip('\n')
    
    s = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![ \u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
    normalize("NFC", s), 0, re.I)
    
    s = normalize('NFC', s)

    return s

def get_response(offset, rows, pagename):
    #funcion para scrapear la url del hotel en base a la máxima cantidad de reviews (25) por iteracion

    base_url = "https://www.booking.com/reviewlist.es.html?cc1=es&pagename="+pagename+"&r_lang=&review_topic_category_id=&type=total&score=&sort=&room_id=&time_of_year=&dist=1&offset={0}&rows={1}"
    url = base_url.format(offset, rows)
    x = requests.get(url, headers={"User-Agent": "PostmanRuntime/7.28.2"})
    return x

def get_data(url):

    r = requests.get(url, headers={"User-Agent": "PostmanRuntime/7.28.2"})
    bsoup = BeautifulSoup(r.text, 'html.parser')

    ubicacion = bsoup.find("span",class_="hp_address_subtitle")
    ubicacion = ubicacion.text
    ubicacion = ubicacion.strip()
    #print(ubicacion)

    slide_info = bsoup.find_all("li", class_ = "a0661136c9")

    n_comments = slide_info[len(slide_info)-1].text
    n_comments = n_comments[n_comments.find('(') + 1 : n_comments.find(')')]

    if(n_comments.isdigit() == False):
        number_parts = n_comments.split(".")
        n_comments = number_parts[0] + number_parts[1]

    n_comments = int(n_comments)
    url_sets = url.split('/')
    url_var = url_sets[5].split('.')

    pagename = url_var[0]

    eAnlaysis = False
    if os.path.isfile(f"./{pagename}"+".csv"):
        eAnlaysis = True
        df_ = pd.read_csv(f"./{pagename}"+".csv", sep = ";", index_col=False)

    dict = {}

    i = 1
    for offset in range(0, n_comments, 25):
        response = get_response(offset, 25, pagename)
        bs = BeautifulSoup(response.text, 'html.parser')

        reviews_body = bs.find_all("li", class_="review_list_new_item_block")
        for reviewBody in reviews_body:

            id_review = reviewBody.get('data-review-url')
            user_name = reviewBody.find_all("span", class_ = "bui-avatar-block__title")
            nacionality = reviewBody.find_all("span", class_= "bui-avatar-block__subtitle")
            comments_title = reviewBody.find_all("h3", class_= "c-review-block__title c-review__title--ltr")
            comments = reviewBody.find_all("span", class_= "c-review__body")
            type_room = reviewBody.find_all("ul", class_= "bui-list bui-list--text bui-list--icon bui_font_caption")
        
            data = reviewBody.find_all("ul", class_= "bui-list bui-list--text bui-list--icon bui_font_caption c-review-block__row c-review-block__stay-date")
            comment_date = reviewBody.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['c-review-block__row'])
            comment_date = comment_date[0].find("span", class_="c-review-block__date")

            if len(comment_date) >= 1:
                date_ = comment_date.text.split(":")[1]
                date_ = date_.strip()
                month = date_.split("de")[1].strip()
                date_ = date_.replace(month, str(MONTH_ES[month]))
                date_object = datetime.strptime(date_,"%d de %m de %Y")
                new_format = "%d/%m/%Y"
                date_new_format = date_object.strftime(new_format)
                date_new_format = pd.to_datetime(date_new_format, dayfirst = True)
            else:
                date_new_format = ""
        
            stay_data = normalize_text(data[0].text)
            number_nights = stay_data.split("·")[0].strip()
            stay_date = stay_data.split("·")[1].strip()

            type_costumer = reviewBody.find_all("ul", class_= "bui-list bui-list--text bui-list--icon bui_font_caption review-panel-wide__traveller_type c-review-block__row")
            #print(normalize_text(nacionality[0].text))
            comment1 = ""
            comment2 = ""
            comment3 = ""
            if len(comments_title)>= 1:
                comment1 = normalize_text(comments_title[0].text)
                if not comment1.endswith("."):
                    if comment1 != "":
                        comment1 = comment1 + "."
                if comment1 == "Esta entrada no tiene comentarios.":
                    comment1 = ""
            if len(comments) >= 1:
                comment2 = normalize_text(comments[0].text)
                if not comment2.endswith("."):
                    if comment2 != "":
                        comment2 = comment2 + "."
                if comment2 == "Esta entrada no tiene comentarios.":
                    comment2 = ""
            if len(comments) >= 2:
                comment3 = normalize_text(comments[1].text)
                if not comment3.endswith("."):
                    if comment3 != "":
                        comment3 = comment3 + "."
                if comment3 == "Esta entrada no tiene comentarios.":
                    comment3 = ""
                
            comment = comment1 + comment2 + comment3
            comment = comment.strip()

            print(comment)
        
            dict[i] = {
                "cliente": normalize_text(user_name[0].text),
                "nacionalidad": "" if len(nacionality) < 1 else normalize_text(nacionality[0].text),
                "comentario_completo" : comment,                                                 
                "tipo de habitacion": "" if len(type_room) < 1 else normalize_text(type_room[0].text),
                "noches": "" if len(data) < 1 else number_nights,
                "fecha_alojamiento" : "" if len(data) < 1 else stay_date,
                "tipo_cliente": "" if len(type_costumer) < 1 else normalize_text(type_costumer[0].text),
                "fecha de comentario" : date_new_format,
                "id": id_review
            }
            i += 1
    df = pd.DataFrame.from_dict(dict, orient="index")
    df.sort_values(by='fecha de comentario', ascending = False, inplace = True)
    #from pandas.io import sql
    #import MySQLdb
    #con = MySQLdb.connect()
    
    #df.to_sql
        
    return (ubicacion, df)