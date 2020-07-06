

import re
import string
import nltk
from nltk.corpus import stopwords

# à faire si besoin
#nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer

lemmatizer=WordNetLemmatizer()
stop=stopwords.words('english')


#prend en entrée un str et retourne un str
def preprocessing(x): #tokenisation,stop-words,lemmatization ...
    clean = re.sub(r'['+string.punctuation + '’—”'+']', "", x.lower())
    clean_text= re.sub(r'\W+', ' ', clean)
    a=""
    for i in clean_text.split():
        if i not in stop :
            a+=str(lemmatizer.lemmatize(i))+' '
    return a
