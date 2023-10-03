from email.mime import base
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
import pandas as pd
import sys
import re
import requests
import django
from django.core.exceptions import ObjectDoesNotExist
from unicodedata import normalize
from datetime import date
from bs4 import BeautifulSoup
from datetime import datetime
import os
import tqdm
import multiprocessing

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'granalysis.settings'
django.setup()

from api.models import Review,Stay,Keyword

def get_stay_polarity(id):
    polarity_list = Review.objects.filter(stay_id=id).values_list('polarity',flat=True)
    n_reviews = polarity_list.count()
    stay_polarity= 0.0
    for review_polarity in polarity_list:
        stay_polarity += review_polarity
    stay_polarity = float(stay_polarity/n_reviews)
    return stay_polarity

def get_keyword(string):
    rake = Rake()
    keywords = rake.apply(string)
    if len(keywords) == 0:
        keyword = ""
    else:  
        keyword = keywords[0][0]
    return keyword

def get_sentiment_analysis(url):
    MODEL = f"clampert/multilingual-sentiment-covid19"
    #MODEL = f"cardiffnlp/twitter-xlm-roberta-base-sentiment"

    #ID del Alojamiento del que se realiza el análisis
    id = Stay.objects.get(url=url).stay_id
    #Lista de Reviews
    review_list = Review.objects.filter(stay_id=id)
    comment_list = review_list.values_list('comment',flat=True)

    
    for review in tqdm.tqdm(review_list):

        tokenizer = AutoTokenizer.from_pretrained(MODEL)
        config = AutoConfig.from_pretrained(MODEL)
        
        text = review.comment
        sentences = sent_tokenize(text)
        sentences = list(filter(None,sentences))

        model = AutoModelForSequenceClassification.from_pretrained(MODEL)
        # model.save_pretrained(MODEL)
        # tokenizer.save_pretrained(MODEL)
        
        polarity_list = []
        keyword_list = []
        review_polarity = 0
        frecuency = 0
        print(sentences)
            
        for sent in sentences:

            keyword = get_keyword(sent)
            

            
            
            #Modelo
            encoded_input = tokenizer(sent, return_tensors ='pt')
            output = model(**encoded_input)
            scores = output[0][0].detach().numpy()
            scores = softmax(scores)
            polarity_ = np.round(float(scores[1]),4)
            review_polarity += polarity_
            print(polarity_)
            polarity_list.append(polarity_)

            #if keyword_list.count(keyword) == 0:
            try:
                Keyword_object = Keyword.objects.filter(id_review__in=review_list).get(word=keyword) #y stay_id=id
                current_polarity = Keyword_object.polarity
                new_polarity = np.round(float((0.5*current_polarity + 0.5*polarity_)),4) ################### INTERPOLACION LINEAL?
                Keyword_object.polarity = new_polarity
                Keyword_object.save()
                
            except ObjectDoesNotExist:
            #else:
                
                for comment in comment_list:
                    frecuency += comment.count(keyword)
                
                newKeyword = Keyword(word=keyword,
                                polarity=polarity_, 
                                frecuency=frecuency, 
                                id_review=review)

                
                keyword_list.append(newKeyword)
                newKeyword.save()
                
        
        review_polarity = float(review_polarity/len(sentences))
        review.polarity = review_polarity
        review.save()
        

        print(review_polarity)

    stay_object = Stay.objects.get(stay_id=id)
    stay_polarity = get_stay_polarity(id)
    stay_object.polarity = stay_polarity
    stay_object.save()
    #return (review_polarity,keyword_list,polarity_list,frecuency)


def stay_is_reviewed(url):
    is_reviewed = False
    id_ = 0
    if Stay.objects.filter(url=url).exists():
        id_ = Stay.objects.get(url=url).stay_id
        if Review.objects.filter(stay_id=id_).exists():
            is_reviewed = True
    return (id_,is_reviewed)

def normalize_text(string):
    #funcion para normalizar el texto antes de incorporarlo al dataframe

    s = string.strip()
    s = s.strip('\n')
    
    s = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![ \u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
    normalize("NFC", s), 0, re.I)

    s = normalize('NFC', s)

    emoji_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        "]+", flags = re.UNICODE)    
    
    s = emoji_pattern.sub(r'',s)

    return s

def get_response(offset, rows, pagename):
    #funcion para scrapear la url del hotel en base a la máxima cantidad de reviews (25) por iteracion

    base_url = "https://www.booking.com/reviewlist.es.html?cc1=es&pagename="+pagename+"&r_lang=&review_topic_category_id=&type=total&score=&sort=f_recent_desc&room_id=&time_of_year=&dist=1&offset={0}&rows={1}"
    url = base_url.format(offset, rows)
    x = requests.get(url, headers={"User-Agent": "PostmanRuntime/7.28.2"})
    return x

def get_data(url):

    #NORMALIZAR URL eliminando ? y posterior

    month_es = {
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

    (id_,is_reviewed) = stay_is_reviewed(url)
    print(id)

    dict = {}

    #Si se ha escrapapeado:

    if is_reviewed:
        #recent_comment = Review.objects.filter(stay_id=id_).order_by("date_review").first()
        #latest_date = recent_comment.date_review

        r = requests.get(url, headers={"User-Agent": "PostmanRuntime/7.28.2"})
        bsoup = BeautifulSoup(r.text, 'html.parser')

        slide_info = bsoup.find_all("a", attrs={"data-target":"hp-reviews-sliding"})
        print(len(slide_info))

        
        n_comments = slide_info[len(slide_info)-1].text
        n_comments = n_comments[n_comments.find('(') + 1 : n_comments.find(')')]
        print(n_comments)
        
        
        if(n_comments.isdigit() == False):
            number_parts = n_comments.split(".")
            n_comments = number_parts[0] + number_parts[1]

        n_comments = int(n_comments)

        url_sets = url.split('/')
        url_var = url_sets[5].split('.')

        pagename = url_var[0]

        current_comments = Review.objects.filter(stay_id=id_).count()
        print(current_comments)

        new_comments = n_comments-current_comments
        print(new_comments)
        
        
        if new_comments > 0:
            
            i = 1
            for offset in range(0, new_comments, 10):
                response = get_response(offset, 10, pagename)
                bs = BeautifulSoup(response.text, 'html.parser')

                reviews_body = bs.find_all("li", class_="review_list_new_item_block")
                for reviewBody in reviews_body:

                    id_review_ = reviewBody.get('data-review-url')
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
                        date_ = date_.replace(month, str(month_es[month]))
                        date_object = datetime.strptime(date_,"%d de %m de %Y")
                        new_format = "%d/%m/%Y"
                        date_new_format = date_object.strftime(new_format)
                        date_new_format = pd.to_datetime(date_new_format, dayfirst = True)
                    else:
                        date_new_format = ""
                
                    stay_data = normalize_text(data[0].text)
                    number_nights = stay_data.split("·")[0].strip()
                    stay_date = stay_data.split("·")[1].strip()
                    print(stay_date)

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
                
                    # dict[i] = {
                    #     "id": id_review,
                    #     "cliente": normalize_text(user_name[0].text),
                    #     "nacionalidad": "" if len(nacionality) < 1 else normalize_text(nacionality[0].text),
                    #     "comentario_completo" : comment,                                                 
                    #     "tipo de habitacion": "" if len(type_room) < 1 else normalize_text(type_room[0].text),
                    #     "noches": "" if len(data) < 1 else number_nights,
                    #     "fecha_alojamiento" : "" if len(data) < 1 else stay_date,
                    #     "tipo_cliente": "" if len(type_costumer) < 1 else normalize_text(type_costumer[0].text),
                    #     "fecha de comentario" : date_new_format
                    # }
                    i += 1

                    review = Review(id_review=id_review_,costumer_name = normalize_text(user_name[0].text), 
                                    nationality =  "" if len(nacionality) < 1 else normalize_text(nacionality[0].text),
                                    comment = comment, 
                                    room_type = "" if len(type_room) < 1 else normalize_text(type_room[0].text),
                                    number_nights = "" if len(data) < 1 else number_nights,
                                    date_review = date_new_format, 
                                    date_entry = "" if len(data) < 1 else stay_date,
                                    client_type = "" if len(type_costumer) < 1 else normalize_text(type_costumer[0].text), 
                                    stay_id = Stay.objects.get(stay_id=id_))
                    review.save()
                    
    #Si NO se ha escrapapeado:
    else:

        r = requests.get(url, headers={"User-Agent": "PostmanRuntime/7.28.2"})
        bsoup = BeautifulSoup(r.text, 'html.parser')

        name = bsoup.find("h2",class_ = "d2fee87262 pp-header__title")
        print(name)
        name = name.text
        name = name.strip()
        #print(name)

        ubicacion = bsoup.find("span",class_="hp_address_subtitle")
        ubicacion = ubicacion.text
        ubicacion = ubicacion.strip()
        #print(ubicacion)

        # stay = Stay(name=name,url=url,location=ubicacion)
        # stay.save()

        slide_info = bsoup.find_all("a", attrs={"data-target":"hp-reviews-sliding"})
        print(len(slide_info))
        n_comments = slide_info[len(slide_info)-1].text
        n_comments = n_comments[n_comments.find('(') + 1 : n_comments.find(')')]
        

        if(n_comments.isdigit() == False):
            number_parts = n_comments.split(".")
            n_comments = number_parts[0] + number_parts[1]

        n_comments = int(n_comments)
        print(n_comments)
        url_sets = url.split('/')
        url_var = url_sets[5].split('.')

        pagename = url_var[0]

        i = 1
        for offset in range(0, n_comments, 25):
            response = get_response(offset, 25, pagename)
            bs = BeautifulSoup(response.text, 'html.parser')

            reviews_body = bs.find_all("li", class_="review_list_new_item_block")
            for reviewBody in reviews_body:

                id_review_ = reviewBody.get('data-review-url')
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
                    date_ = date_.replace(month, str(month_es[month]))
                    date_object = datetime.strptime(date_,"%d de %m de %Y")
                    date_new_format = date_object.date()
                    #new_format = "%d/%m/%Y"
                    #date_new_format = date_new_format.strftime(new_format)
                    #date_new_format = pd.to_datetime(date_new_format, dayfirst = True)
                    
                else:
                    date_new_format = ""
            
                stay_data = normalize_text(data[0].text)
                number_nights = stay_data.split("·")[0].strip()
                stay_date = stay_data.split("·")[1].strip()
                print(stay_date)

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

                print("\nComentario numero "+ str(i) +": " + comment + "\n")
                #print("Nacionalidad del usuario de la review: " + nacionality[0].text + "\n")
            
                dict[i] = {
                    "id": id_review_,
                    "cliente": normalize_text(user_name[0].text),
                    "nacionalidad": "" if len(nacionality) < 1 else normalize_text(nacionality[0].text),
                    "comentario_completo" : comment,                                                 
                    "tipo de habitacion": "" if len(type_room) < 1 else normalize_text(type_room[0].text),
                    "noches": "" if len(data) < 1 else number_nights,
                    "fecha_alojamiento" : "" if len(data) < 1 else stay_date,
                    "tipo_cliente": "" if len(type_costumer) < 1 else normalize_text(type_costumer[0].text),
                    "fecha de comentario" : date_new_format
                }
                i += 1

                review = Review(id_review = id_review_, 
                                costumer_name = normalize_text(user_name[0].text), 
                                nationality =  "" if len(nacionality) < 1 else normalize_text(nacionality[0].text),
                                comment = comment, 
                                room_type = "" if len(type_room) < 1 else normalize_text(type_room[0].text),
                                number_nights = "" if len(data) < 1 else number_nights,
                                date_review = date_new_format, 
                                date_entry = "" if len(data) < 1 else stay_date,
                                client_type = "" if len(type_costumer) < 1 else normalize_text(type_costumer[0].text), 
                                stay_id = Stay.objects.get(stay_id=id_))
                review.save()  
        
    df = pd.DataFrame.from_dict(dict, orient="index")
    #df.sort_values(by='fecha de comentario', ascending = False, inplace = True)  
    # today_date = date.today()
    # today_date = datetime.strftime("%d/%m%Y")
    df.to_csv(f"stay_reviews/{pagename}"+".csv", sep = ";", index=False) 

#arguments = sys.argv
#url = arguments[1]
#get_data(url)

url ="https://www.booking.com/hotel/es/plazas-de-ca-diz-apartamentos.es.html"
#get_data(url)
get_sentiment_analysis(url)