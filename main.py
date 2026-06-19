import os
from dotenv import load_dotenv
from datetime import datetime
from flask import Flask,render_template,request,redirect,url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, Boolean, inspect
from sqlalchemy.orm import Mapped, mapped_column
from forms import AddForm, RegisterForm, LoginForm
from flask_login import LoginManager,UserMixin,login_user,current_user,logout_user
from werkzeug.security import generate_password_hash, check_password_hash


load_dotenv()

app = Flask(__name__)
#環境変数に入れる
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
Bootstrap5(app)


#create database
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    name:  Mapped[str] = mapped_column(String,nullable=False)
    email: Mapped[str] = mapped_column(String,nullable=False)
    password: Mapped[str] = mapped_column(String,nullable=False)


class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    name: Mapped[str] = mapped_column(String(250),unique=True,nullable=False)
    map_url: Mapped[str] = mapped_column(String(500),nullable=False)
    img_url: Mapped[str] = mapped_column(String(500),nullable=False)
    location: Mapped[str] = mapped_column(String(250),nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean,nullable=False)
    has_toilet:  Mapped[bool] = mapped_column(Boolean,nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean,nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean,nullable=False)
    seats: Mapped[str] = mapped_column(String(250))
    coffee_price: Mapped[str] = mapped_column(String(250))

#テーブルを作成
with app.app_context():
    db.create_all()

# with app.app_context():
#     cafe_from_db = db.session.execute(db.select(Cafe)).scalars().all()
#     for item in cafe_from_db:
#         print(item)

# ログイン
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User,int(user_id))

@app.context_processor
def inject():
    return{
        'current_year': datetime.now().year,
    }

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/cafes')
def cafe():
    cafe_from_db = db.session.execute(db.select(Cafe)).scalars().all()
    return render_template('cafe.html',cafe_info=cafe_from_db)


@app.route('/add',methods=['GET','POST'])
def add():
    form = AddForm()
    if form.validate_on_submit():
        name = form.cafe_name.data
        location = form.location.data
        price = form.coffee_price.data
        map_url = form.map_url.data
        img_url = form.img_url.data
        socket = form.sockets.data == 'True'
        toilet = form.toilets.data == 'True'
        wifi = form.wifis.data == 'True'
        call = form.calls.data == 'True'
        seat = form.seats.data == 'True'

        
        new_cafe = Cafe(
            name = name,
            map_url = map_url,
            img_url = img_url,
            location = location,
            has_sockets = socket,
            has_toilet = toilet,
            has_wifi = wifi,
            can_take_calls = call,
            seats = seat,
            coffee_price = price,
        )

        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('cafe'))

    return render_template('add.html',form=form)

#edit機能とdelete機能をつけたい
@app.route('/delete/<int:cafe_id>')
def delete(cafe_id):
    cafe_to_delete = db.get_or_404(Cafe,cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('home'))




#ログイン機能をつけたい。
@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        hashed_password = generate_password_hash(
            password=password,
            method='pbkdf2:sha256',
            salt_length=8,
        )

        new_user = User(
            name = name,
            email = email,
            password = hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        #login for new user
        login_user(new_user)
        return redirect(url_for('home'))
    
    return render_template('register.html',form=form)

#ログインした後
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        check_login_user = db.session.execute(
            db.select(User).where(User.email == email)
        ).scalar()

        if not check_login_user:
            return redirect(url_for('login'))
        
        check_password = check_password_hash(
            pwhash = check_login_user.password,
            password = password
        )

        if check_password:
            login_user(check_login_user)
            return redirect(url_for('home'))
        
        else:
            return redirect(url_for('login'))
        
    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ =='__main__':
    app.run(debug=True)
