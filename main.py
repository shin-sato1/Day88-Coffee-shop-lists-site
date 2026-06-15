from flask import Flask,render_template,request,redirect,url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, Boolean, inspect
from sqlalchemy.orm import Mapped, mapped_column
import os
from dotenv import load_dotenv

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


# with app.app_context():
#     cafe_from_db = db.session.execute(db.select(Cafe)).scalars().all()
#     for item in cafe_from_db:
#         print(item)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/cafes')
def cafe():
    cafe_from_db = db.session.execute(db.select(Cafe)).scalars().all()
    return render_template('cafe.html',cafe_info=cafe_from_db)


@app.route('/add')
def add():
    return



if __name__ =='__main__':
    app.run(debug=True)
