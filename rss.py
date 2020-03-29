from flask import Flask, render_template, request, flash, url_for, redirect, g
import feedparser
from flask_mail import Mail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://rsssender:jRwmwyuWBl5VtKcmGKjZnyhukL6HaUxt0X7oSteWYSR1JD7VVe5atFkoQ0TfM7ypGJzxk8w71FlEgn7W7ebb2g==@rsssender.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@rsssender@")
db1 = client.test
db1.authenticate(name="rsssender" ,password='jRwmwyuWBl5VtKcmGKjZnyhukL6HaUxt0X7oSteWYSR1JD7VVe5atFkoQ0TfM7ypGJzxk8w71FlEgn7W7ebb2g==')


app.config.update(dict(
    SECRET_KEY='bardzosekretnawartosc',
))


@app.route('/send', methods=['POST'])
def send():

    RssListColection = db1.rsslist.find({}, {'_id': 0, 'email': 0})
    EmailListCollection = db1.rsslist.find({}, {'_id': 0, 'rss': 0})
    email = EmailListCollection[0]
    listarssow = []
    entrieslist = []
    for x in RssListColection:
        listarssow.append(x['rss'])

    for x in listarssow:
        feed = feedparser.parse(x)
        entries = feed.entries
        for z in entries:
            entrieslist.append(z)

    html1 = render_template('mailtemplate.html', entrieslist=entrieslist)
    message = Mail(
        from_email='patryk.razniak@example.com',
        to_emails=email['email'],
        subject='RssSenderMail',
        html_content=html1)
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
    return redirect(url_for('sendRss'))


@app.route('/delete', methods=['POST'])
def delete():
    """Usuniecie rss-u"""
    zadanie_id = request.form['id']
    db1.rsslist.delete_one({'rss': zadanie_id})
    flash('Zmieniono status zadania.')
    return redirect(url_for('sendRss'))


@app.route('/sendRss', methods=['GET', 'POST'])
def sendRss():
    error = None
    if request.method == 'POST':
        _rss = request.form['inputRss'].strip()
        _email = request.form['inputEmail'].strip()
        rsslist = db1.rsslist
        rsslist.insert({'rss': _rss, 'email': _email})
        flash('Dodano nowy rss.')
        return redirect(url_for('sendRss'))

        error = 'Nie możesz dodać pustego rss-a!'  # komunikat o błędzie

    RssListColection = db1.rsslist.find({}, {'_id': 0, 'email': 0})
    listarssow = []
    entrieslist = []

    for x in RssListColection:
        listarssow.append(x['rss'])

    for x in listarssow:
        feed = feedparser.parse(x)
        entries = feed.entries
        for z in entries:
            entrieslist.append(z)

    return render_template("index.html", error=error, listarssow=listarssow, entrieslist=entrieslist)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
