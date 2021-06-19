from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/home', methods=["GET", "POST"])
def home():
    if not request.args.get('id'):
        frame = 'https://www.youtube.com/embed/rYAf_yClD8o'
        heading = 'Lecture'
    else:
        video_num = int(request.args.get('id'))
        video_headings = ['Primary Sector', 'Secondary Sector', 'Tertiary Sector']
        videos = ["https://www.youtube.com/embed/0GJN5pyxWFQ", "https://www.youtube.com/embed/rYAf_yClD8o", "https://www.youtube.com/embed/lj4lrMudcIQ"]
        for video in videos:
            if video_num == videos.index(video) + 1:
                frame = video
                heading = video_headings[video_num - 1]
    return render_template('index.html', video=frame, heading=heading)


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/password')
def password():
    return render_template('password.html')


@app.route('/page_not_found')
def page_not_found():
    return render_template('404.html')


@app.route('/unauthorized')
def unauthorized():
    return render_template('401.html')


@app.route('/server_error')
def server_error():
    return render_template('500.html')


if __name__ == '__main__':
    app.run(debug=True)
