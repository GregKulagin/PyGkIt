# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, redirect, flash, url_for
import config
import logging

logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'logs/test.log')
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'sjkfshfd89f7sghjksdf'
#app.config['WTF_CSRF_ENABLED'] = False
#app.config.from_object(config)
app.config['WTF_CSRF_SECRET_KEY'] = 'sdfjh(&*hkjsdhfjks'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    from forms import LoginForm
    import psycopg2
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember me {}'.format(form.username.data, form.remember_me.data))
        login = form.username.data
        password = form.password.data
        conn = psycopg2.connect(host='localhost', user='greg', password='greg', dbname='gregdb')
        cursor = conn.cursor()
       # logging.debug(sql)
        cursor.execute('INSERT INTO users (login, password) VALUES (%s,%s)', (login, password))
        conn.commit()
        conn.close()
        cursor.close()
        return redirect('/')
    return render_template('login.html', title='Sign In', form=form)


if __name__ == '__main__':
    app.run()
