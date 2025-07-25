from flask import Flask, request, render_template_string
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('userinfo.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS userinfo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            user_agent TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def store_userinfo(ip, user_agent, referrer, timestamp):
    conn = sqlite3.connect('userinfo.db')
    c = conn.cursor()
    c.execute('INSERT INTO userinfo (ip, user_agent, timestamp) VALUES (?, ?, ?)',
              (ip, user_agent, timestamp))
    conn.commit()
    conn.close()

with app.app_context():
    init_db()

NAVBAR = '''
<nav style="background:#333;padding:1em;">
  <a href="/" style="color:#fff;margin-right:1em;">Home</a>
  <a href="/about" style="color:#fff;margin-right:1em;">About</a>
  <a href="/contact" style="color:#fff;">Contact</a>
</nav>
'''

HOME_HTML = '''
<html>
  <head>
    <title>Return My Dog - Home</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 0; background: #f4f4f4; }
      .container { max-width: 700px; margin: 40px auto; background: #fff; padding: 2em; border-radius: 8px; box-shadow: 0 2px 8px #ccc; }
      h1, h2 { text-align: center; }
      .dog-img { display: block; margin: 2em auto 1em auto; border-radius: 10px; box-shadow: 0 2px 8px #bbb; width: 250px; }
      .info { text-align: center; font-size: 1.1em; margin-bottom: 2em; }
      .ip { margin-top: 2em; text-align: center; color: #555; font-size: 0.95em; }
      .center-btn { display: flex; justify-content: center; margin-top: 2em; }
      .my-btn { background: #333; color: #fff; border: none; padding: 0.8em 2em; border-radius: 5px; font-size: 1em; cursor: pointer; }
      .my-btn:hover { background: #555; }
    </style>
  </head>
  <body>
    ''' + NAVBAR + '''
    <div class="container">
      <h1>Help Return My Dog!</h1>
      <img src="/static/IMG_6736.jpg" alt="Dog photo" class="dog-img">
      <div class="info">
        <strong>Name:</strong> Fargo<br>
        <strong>Breed:</strong> Golden Doodle<br>
        <strong>Owner:</strong> Confrey Family<br>
      </div>
      <div class="center-btn">
        <button class="my-btn" onclick="window.location.href='/contact'">Contact Owner</button>
      </div>
    </div>
  </body>
</html>
'''

ABOUT_HTML = '''
<html>
  <head>
    <title>About - Return My Dog</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 0; background: #f4f4f4; }
      .container { max-width: 700px; margin: 40px auto; background: #fff; padding: 2em; border-radius: 8px; box-shadow: 0 2px 8px #ccc; }
      h1 { text-align: center; }
      .about-img { display: block; margin: 2em auto 1em auto; border-radius: 10px; box-shadow: 0 2px 8px #bbb; width: 200px; }
      p { font-size: 1.1em; }
    </style>
  </head>
  <body>
    ''' + NAVBAR + '''
    <div class="container">
      <h1>About This Website</h1>
      <img src="/static/IMG_7041.jpg" alt="Dog paw" class="about-img">
      <p>
        This website is designed to help return Fargo to us. If you have found Fargo, please use the contact information provided to reach out to us. Thank you for helping reunite Fargo with us!
      </p>
    </div>
  </body>
</html>
'''

CONTACT_HTML = '''
<html>
  <head>
    <title>Contact Owner - Return My Dog</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 0; background: #f4f4f4; }
      .container { max-width: 700px; margin: 40px auto; background: #fff; padding: 2em; border-radius: 8px; box-shadow: 0 2px 8px #ccc; }
      h1 { text-align: center; }
      .contact-img { display: block; margin: 2em auto 1em auto; border-radius: 10px; box-shadow: 0 2px 8px #bbb; width: 180px; }
      .contact-info { text-align: center; font-size: 1.1em; }
    </style>
  </head>
  <body>
    ''' + NAVBAR + '''
    <div class="container">
      <h1>Contact the Owner</h1>
      <img src="/static/IMG_7079.jpg" alt="Dog with collar" class="contact-img">
      <div class="contact-info">
        <strong>Confrey family</strong><br>
        <strong>Phone:</strong> <a>555-123-4567</a><br>
        <strong>Email:</strong> <a>ifoundfargo@icloud.com</a>
      </div>
    </div>
  </body>
</html>
'''

@app.route('/')
def home():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent', '')
    referrer = request.referrer or ''
    timestamp = datetime.now().isoformat()
    store_userinfo(ip, user_agent, referrer, timestamp)
    return render_template_string(HOME_HTML, ip=ip)

@app.route('/about')
def about():
    return render_template_string(ABOUT_HTML)

@app.route('/contact')
def contact():
    return render_template_string(CONTACT_HTML)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=False, host="0.0.0.0", port=port)