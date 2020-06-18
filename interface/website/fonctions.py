import re
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
import json

lemmatizer=WordNetLemmatizer()
stop=stopwords.words('english')
root_path=root_path = '/home/arnaud/Documents/Mines1a/Informatique/Projet_informatique/data/CORD-19-research-challenge'


def preprocessing(x): #tokenisation,stop-words,lemmatization ...
    clean = re.sub(r'['+string.punctuation + '’—”'+']', "", x.lower())
    clean_text= re.sub(r'\W+', ' ', clean)
    a=""
    for i in clean_text.split():
        if i not in stop :
            a+=str(lemmatizer.lemmatize(i))+' '
    return a

def preprocessing_title(x): #tokenisation,stop-words,lemmatization ...
    clean = re.sub(r'['+string.punctuation + '’—”'+']', "", x.lower())
    clean_text= re.sub(r'\W+', ' ', clean)
    a=""
    for i in clean_text.split():
        a+=str(lemmatizer.lemmatize(i))+' '
    return a


def counter(keywords,text): #keywords est une phrase
    keys=preprocessing(keywords).split()
    text=str(text)
    if text=="NaN": #élimine 
        return -1
    a=text.split()
    if len(a)==0:
        return 0
    c=0
    for i in a:
        if i in keys:
            c+=1
    
    return c/len(a)

def counter_title(keywords,text): #keywords est une phrase
    keys=preprocessing_title(keywords).split()
    text=str(text)
    if text=="NaN":
        return -1
    a=text.split()
    if len(a)==0:
        return 0
    c=0
    for i in keys:
        if i in a:
            c+=1
    
    return c/len(keys)

def give_note(data,keywords):#data est un df
    data["freq_title"]=data["title_process"].apply(lambda x:counter_title(keywords,x))
    data["freq_abstract"]=data["abstract_process"].apply(lambda x:counter(keywords,x))
    data["note"]=data[["freq_title","freq_abstract","note_date","note_ref"]].apply(lambda x: x["freq_title"]+x["freq_abstract"]+x["note_ref"]+x["note_date"],axis=1)

def open_article(path):
    file=open(root_path+"/"+path,'r')
    article_json=json.load(file)
    file.close()
    return article_json

def make_text(article_json):
    text_list = []
    for entry in article_json['body_text']:
        text_list.append(entry['text'])
        text_list.append("\n \n")
    
    text_full=''.join(text_list)
    return text_full