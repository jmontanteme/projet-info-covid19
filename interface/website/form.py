from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField,SelectMultipleField
from wtforms.validators import DataRequired
from wtforms.widgets import CheckboxInput,ListWidget

RiskFactors=[("smoking_status","Smoking Status"),("hypertension","Hypertension"),("diabetes","Diabetes"),("gender","Gender"),("heart_disease","Heart_Diseases"),("COPD_respiratory_system ","COPD respiratory system"),("age","Age"),("cerebrovascular_disease","Cerbrovascular_disease"),("cancer","Cancer"),("kidney_disease","Kidney disease"),("drinking","Drinking"),("overweight","Overweight"),("liver_disease",'Liver Disease')]
class SearchBar(FlaskForm):
    keywords =TextAreaField('Mots-clés', validators=[DataRequired()])
    submit = SubmitField('Rechercher')

class Factor_selection(FlaskForm):
    select=SelectMultipleField("facteurs",choices=RiskFactors ,option_widget=CheckboxInput(),widget=ListWidget(prefix_label=False))
    submit = SubmitField('Rechercher')
    

