import numpy as np
import pandas as pd
import json

from fonctions import *

meta_df=pd.read_csv("metadata_full.csv")

def fonction_search(keywords):
    give_note(meta_df,keywords)
    top=meta_df.sort_values(by=["note"],ascending=False)[0:5].values.tolist()   
    list_full=[True for i in range(5)] 
    for i in range(5):
        if str(top[i][7])=="nan":
            list_full[i]=False
    return top,list_full

def search_factors(factors):#factors est une liste
    give_note_factor(meta_df,factors)
    top=meta_df.sort_values(by=["note_totale"],ascending=False)[0:5].values.tolist()   
    list_full=[True for i in range(5)] 
    for i in range(5):
        if str(top[i][7])=="nan":
            list_full[i]=False
    return top,list_full

def get_article(n_article):
    article=meta_df.loc[n_article]
    path=article[7]
    print(f"path={path}")
    if str(path)=="nan":
            full=False
            text=""
            l_article=[]
            biblio=dict()
    else:
        full=True
        article_full=open_article(path)
        biblio=article_full["bib_entries"]
        l_article=make_article(path)         

    return article,full,l_article,biblio


def get_suggestion(n_article):
    article=meta_df.loc[n_article]
    suggestions=article[[f"suggestion_{i}" for i in range(5)]].tolist()
    Sug=[]
    list_full=[]
    for s_indice in suggestions:
        article,full,_,_=get_article(s_indice)
        Sug.append(article)
        list_full.append(full)
    return Sug,list_full

#les articles sont décrits sous la forme :
# 0 numéro article (inutile)
# 1 title
# 2 abstract
# 3 authors
# 4 title_process 	
# 5 abstract_process 	
# 6 date 	
# 7 path 	 	
# 8 nb_ref_linked 	
# 9 note_ref 	
# 10 freq_title 	
# 11 freq_abstract 	
# 12 - 16 suggestion_i
# note_factors 17 - 29
"""
article,full,l_article,biblio=get_article(59825)

print(l_article)


print(meta_df.columns)
"""
