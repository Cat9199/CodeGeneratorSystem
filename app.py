# Modules
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,session
from PIL import Image, ImageDraw, ImageFont
from flask_sqlalchemy import SQLAlchemy
from sendtodb import add_post_and_meta
from sqlalchemy.sql import func
import random
import os
import datetime
import pytz
#Data Base
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)  
app.secret_key = 'code.yahia'

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# DB Shemae
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200)) 
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80))
    host = db.Column(db.String(200))
    user = db.Column(db.String(200))
    passworddb = db.Column(db.String(200))
    database = db.Column(db.String(200))  
    Tcode = db.Column(db.Integer)  
class Codes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    code = db.Column(db.String(80))
    price = db.Column(db.String(200))
    date = db.Column(db.String(200))
class Actions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)        # Use the default font
    codenum = db.Column(db.Integer)
    codeprice = db.Column(db.Integer)
    date = db.Column(db.String(200))
    stat = db.Column(db.Integer)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def gtime():
    egypt_timezone = pytz.timezone('Africa/Cairo')
    current_time = datetime.datetime.now(egypt_timezone)
    current_time = current_time.replace(microsecond=0, tzinfo=None)
    return current_time
@app.route('/allc')
def allc():
    codes = Codes.query.all()
    codes= codes[::-1]
    return render_template('tabel.html',codes=codes)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method =='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user =User.query.filter_by(username=username,password=password).first()
        if user:
            session['username'] = username
            return redirect('/createcode')
        else: 
            return render_template('login.html',mess='error')
    return render_template('login.html')
@app.route('/createcode')
def createcode():
    username = session.get('username')
    if username :
        return render_template('gcode.html')
    else:
        return redirect('/login')
@app.route('/logout')
def logout():
    session['username'] = None
    return redirect('/')
@app.route('/loginadmin',methods=['POST','GET'])
def lognadmin():
    if request.method == 'POST':
        user = request.form.get('user')
        admin='E3lanoTopia@admin-2023'
        if user == admin:
            session['admin']= 'admin'
            return redirect('/dashboard')
        else:
            return redirect('/')
    return render_template('adminlogin.html')
@app.route('/process', methods=['POST'])
def process_files():
    username = session.get('username')
    if username:
        info = User.query.filter_by(username=username).first()
        img_file = request.files['img']
        if img_file.filename == '' or not allowed_file(img_file.filename):
            return redirect(request.url)
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], 'input_image.jpg')
        img_file.save(img_path)
        font_color = request.form['font_color']
        num = request.form['num']
        price = request.form['price']
        p_type = request.form['p-type']
        output_filenames = process_random_numbers(img_path,host=info.host,user=info.user,password=info.passworddb,database=info.database,font_size= 50,num=int(num),font_color=font_color,code_position=330,price=price)
        if p_type == 'print':
            return redirect(url_for('result1', filenames=output_filenames))
        else:
            return redirect(url_for('result2', filenames=output_filenames))
def process_random_numbers(img_path, font_size, font_color, code_position, host, user, password, database, num, price):
    output_filenames = []
    username = session.get('username')
    
    for index in range(num):
        random_code = str(random.randint(1000000000, 9999999999))
        img = Image.open(img_path)
        draw = ImageDraw.Draw(img)
        add_post_and_meta(meta_value=price, credintial=random_code, host=host, user=user, password=password, database=database)

        new_code = Codes(
            username=username,
            code=random_code,
            price=price,
            date=gtime()
        )
        db.session.add(new_code)
        font = ImageFont.truetype("Pillow/Tests/fonts/FreeMonoBold.ttf", font_size)
        y_position = code_position
        draw.text((100, y_position), random_code, font=font, fill=font_color)
        output_filename = f'output_{index}.jpg'
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        img.save(output_path)
        output_filenames.append(output_filename)
    new_ac = Actions(
        username=username,
        codenum=num,
        codeprice=price,
        date=gtime(),
        stat=0,
    )
    db.session.add(new_ac)
    db.session.commit()
    return output_filenames
@app.route('/dashboard')
def dashboard():
    user = session.get('admin')
    if user :
        codes = Actions.query.all()
        codes =codes[::-1]
        return render_template('dashboard.html',codes=codes)
    else:
        return render_template('404.html')
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
@app.route('/adduser',methods=['POST','GET'])
def adduser():
    user = session.get('admin')
    if user :
        if request.method == 'POST':
            name = request.form.get('name')
            username = request.form.get('username')
            Host = request.form.get('Host')
            password = request.form.get('password')
            database = request.form.get('database')
            database_username = request.form.get('database-username')
            database_password = request.form.get('database-password')
            newuser = User(
                name = name,
                username = username,
                password = password,
                host=Host,
                passworddb = database_password,
                user=database_username,
                database = database,
                Tcode = 0                
            )
            db.session.add(newuser)
            db.session.commit()
            return render_template('create-account.html',mess='ok')
        return render_template('create-account.html')
    else:
        return render_template('404.html')
@app.route('/result1')
def result1():
    return render_template('result1.html', filenames=request.args.getlist('filenames'))
@app.route('/result2')
def result2():
    return render_template('result2.html', filenames=request.args.getlist('filenames'))
@app.route('/ac')
def ac():
    user = session.get('admin')
    if user :
        ac = Actions.query.filter_by(stat=0).all()
        return render_template('ac.html',codes=ac)
    else:
        return render_template('404.html')
@app.route('/okk/<int:id>')
def okk(id):
    user = session.get('admin')
    if user :
        ss = Actions.query.get(id)
        ss.stat = 1
        db.session.commit()
        return redirect('/ac')
    else:
        return render_template('404.html')
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    with app.app_context():
        db.create_all()
    app.run(debug=True,host='0.0.0.0')

