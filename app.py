import datetime
import os

from flask import Flask, render_template, redirect, url_for
from forms import ItemForm
from models import Items
from database import db_session
from flask import Response


app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route("/", methods=('GET', 'POST'))
def add_item():
    form = ItemForm()
    if form.validate_on_submit():
        item = Items(name=form.name.data, quantity=form.quantity.data, description=form.description.data, date_added=datetime.datetime.now())
        #item = Items(name="hhwu", quantity=1, description="test", date_added=datetime.datetime.now())
        db_session.add(item)
        db_session.commit()
        return redirect(url_for('success', _external=True))
    return render_template('index.html', form=form)

@app.route("/success")
def success():
    results = []
 
    qry = db_session.query(Items)
    results = qry.all()

    res = "%-10s%-10s%-20s%s\n" %("name", "quantity", "description", "date")
    for elem in results:
        res += "%-10s%-10d%-20s%s\n" % (elem.name, elem.quantity, elem.description, str(elem.date_added))

    return Response(res, content_type="text/plain")
  

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
