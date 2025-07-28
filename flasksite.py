import os
from datetime import datetime

import psycopg2
import requests
from dotenv import load_dotenv
from flask import Flask, render_template_string, request
from user_agents import parse as parse_user_agent

load_dotenv()

Rewardpage = os.getenv("Rewardpage")
print("Rewardpage:", Rewardpage)

phone_env = os.getenv("Phone")
nophone = ""


if rewardpage == True:
  homeheading = '<h1>Help Return Fargo, <span style="color: red;">Reward Offered!</span></h1>'
else:
    homeheading = "<h1>Help Return Fargo</h1>"


# Get Render's DATABASE_URL from environment
DATABASE_URL = os.environ.get("DATABASE_URL")  # in Render settings

app = Flask(__name__)


def init_db():
    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS visits (
            id SERIAL PRIMARY KEY,
            ip TEXT,
            location TEXT,
            device TEXT,
            browser TEXT,
            os TEXT,
            referrer TEXT,
            timestamp TIMESTAMPTZ DEFAULT NOW()
        )
    """
    )
    conn.commit()
    conn.close()


def get_real_ip(request):
    xff = request.headers.get("X-Forwarded-For", request.remote_addr)
    return xff.split(",")[0].strip()


def geolocate_ip(ip):
    try:
        res = requests.get(f"https://ipapi.co/{ip}/json/")
        data = res.json()
        return f"{data.get('city', '?')}, {data.get('region', '?')}, {data.get('country_name', '?')}"
    except:
        return "Unknown Location"


def store_visit(request):
    ip = get_real_ip(request)
    user_agent_string = request.headers.get("User-Agent")
    timestamp = datetime.utcnow().isoformat()
    ua = request.headers.get("User-Agent", "")
    if "Go-http-client" in ua:
        return  # Skip storing these requests

    # Parse user agent
    ua = parse_user_agent(user_agent_string)
    device = "Mobile" if ua.is_mobile else "Tablet" if ua.is_tablet else "PC"
    browser = f"{ua.browser.family} {ua.browser.version_string}"
    os = f"{ua.os.family} {ua.os.version_string}"

    location = geolocate_ip(ip)
    referrer = request.referrer or "Direct"

    # Insert into PostgreSQL
    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO visits (ip, location, device, browser, os, referrer, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """,
        (ip, location, device, browser, os, referrer, timestamp),
    )
    conn.commit()
    conn.close()


# Initialize table when app starts
with app.app_context():
    init_db()


if Rewardpage == "True":
    NAVBAR = """
    <style>
      .nav-link {
        color: #fff !important;
        text-decoration: none !important;
        font-weight: 500 !important;
        padding: 0.6em 1.2em !important;
        border-radius: 30px !important;
        transition: background 0.3s ease, transform 0.2s ease !important;
      }
      .nav-link:hover {
        background: rgba(255,255,255,0.25) !important;
        transform: translateY(-3px) !important;
      }
    </style>
    <nav style="background: linear-gradient(135deg, #5f72be 0%, #9921e8 100%); padding: 1.2em; box-shadow: 0 3px 12px rgba(0,0,0,0.1); position: sticky; top: 0; z-index: 1000;">
      <div style="max-width: 1100px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center;">
        <div style="font-size: 1.6em; font-weight: bold; color: #fff; text-shadow: 0 1px 2px rgba(0,0,0,0.3);">
          🐕 Fargo
        </div>
        <div style="display: flex; gap: 1.8em;">
          <a href="/" class="nav-link">🏠 Home</a>
          <a href="/about" class="nav-link">ℹ️ About</a>
          <a href="/contact" class="nav-link">📞 Contact</a>
          <a href="/reward" class="nav-link">🏅 Reward</a>
        </div>
      </div>
    </nav>
    """
else:
    NAVBAR = """
<style>
  .nav-link {
    color: #fff !important;
    text-decoration: none !important;
    font-weight: 500 !important;
    padding: 0.6em 1.2em !important;
    border-radius: 30px !important;
    transition: background 0.3s ease, transform 0.2s ease !important;
  }
  .nav-link:hover {
    background: rgba(255,255,255,0.25) !important;
    transform: translateY(-3px) !important;
  }
</style>
<nav style="background: linear-gradient(135deg, #5f72be 0%, #9921e8 100%); padding: 1.2em; box-shadow: 0 3px 12px rgba(0,0,0,0.1); position: sticky; top: 0; z-index: 1000;">
  <div style="max-width: 1100px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center;">
    <div style="font-size: 1.6em; font-weight: bold; color: #fff; text-shadow: 0 1px 2px rgba(0,0,0,0.3);">
      🐕 Fargo
    </div>
    <div style="display: flex; gap: 1.8em;">
      <a href="/" class="nav-link">🏠 Home</a>
      <a href="/about" class="nav-link">ℹ️ About</a>
      <a href="/contact" class="nav-link">📞 Contact</a>
    </div>
  </div>
</nav>
"""


reward_section = ""
if Rewardpage == "True":
    reward_section = """
    <div style="background: #fdecea; color: #b12727; border: 2px solid #f5c6cb; padding: 1em; margin: 1.5em 0; border-radius: 10px;">
      <strong>Reward offered for finding Fargo!</strong>
      <div style="margin-top: 1em;">
        <button class="my-btn" onclick="window.location.href='/reward'">View Reward Details</button>
      </div>
    </div>
    """

HOME_HTML = (
    """
<html>
  <head>
    <title>Return My Dog - Home</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      body {
        font-family: 'Segoe UI', sans-serif;
        margin: 0;
        background: #f5f7fa;
        color: #333;
        display: flex;
        flex-direction: column;
        min-height: 100vh;
      }
      .container {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2em 1em;
      }
      .content-box {
        width: 100%;
        max-width: 720px;
        background: #fff;
        padding: 2em;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        text-align: center;
      }
      .dog-img {
        margin: 1.5em auto;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        width: 100%;
        max-width: 300px;
        height: auto;
      }
      .info {
        font-size: 1.1em;
        line-height: 1.6em;
        margin: 1.5em 0;
      }
      .center-btn {
        margin-top: 2em;
      }
      .my-btn {
        background: #5f72be;
        color: #fff;
        border: none;
        padding: 0.9em 2.2em;
        border-radius: 8px;
        font-size: 1.05em;
        cursor: pointer;
        transition: background 0.3s ease;
      }
      .my-btn:hover {
        background: #4a5bb3;
      }
    </style>
  </head>
  <body>
"""
    + NAVBAR
    + """
    <div class="container">
      <div class="content-box">
        """
    + homeheading
    + """
        <img src="/static/IMG_6736.jpg" alt="Dog photo" class="dog-img">
        <div class="info">
          <strong>Name:</strong> Fargo<br>
          <strong>Breed:</strong> Golden Doodle<br>
          <strong>Owner:</strong> Confrey Family<br>
        </div>
"""
    + reward_section
    + """
        <div class="center-btn">
          <button class="my-btn" onclick="window.location.href='/contact'">Contact Owner</button>
        </div>
      </div>
    </div>
  </body>
</html>
"""
)


ABOUT_HTML = (
    """
<html>
  <head>
    <title>About - Return My Dog</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      body {
        font-family: 'Segoe UI', sans-serif;
        margin: 0;
        background: #f5f7fa;
        color: #333;
        display: flex;
        flex-direction: column;
        min-height: 100vh;
      }
      .container {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2em 1em;
      }
      .content-box {
        width: 100%;
        max-width: 720px;
        background: #fff;
        padding: 2em;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        text-align: center;
      }
      .about-img {
        margin: 1.5em auto;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        width: 100%;
        max-width: 250px;
        height: auto;
      }
      p {
        font-size: 1.1em;
        line-height: 1.6em;
        margin-top: 1.5em;
      }
    </style>
  </head>
  <body>
    """
    + NAVBAR
    + """
    <div class="container">
      <div class="content-box">
        <h1>About This Website</h1>
        <img src="/static/IMG_7041.jpg" alt="Dog paw" class="about-img">
        <p>
          This website is designed to help return Fargo to us. If you have found Fargo,
          please use the contact information provided to reach out. Thank you for helping reunite Fargo with us!
        </p>
      </div>
    </div>
  </body>
</html>
"""
)


CONTACT_HTML = (
    """
<html>
  <head>
    <title>Contact Owner - Return My Dog</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      body {
        font-family: 'Segoe UI', sans-serif;
        margin: 0;
        background: #f5f7fa;
        color: #333;
        display: flex;
        flex-direction: column;
        min-height: 100vh;
      }
      .container {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2em 1em;
      }
      .content-box {
        width: 100%;
        max-width: 720px;
        background: #fff;
        padding: 2em;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        text-align: center;
      }
      .contact-img {
        margin: 1.5em auto;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        width: 100%;
        max-width: 220px;
        height: auto;
      }
      .contact-info {
        font-size: 1.1em;
        line-height: 1.6em;
        margin-top: 1.5em;
      }
      a {
        color: #5f72be;
        text-decoration: none;
      }
    </style>
  </head>
  <body>
    """
    + NAVBAR
    + """
    <div class="container">
      <div class="content-box">
        <h1>Contact the Owner</h1>
        <img src="/static/IMG_5463.jpeg" alt="Dog with collar" class="contact-img">
        <div class="contact-info">
          <strong>Confrey family</strong><br>
          """
    + phoneornot
    + """
          <strong>Email:</strong> <a href="mailto:ifoundfargo@icloud.com">ifoundfargo@icloud.com</a>
        </div>
      </div>
    </div>
  </body>
</html>
"""
)

REWARD_HTML = (
    """
<html>
  <head>
    <title>Reward for Finding Fargo</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      body {
        font-family: 'Segoe UI', sans-serif;
        margin: 0;
        background: #f5f7fa;
        color: #333;
        display: flex;
        flex-direction: column;
        min-height: 100vh;
      }
      .container {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2em 1em;
      }
      .content-box {
        width: 100%;
        max-width: 720px;
        background: #fff;
        padding: 2em;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        text-align: center;
      }
      .reward-img {
        margin: 1.5em auto;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        width: 100%;
        max-width: 300px;
        height: auto;
      }
      .reward-text {
        font-size: 1.2em;
        line-height: 1.6em;
        margin-top: 1.5em;
      }
      .reward-amount {
        font-size: 2em;
        font-weight: bold;
        color: #e63946;
        margin-top: 0.5em;
      }
      .contact-link {
        display: inline-block;
        margin-top: 2em;
        background: #5f72be;
        color: white;
        padding: 0.9em 2em;
        border-radius: 8px;
        text-decoration: none;
        font-size: 1.05em;
        transition: background 0.3s ease;
      }
      .contact-link:hover {
        background: #4a5bb3;
      }
    </style>
  </head>
  <body>
    """
    + NAVBAR
    + """
    <div class="container">
      <div class="content-box">
        <h1>Reward Offered</h1>
        <img src="/static/IMG_7079.jpg" alt="Reward image of Fargo" class="reward-img">
        <div class="reward-text">
          Fargo is missing and we are offering a reward to anyone who helps bring him home.
        </div>
        <div class="reward-amount">
           $200 REWARD!
        </div>
        <div class="reward-text">
          No questions asked — if you’ve seen or found Fargo, please reach out right away.
        </div>
        <a class="contact-link" href="/contact">📞 Contact Us</a>
      </div>
    </div>
  </body>
</html>
"""
)


@app.route("/")
def home():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent = request.headers.get("User-Agent", "")
    referrer = request.referrer or ""
    timestamp = datetime.now().isoformat()
    store_visit(request)
    return render_template_string(HOME_HTML, ip=ip)


@app.route("/about")
def about():
    return render_template_string(ABOUT_HTML)


@app.route("/contact")
def contact():
    return render_template_string(CONTACT_HTML)


if Rewardpage == "True":

    @app.route("/reward")
    def reward():
        return render_template_string(REWARD_HTML)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=False, host="0.0.0.0", port=port)
