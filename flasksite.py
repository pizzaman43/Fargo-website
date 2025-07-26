import os
import psycopg2
from flask import Flask, request, render_template_string
from datetime import datetime

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL')  # Set this in Render's environment variables

def init_db():
    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS userinfo (
            id SERIAL PRIMARY KEY,
            ip TEXT,
            user_agent TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def store_userinfo(ip, user_agent, timestamp):
    # Filter out health checks and monitoring tools
    if ip == '127.0.0.1' and user_agent == 'Go-http-client/1.1':
        return
    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()
    c.execute('INSERT INTO userinfo (ip, user_agent, timestamp) VALUES (%s, %s, %s)',
              (ip, user_agent, timestamp))
    conn.commit()
    conn.close()

with app.app_context():
    init_db()

NAVBAR = '''
<style>
.nav-link {
  color: #fff !important;
  text-decoration: none !important;
  font-weight: 500 !important;
  padding: 0.5em 1em !important;
  border-radius: 25px !important;
  transition: all 0.3s ease !important;
}
.nav-link:hover {
  background: rgba(255,255,255,0.2) !important;
  transform: translateY(-2px) !important;
}
</style>
<nav style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.2em; box-shadow: 0 2px 10px rgba(0,0,0,0.1); position: sticky; top: 0; z-index: 1000;">
  <div style="max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center;">
    <div style="font-size: 1.5em; font-weight: bold; color: #fff; text-shadow: 0 1px 2px rgba(0,0,0,0.3);">
      🐕 Fargo
    </div>
    <div style="display: flex; gap: 2em;">
      <a href="/" class="nav-link">🏠 Home</a>
      <a href="/about" class="nav-link">ℹ️ About</a>
      <a href="/contact" class="nav-link">📞 Contact</a>
    </div>
  </div>
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
      <h1>Help Return Fargo!</h1>
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
        <strong>Phone:</strong> <a>845-536-7118</a><br>
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