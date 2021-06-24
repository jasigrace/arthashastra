import os
import pathlib
import cv2
from flask import Flask, render_template, request, session, abort, redirect

import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import smtplib
from flask_sqlalchemy import SQLAlchemy


app = Flask("Google Login App")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


GOOGLE_CLIENT_ID="725966490373-jt3f749q8mqc4igt1co8v0tf7odvnc4s.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)



USER = "iamgrace2113@gmail.com"
PASSWORD = "vwTJ$)1xA5mX$%bJ"

account_sid = 'AC40eac0c6acd601078c4d7f53b67d1daf'
auth_token = '28a5445a102e1881a21855ea1cd0eb66'

#NEWS_API_KEY = "f22b2b12bdcb49a5b8cd7f203dffd293"
#NEWS_URL = "https://newsapi.org/v2/sources"

#news_parameters = {
 #   "category": "business",
  #  "apiKey": NEWS_API_KEY,
#}





# Create Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)


db.create_all()

video_headings = ['Story of Money', 'Goods and Services', 'Producers and Consumers', 'History and Measure of Money', 'Save Money', 'Inflation', 'Banks', 'Making of Coins', 'Functions of Money', 'Evolution of Money', 'Primary Sector', 'Secondary Sector', 'Tertiary Sector']
videos = [
          "https://www.dropbox.com/s/t416oto44q6w2p9/Lecture-1%20ARTHASHASTRA.mp4?raw=1",
          "https://www.dropbox.com/s/m9mw7ckfxt9e128/Lecture-2%20ARTHASHASTRA.mp4?raw=1",
          "https://www.dropbox.com/s/p05cu07m3ad320n/Orange%20and%20White%20Funny%20Dating%20Animated%20Video%20Presentation%20%282%29.mp4?raw=1",
          "https://www.youtube.com/embed/uAm412lkg9o?autoplay=1&mute=0",
          "https://www.youtube.com/embed/hjcZCZBNMTo?autoplay=1&mute=0",
          "https://www.youtube.com/embed/1pzFH7Pcwkg?autoplay=1&mute=0",
          "https://www.youtube.com/embed/elDurqnWDnI?autoplay=1&mute=0",
          "https://www.youtube.com/embed/dLNxyQzbK08?autoplay=1&mute=0",
          "https://www.youtube.com/embed/Rz-xJ-yttOk?autoplay=1&mute=0",
          "https://www.youtube.com/embed/wH01hRoaSL8?autoplay=1&mute=0",
          "https://www.dropbox.com/s/wqrdyrgzro3609k/Orange%20and%20White%20Funny%20Dating%20Animated%20Video%20Presentation.mp4?raw=1",
          "https://www.dropbox.com/s/p05cu07m3ad320n/Orange%20and%20White%20Funny%20Dating%20Animated%20Video%20Presentation%20%282%29.mp4?raw=1",
          "https://www.dropbox.com/s/7ebt2k5yarmscwg/Lecture-3%20ARTHASHASTRA.mp4?raw=1"
          ]


@app.route('/')
def duplicate():
    return render_template('duplicates/duplicate_dashboard.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route("/login1")
def login1():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/home")


@app.route('/home', methods=["GET", "POST"])
def home():
    progress = 0
    certificate = "Activity Log"
    if not request.args.get('id'):
        frame = 'https://www.youtube.com/embed/rYAf_yClD8o'
        heading = 'Lecture'
    else:
        video_num = int(request.args.get('id'))
        progress = round(video_num / len(video_headings) * 100, 2)
        for video in videos:
            if video_num == videos.index(video) + 1:
                frame = video
                heading = video_headings[video_num - 1]
        if video_num == 13:
            certificate = "Certificate"
        else:
            certificate = "Activity Log"
    return render_template('index.html', video=frame, heading=heading, certificate=certificate, progress=progress, value=int(progress))


@app.route('/login', methods=["GET", "POST"])
def login():
    message = "Login"
    if request.method == "POST":
        all_users = User.query.all()
        emails = [user.email for user in all_users]
        passwords = [user.password for user in all_users]
        names = [f'{user.fname} {user.lname}' for user in all_users]
        email = request.form.get('email')
        password = request.form.get('password')
        if email in emails:
            if password == passwords[emails.index(email)]:
                name = names[emails.index(email)]
                print(name)
                print("YES")
                return render_template('dashboard.html', name=name)
            else:
                message = "Invalid Details"
                print("NO")
                return render_template('login.html', message=message)
    return render_template('login.html', message=message)


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        print("HI")
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        print(fname, lname, password, email, cpassword)
        if password == cpassword:
            new_user = User(
                fname=fname,
                lname=lname,
                email=email,
                password=password,
            )
            db.session.add(new_user)
            db.session.commit()
    return render_template('register.html')


@app.route('/password', methods=["POST", "GET"])
def password():
    if request.method == "POST":
        all_users = User.query.all()
        emails = [user.email for user in all_users]
        passwords = [user.password for user in all_users]
        names = [f'{user.fname} {user.lname}' for user in all_users]
        user_email = request.form.get('email')
        for email in emails:
            if email == user_email:
                user_password = passwords[emails.index(user_email)]
                connection = smtplib.SMTP("smtp.gmail.com", port=587)
                connection.starttls()
                connection.login(user=USER, password=PASSWORD)
                connection.sendmail(from_addr=USER,
                                    to_addrs=user_email,
                                    msg=f"Subject: Arthashastra Details!\n\nYour Password: {user_password} ")
                connection.close()
    return render_template('password.html')


@app.route('/practice')
def practice():
    for heading in video_headings:
        if heading == request.args.get('quiz'):
            print(request.args.get('level'))
            return render_template('quiz.html', file=f"practice/quiz_{video_headings.index(heading) + 1}", heading=heading)


@app.route('/easy')
def easy():
    for heading in video_headings:
        if heading == request.args.get('quiz'):
            print(request.args.get('level'))
            return render_template('quiz.html', file=f"easy/quiz_{video_headings.index(heading) + 1}", heading=heading)


@app.route('/medium')
def medium():
    for heading in video_headings:
        if heading == request.args.get('quiz'):
            print(request.args.get('level'))
            return render_template('quiz.html', file=f"medium/quiz_{video_headings.index(heading) + 1}", heading=heading)


@app.route('/hard')
def hard():
    for heading in video_headings:
        if heading == request.args.get('quiz'):
            print(request.args.get('level'))
            return render_template('quiz.html', file=f"hard/quiz_{video_headings.index(heading) + 1}", heading=heading)


@app.route('/levels')
def levels():
    return render_template('levels.html', level=request.args.get('level'))


@app.route('/news')
def news():
    #news_response = requests.get(url=NEWS_URL, params=news_parameters)
    #news_article = []
    #for i in range(1, 7):
     #   news_article.append(news_response.json()['sources'][i]['description'])
    return render_template('news.html')


@app.route('/certificate', methods=["POST", "GET"])
def certificate():
    if request.method == "POST":
        email = request.form.get('email')
        all_users = User.query.all()
        emails = [user.email for user in all_users]
        names = [f'{user.fname} {user.lname}' for user in all_users]
        for mail in emails:
            if email == mail:
                name = names[emails.index(email)]
                path = 'static/pictures/certificate.jpeg'
                image = cv2.imread(path)
                font = cv2.FONT_HERSHEY_SIMPLEX
                org = (550, 430)
                fontScale = 1
                color = (255, 255, 255)
                thickness = 2
                image = cv2.putText(image, name.upper(), org, font,
                                    fontScale, color, thickness, cv2.LINE_AA)
                cv2.imwrite(f'static/pictures/{name}.jpeg', image)
                return render_template('certificate.html', name=name)
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
