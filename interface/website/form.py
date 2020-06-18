from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField,SelectMultipleField
from wtforms.validators import DataRequired
from wtforms.widgets import CheckboxInput,ListWidget

RiskFactors=[("Obesity","Obesity"),("Smoking","Smoking")]
class SearchBar(FlaskForm):
    keywords =TextAreaField('Mots-clés', validators=[DataRequired()])
    submit = SubmitField('Rechercher')

class Factor_selection(FlaskForm):
    select=SelectMultipleField("facteurs",choices=RiskFactors ,option_widget=CheckboxInput(),widget=ListWidget(prefix_label=False))
    submit = SubmitField('Rechercher')
    

