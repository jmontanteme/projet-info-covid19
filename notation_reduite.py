
hypertension = ['hypertension', 'high blood pressure', 'hypertensive', 'high pressure', 'raised blood pressure', 'htn', 'hbp', 'ht', 'ace inhibitor', 'sartan']
diabetes = ['diabetes', 'high blood sugar', 'insulin resistance', 'diabetic', 'diabetics', 'dm']
gender = ['male gender', 'male', 'gender', 'sex', 'masculine', 'female']
heart_disease = ['cardiopathy', 'heart disease', 'heart', 'chd', 'arrhythmia', 'tachycardia', 'bradycardia', 'fibrillation', 'cardiomyopathy', 'infarction', 'ischemic heart disease']
COPD_respiratory_system = ['copd', 'emphysema', 'bronchitis', 'asthma', 'bronchiectasis', 'respiratory', 'trachea', 'lung', 'lungs', 'pulmonary', 'pneumoniae', 'pharyngitis', 'bronchiolitis', 'bronchopneumonia' ]
smoking_status = ['smoking', 'smoke', 'smoker', 'tobacco']
age = ['age', 'old', 'young', 'senior', 'child', 'children']
cerebrovascular_disease = ['cerebrovascular', 'embolism', 'ischemic', 'stroke', 'aneurysm', 'tia']
cancer = ['cancer', 'leukemia', 'cancerology', 'lymphom']
kidney_disease = ['kidney', 'gfr', 'dialysis']
drinking = ['drinking', 'alcohol', 'alcoholic']
overweight = ['overweight', 'obesity', 'obese', 'bmi']
liver_disease = ['liver', 'fascioliasis', 'cirrhosis', 'hepatitis']

import numpy as np
import pandas as pd
import json
import glob
import spacy
from spacy.matcher import PhraseMatcher
nlp = spacy.blank('en')
nlp.max_length = 5000000000000000

hta_tokens_list = [nlp(factor) for factor in hypertension]
diabetes_tokens_list = [nlp(factor) for factor in diabetes]
gender_tokens_list = [nlp(factor) for factor in gender]
heart_tokens_list = [nlp(factor) for factor in heart_disease]
respi_tokens_list = [nlp(factor) for factor in COPD_respiratory_system]
smoking_tokens_list = [nlp(factor) for factor in smoking_status]
age_tokens_list = [nlp(factor) for factor in age]
cerebrovascular_tokens_list = [nlp(factor) for factor in cerebrovascular_disease]
cancer_tokens_list = [nlp(factor) for factor in cancer]
kidney_tokens_list = [nlp(factor) for factor in kidney_disease]
drinking_tokens_list = [nlp(factor) for factor in drinking]
overweight_tokens_list = [nlp(factor) for factor in overweight]
liver_tokens_list = [nlp(factor) for factor in liver_disease]

root_path = '/Users/juliettemontanteme/Desktop/data_covid'
metadata_path = '/Users/juliettemontanteme/Desktop/metadata_processed_byme.csv'
meta_df = pd.read_csv(metadata_path)
print(meta_df.columns)
#Classe permettant de faire un preprocessing d'un texte

class Preprocess:
    def __init__(self, path):
        self.path = path
        self.article = ""
        self.text = ""
        self.text1 = ""
        self.text2 = ""
        self.title = ""
        self.abstract = ""
    def open_article(self):
        file=open(str(root_path)+"/"+str(path),'r')
        article=json.load(file)
        file.close()
        self.article = article
    def make_text(self):
        text_list = []
        for entry in self.article['body_text']:
            text_list.append(entry['text'])
            text_list.append("\n")
        text_full=''.join(text_list)
        self.text = text_full
        self.title = nlp(meta_df.loc[lambda df: df['path'] == self.path] ['title_process'].to_string(index = False))
        self.abstract = nlp(meta_df.loc[lambda df: df['path'] == self.path] ['abstract_process'].to_string(index = False))
    
    def preprocess(self): 
        self.text1 = nlp(self.text)
        text2 = ""
        for token in self.text1: 
            if token.is_stop == False:
                text2 = text2 + " " + token.lemma_
        self.text2 = nlp(text2)

    def repr_1(self):
        return(self.text1)
    
    def repr_2(self):
        return(self.text2)


import math


class Diffusivity:
    def __init__(self, matches, doc):
        self.matches = matches
        self.doc = doc
        self.positions = []
        self.occurence = len(self.matches)
        self.score = 0
    def position(self):
        if self.matches != []:
            for match in self.matches :
                pos = (match[1] + match[2])/2
                self.positions.append(int(pos))   
    def scoring(self):
        if self.positions != []:
            mean_pos = np.mean(self.positions)
            ecart_pos = math.sqrt(np.var(self.positions))
            self.score = ecart_pos / len(self.doc)

class Frequency: 
    def __init__(self, matches, doc):
        self.matches = matches
        self.doc = doc
        self.occurence = len(self.matches)
        self.score = 0

    def scoring(self):
        if len(self.matches) != 0:
            self.score = len(self.matches)/len(self.doc)

        
class Scoring:
    def __init__(self, text, title, abstract, lex, lex_name):
        self.text = text
        self.title = title
        self.abstract = abstract
        self.lex = lex
        self.lex_name = lex_name
        self.match_doc = []
        self.match_title = []
        self.match_abstract = []
        self.score_dif = 0
        self.score_fr_doc = 0
        self.score_fr_title = 0
        self.score_fr_abstract = 0
        self.score_dif = 0
    def matching(self):
        matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
        matcher.add(self.lex_name, self.lex)
        self.match_doc = matcher(self.text)
        self.match_title = matcher(self.title)
        self.match_abstract = matcher(self.abstract)
        
    def scoring(self):
        #Calcul du score de diffusivité
        dif = Diffusivity(self.match_doc, self.text)
        dif.position()
        dif.scoring()
        self.score_dif = dif.score
        #Calcul du score de fréquence dans le texte
        fr_doc = Frequency(self.match_doc, self.text)
        fr_doc.scoring()
        self.score_fr_doc = fr_doc.score
        #Calcul du score de fréquence dans le titre
        fr_title = Frequency(self.match_title, self.title)
        fr_title.scoring()
        self.score_fr_title = fr_title.score
        #Calcul du score de fréquence dans l'abstract
        fr_abstract = Frequency(self.match_abstract, self.abstract)
        fr_abstract.scoring()
        self.score_fr_abstract = fr_abstract.score
        

tokens_list = [hta_tokens_list, diabetes_tokens_list, gender_tokens_list, heart_tokens_list,respi_tokens_list, smoking_tokens_list, age_tokens_list, cerebrovascular_tokens_list, cancer_tokens_list, kidney_tokens_list, drinking_tokens_list, overweight_tokens_list, liver_tokens_list] 
tokens_names = ["HTA", "DIABETES", "GENDER", "HEART", "RESPI", "SMOKING", "AGE", "CEREBROVASCULAR", "CANCER", "KIDNEY", "DRINKING", "OVERWEIGHT", "LIVER"]
columns = ['hypertension', 'diabetes', 'gender', 'heart_disease', 'COPD_respiratory_system ', 'smoking_status', 'age', 'cerebrovascular_disease', 'cancer', 'kidney_disease', 'drinking', 'overweight', 'liver_disease']
meta_work = meta_df.sort_values(by = ['date'], ascending = False)

for i in range(13):
    meta_work[f'note_{columns[i]}'] = 0


for j in range(len(meta_work)):
    if j%1000 == 0:
        print(j)
    path = meta_work['path'].iloc[j] 
    try: 
        proc = Preprocess(path)
        proc.open_article()
        proc.make_text()
        proc.preprocess()
        text = proc.repr_1()
        title = proc.title
        abstract = proc.abstract
        for i in range(13):
            lex = tokens_list[i]
            lex_name = tokens_names[i]
            sc = Scoring(text, title, abstract, lex, lex_name)
            sc.matching()
            sc.scoring()
            a = sc.score_dif
            b = sc.score_fr_title
            c = sc.score_fr_abstract
            d = sc.score_fr_doc
            meta_work[f'note_{columns[i]}'].iloc[j] = a + b + c + d    
    except(FileNotFoundError):
        pass
            



meta_df_save = meta_work
meta_df_save.to_csv("metadata_processed_byme.csv")