from flask import Flask,render_template,request,redirect,url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, Boolean, inspect
from sqlalchemy.orm import Mapped, mapped_column
from forms import Addform
import os
from dotenv import load_dotenv
from datetime import datetime

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
    form = Addform()
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

#ログイン機能をつけたい。

if __name__ =='__main__':
    app.run(debug=True)
