import sqlite3
# import logging
from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash, Response
from werkzeug.exceptions import abort
from logging.config import dictConfig

total_connections = 0

# Configure Logging
# dictConfig({
#     'version': 1,
#     'formatters': {'default': {
#         'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
#     }},
#     'handlers': {'wsgi': {
#         'class': 'logging.StreamHandler',
#         'stream': 'ext://flask.logging.wsgi_errors_stream',
#         'formatter': 'default'
#     }},
#     'root': {
#         'level': 'DEBUG',
#         'handlers': ['wsgi']
#     }
# })

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    global total_connections
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    total_connections += 1
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
# logging.basicConfig(level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
# logging.basicConfig(level=logging.INFO, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
# logging.basicConfig(level=logging.WARNING, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
# logging.basicConfig(level=logging.ERROR, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app.config['SECRET_KEY'] = 'your secret key'

# HealthCheck
@app.route('/healthz')
def healthz():
    return Response('{"result": "OK - health"}', status=200, mimetype='application/json')

# Metrics page
@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    global total_connections
    posts = connection.execute('SELECT * FROM posts').fetchall()
    total_connections += 1
    post_count = len(posts)
    conn_count = total_connections
    msg = '"db_connection_count": {}, "post_count": {}'.format(conn_count, post_count)
    return Response(msg, status=200, mimetype='application/json')

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    global total_connections
    posts = connection.execute('SELECT * FROM posts').fetchall()
    total_connections += 1
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.error('Nonexistant post access was attempted, id: {}'.format(post_id))
      return render_template('404.html'), 404
    else:
      app.logger.info("Post: {} was accessed.".format(post['title']))
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info('About Page was accessed.')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            global total_connections
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            total_connections += 1
            connection.commit()
            app.logger.info("New post titled: {} was created.".format(title))
            connection.close()

            return redirect(url_for('index'))

    return render_template('create.html')

# start the application on port 3111
if __name__ == "__main__":
    # server = Server(app.wsgi_app)
    app.run(host='0.0.0.0', port='3111', debug=True)
    # app.logger.setLevel(logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # server.serve(port=3111)
