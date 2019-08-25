from datetime import datetime
import math
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"

Base = declarative_base()

class Atlet(Base):
	__tablename__ = 'athelete'
	id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
	age = sa.Column(sa.Integer)
	birthdate = sa.Column(sa.Text)
	gender = sa.Column(sa.Text)
	height = sa.Column(sa.Float)
	name = sa.Column(sa.Text)
	weight = sa.Column(sa.Integer)
	gold_medals = sa.Column(sa.Integer)
	silver_medals = sa.Column(sa.Integer)
	bronze_medals = sa.Column(sa.Integer)
	total_medals = sa.Column(sa.Integer)
	sport = sa.Column(sa.Text)
	country = sa.Column(sa.Text)

#class Sqs(Base):
#	__tablename__ = 'sqlite_sequence'

class User(Base):
	__tablename__ = "user"
	id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
	first_name = sa.Column(sa.Text)
	last_name = sa.Column(sa.Text)
	gender = sa.Column(sa.Text)
	email = sa.Column(sa.Text)
	birthdate = sa.Column(sa.Text)
	height = sa.Column(sa.Float)

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()

def reg():
	print("Go!")
	name = input("Enter our name:")
	surname = input("Enter our surname:")
	gender = input("Enter our gender:")
	email = input("Enter our email:")
	birthdate = input("Enter our birthdate:")
	height = input("Enter our hieght:")

	session.add(User(first_name = name, 
		last_name = surname, 
		gender = gender, 
		email = email, 
		birthdate = birthdate, 
		height = height))
	session.commit()
	print("Спасибо, данные сохранены!")

def find(user):
	print("В базе 'User' найден пользователь с именем:{}, фамилией {}, ростом: {}, и днём рождения:{}".format(user.first_name, user.last_name, user.height, user.birthdate))
	atlets = session.query(Atlet)
	def_height = 200.0
	for men in atlets:
		if men.height is not None:
			confronto = math.fabs(user.height - men.height)
			if confronto < def_height:
				def_height = confronto
				min_def_height_people = men
	print("В базе 'Atlets' найден спортсмен с именем:{}, возрастом {}, ростом: {}".format(min_def_height_people.name, min_def_height_people.age, min_def_height_people.height))
	minTimeDef(user, atlets)


def minTimeDef(target, atlets):
	birthdate = datetime.strptime(target.birthdate, '%d.%m.%Y')
	def_birthday = datetime.now() - birthdate
	need_atlet = atlets[0]
	for atlet in atlets:
		if atlet == target:
			continue
		if birthdate > datetime.strptime(atlet.birthdate, '%Y-%m-%d'):
			timedelta = birthdate -  datetime.strptime(atlet.birthdate, '%Y-%m-%d')
		else:
			timedelta = datetime.strptime(atlet.birthdate, '%Y-%m-%d')- birthdate
		if atlet.birthdate is not None:
			if def_birthday > timedelta:
				def_birthday = timedelta
				need_atlet = atlet
	print("В базе 'Atlets' найден спортсмен с именем:{}, возрастом {}, ростом: {} и датой рождения: {}".format(need_atlet.name, need_atlet.age, need_atlet.height, need_atlet.birthdate))

def show():
	user_list = session.query(User).all()
	for user in user_list:
		print("Имя: {}, фамилия: {}, email: {}, день рождения: {}".format(user.first_name, user.last_name, user.email, user.birthdate))

def id_test():
	identif = int(input("Input athelete id:"))
	user_count = session.query(User).count()
	if identif > user_count:
		print("It`s wrong id, try again!")
	else: find(session.query(User).filter(User.id == identif).first())

session = connect_db()
select = ""
while(select != 2):
	print("Choice:")
	print("1. Register new user.")
	print("2. Show all users")
	print("3. Find.")
	print("4. Exit.")

	select = input()
	if select == "1":
		reg()
	elif select == "3":
		id_test()
	elif select == "2":
		show()
	else:
		select = 2

