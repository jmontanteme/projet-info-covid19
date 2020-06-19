from flask import Flask, render_template, flash, redirect, url_for
from form import SearchBar,Factor_selection
from flask_wtf.csrf import CSRFProtect
from search import fonction_search,get_article

app = Flask(__name__)

#pour empêcher les requêtes non souhaitées
csrf =CSRFProtect(app)
app.config['SECRET_KEY'] = "secretkey"
app.config['WTF_CSRF_SECRET_KEY'] = "secretkey"
csrf.init_app(app)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/recherche",methods=["GET", "POST"])
def search():
    form=SearchBar(csrf_enable=False)
    if form.validate_on_submit():
        keywords=form.keywords.data	
        top=fonction_search(keywords)
        return render_template("resultats_recherche.html",top=top,keywords=keywords)
    return render_template("barre_recherche.html", form=form)   

@app.route('/facteurs',methods=["GET", "POST"])
def search_facteur():
    form=Factor_selection()
    if form.validate_on_submit():
        factors=form.select.data
        return render_template("resultats_facteurs.html",factors=factors)
    return render_template("selection_facteurs.html",form=form)

@app.route("/affichage/<int:n_article>")
def aff_article(n_article):
    article,full,text=get_article(n_article)
    return render_template("affichage_article.html",article=article,full=full,text=text)


if __name__ == "__main__":
    app.run(debug=True)