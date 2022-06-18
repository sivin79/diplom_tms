#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql.cursors
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import socket


import config


def get_connection():

    connection = pymysql.connect(host=config.DB_HOST,
                                 user='root',
                                 password=config.DB_PASSWORD,
                                 db='posts',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    #print("Успешное подключение к базе данных!\n")
    connection.commit()
    return connection


def get_post(post_id):
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM posts WHERE id = {}".format(post_id))
            result = cursor.fetchone()
            if result is None:
                abort(404)
            return result


app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdfghjkl223056wertyuiop'


@app.route('/')
def index():
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM posts")
            posts = cursor.fetchall()

    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO posts (`title`, `content`) VALUES ('{}', '{}')".format(
                title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/about', methods=('GET', 'POST'))
def about():
    #server_ip = socket.gethostbyname(socket.gethostname())
    client_ip = request.remote_addr
    return render_template('about.html', client_ip=client_ip, HOST=config.DB_HOST)


@ app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE posts SET `title` = '{}', `content` = '{}' WHERE (`id` = '{}')".format(
                title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@ app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM posts WHERE (`id` = '{}')".format(id))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
