import numpy as np
import pandas as pd
import json

from fonctions import *

meta_df=pd.read_csv("metadata_processed.csv")

def fonction_search(keywords):
    give_note(meta_df,keywords)
    top=meta_df.sort_values(by=["note"],ascending=False)[0:5].values.tolist()    
    return top

def get_article(n_article):
    article=meta_df.loc[n_article]
    path=article[7]
    try:
        if np.isnan(path):
            full=False
            text=""
    except TypeError:
        full=True
        article_json=open_article(path)
        text=make_text(article_json)
    return article,full,text


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