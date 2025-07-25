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

def store_userinfo(ip, user_agent, referrer, timestamp):
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
<nav style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.2em; box-shadow: 0 2px 10px rgba(0,0,0,0.1); position: sticky; top: 0; z-index: 1000;">
  <div style="max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center;">
    <div style="font-size: 1.5em; font-weight: bold; color: #fff; text-shadow: 0 1px 2px rgba(0,0,0,0.3);">
      🐕 Fargo
    </div>
    <div style="display: flex; gap: 2em;">
      <a href="/" style="color: #fff; text-decoration: none; font-weight: 500; padding: 0.5em 1em; border-radius: 25px; transition: all 0.3s ease; hover: background: rgba(255,255,255,0.2); hover: transform: translateY(-2px);">🏠 Home</a>
      <a href="/about" style="color: #fff; text-decoration: none; font-weight: 500; padding: 0.5em 1em; border-radius: 25px; transition: all 0.3s ease; hover: background: rgba(255,255,255,0.2); hover: transform: translateY(-2px);">ℹ️ About</a>
      <a href="/contact" style="color: #fff; text-decoration: none; font-weight: 500; padding: 0.5em 1em; border-radius: 25px; transition: all 0.3s ease; hover: background: rgba(255,255,255,0.2); hover: transform: translateY(-2px);">📞 Contact</a>
    </div>
  </div>
</nav>
'''

HOME_HTML = '''
<html>
  {% extends "base.html" %}

{% block title %}Help Return Fargo - Lost Dog Recovery{% endblock %}

{% block content %}
<div class="container">
    <div class="hero-section">
        <h1 class="hero-title">Help Return Fargo!</h1>
        <p class="hero-subtitle">Our beloved Golden Doodle needs your help to get home</p>
    </div>
    
    <div class="content-section">
        <img src="{{ url_for('static', filename='IMG_6736.jpg') }}" alt="Fargo - Golden Doodle" class="dog-image" style="width: 350px; border: 4px solid #fff; box-shadow: 0 15px 35px rgba(0,0,0,0.2);">
        
        <div class="info-grid">
            <div class="info-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); transform: scale(1.05);">
                <h3>🐕 Name</h3>
                <p style="font-size: 1.4em; font-weight: bold;">Fargo</p>
            </div>
            <div class="info-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); transform: scale(1.05);">
                <h3>🐾 Breed</h3>
                <p style="font-size: 1.4em; font-weight: bold;">Golden Doodle</p>
            </div>
            <div class="info-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); transform: scale(1.05);">
                <h3>👨‍👩‍👧‍👦 Owner</h3>
                <p style="font-size: 1.4em; font-weight: bold;">Confrey Family</p>
            </div>
        </div>
        
        <div style="text-align: center; margin: 3rem 0;">
            <a href="/contact" class="btn" style="font-size: 1.3em; padding: 1.2rem 2.5rem; background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); box-shadow: 0 8px 25px rgba(255,107,107,0.4);">📞 Contact Owner Now</a>
        </div>
    </div>
</div>
{% endblock %}
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
  {% extends "base.html" %}

{% block title %}About - Help Return Fargo{% endblock %}

{% block content %}
<div class="container">
    <div class="hero-section">
        <h1 class="hero-title">About This Website</h1>
        <p class="hero-subtitle">Helping reunite families with their lost pets</p>
    </div>
    
    <div class="content-section">
        <img src="{{ url_for('static', filename='IMG_7041.jpg') }}" alt="Dog paw print" class="dog-image" style="width: 280px; border: 4px solid #fff; box-shadow: 0 15px 35px rgba(0,0,0,0.2);">
        
        <div class="about-text" style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 2.5rem; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
            <p style="font-size: 1.3em; line-height: 1.8; color: #2d3436; margin-bottom: 2rem;">
                This website is designed to help return Fargo to his loving family. If you have found Fargo, 
                please use the contact information provided to reach out to us immediately. 
            </p>
            <p style="font-size: 1.3em; line-height: 1.8; color: #2d3436; margin-bottom: 2rem;">
                Fargo is a friendly Golden Doodle who loves attention and treats. He may be scared and confused 
                being away from home, so please approach him gently if you see him.
            </p>
            <p style="font-size: 1.3em; line-height: 1.8; color: #2d3436;">
                Thank you for helping reunite Fargo with his family! Your kindness means the world to us.
            </p>
        </div>
        
        <div style="text-align: center; margin: 3rem 0;">
            <a href="/contact" class="btn" style="font-size: 1.3em; padding: 1.2rem 2.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); box-shadow: 0 8px 25px rgba(102,126,234,0.4);">📞 Contact Us</a>
        </div>
    </div>
</div>
{% endblock %}
</html>
'''

CONTACT_HTML = '''
<html>
 {% extends "base.html" %}

{% block title %}Contact Owner - Help Return Fargo{% endblock %}

{% block content %}
<div class="container">
    <div class="hero-section">
        <h1 class="hero-title">Contact the Owner</h1>
        <p class="hero-subtitle">Please reach out if you've found Fargo</p>
    </div>
    
    <div class="content-section">
        <div class="emergency-banner" style="font-size: 1.4em; padding: 1.5rem; border-radius: 15px; box-shadow: 0 8px 25px rgba(255,107,107,0.3);">
            🚨 URGENT: If you see Fargo, please contact us immediately! 🚨
        </div>
        
        <img src="{{ url_for('static', filename='IMG_7079.jpg') }}" alt="Fargo with collar" class="dog-image" style="width: 320px; border: 4px solid #fff; box-shadow: 0 15px 35px rgba(0,0,0,0.2);">
        
        <div class="contact-info" style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); box-shadow: 0 15px 35px rgba(255,107,107,0.3);">
            <h2 style="font-size: 2.5em; margin-bottom: 2rem;">Confrey Family</h2>
            <div class="contact-item" style="font-size: 1.5em; margin: 1.5rem 0;">
                📞 <strong>Phone:</strong> <a href="tel:845-536-7118" style="font-size: 1.2em;">845-536-7118</a>
            </div>
            <div class="contact-item" style="font-size: 1.5em; margin: 1.5rem 0;">
                📧 <strong>Email:</strong> <a href="mailto:ifoundfargo@icloud.com" style="font-size: 1.2em;">ifoundfargo@icloud.com</a>
            </div>
            <div class="contact-item" style="font-size: 1.5em; margin: 1.5rem 0;">
                ⏰ <strong>Available:</strong> 24/7 - Please call anytime!
            </div>
        </div>
        
        <div style="text-align: center; margin: 3rem 0;">
            <p style="font-size: 1.2em; color: #666; margin-bottom: 1rem;">
                Thank you for your help in bringing Fargo home safely!
            </p>
            <a href="/" class="btn" style="font-size: 1.3em; padding: 1.2rem 2.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); box-shadow: 0 8px 25px rgba(102,126,234,0.4);">🏠 Back to Home</a>
        </div>
    </div>
</div>
{% endblock %}
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