import numpy as np
import pandas as pd
import json

from fonctions import *

meta_df=pd.read_csv("metadata_processed.csv")
meta_df2=pd.read_csv("metadata_processed_reduced.csv")



def fonction_search(keywords):
    give_note(meta_df,keywords)
    top=meta_df.sort_values(by=["note"],ascending=False)[0:5].values.tolist()   
    list_full=[True for i in range(5)] 
    for i in range(5):
        if str(top[i][7])=="nan":
            list_full[i]=False
    return top,list_full

def search_factors(factors):#factors est une liste
    give_note_factor(meta_df2,factors)
    top=meta_df2.sort_values(by=["note_totale"],ascending=False)[0:5].values.tolist()   
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
    cluster=article["cluster"]
    meta_df_cluster=meta_df.loc[meta_df["cluster"]==cluster]
    suggestions=meta_df_cluster.sort_values(by=["note_ref"],ascending=False)[0:10].values.tolist()
    list_full=[True for i in range(5)] 
    for i in range(5):
        if str(suggestions[i][7])=="nan":
            list_full[i]=False
    return suggestions,list_full

#les articles sont décrits sous la forme :
# 0 numéro article (inutile)
# 1 title
# 2 abstract
# 3 authors
# 4 title_process 	
# 5 abstract_process 	
# 6 date 	
# 7 path 	
# 8 note_date 	
# 9 nb_ref_linked 	
# 10 note_ref 	
# 11 freq_title 	
# 12 freq_abstract 	
# 13 note
"""
article,full,l_article,biblio=get_article(59825)

print(l_article)

"""