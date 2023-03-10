from config import load_config
import pandas
from sqlalchemy import create_engine, text
import sqlalchemy


url_object = sqlalchemy.engine.url.URL(
    "postgresql+psycopg2",
    username='postgres',
    password='1234',
    host='db',
    database='telegrambot',
    port='5432',
    query={'sslmode': 'disable'}
)

# Подключаемся к PostgreSql
# connection = pymysql.connect(
#     host='db',
#     user='postgres',
#     password='1234',
#     database='telegrambot',
#     cursorclass=cursors.DictCursor,
#     autocommit=True,
# )
engine = create_engine(url_object)
# with engine.begin() as cursor:
#     cursor.execute(text(
#         """
#         CREATE TABLE "users"(
#             id bigserial PRIMARY KEY,
#             user_id bigint NOT NULL,
#             GX varchar(15) DEFAULT NULL,
#             status boolean DEFAULT NULL,
#             lan varchar(15) NOT NULL
#             );
#         """
#         ))
# #         ALTER TABLE "users" ALTER COLUMN user_id TYPE bigint;
# #         """
# #     cursor.execute(text(
# #         """
# #         ALTER TABLE "admin" ALTER COLUMN user_id TYPE bigint;
# #         """
# #     ))
    
# #         
# with engine.begin() as cursor:
#     cursor.execute(text(
#         """
#         CREATE TABLE "admin"(
#         id bigserial PRIMARY KEY,
#         user_id bigint NOT NULL UNIQUE,
#         is_admin boolean NOT NULL
#         );
#         """
#     ))

# with engine.begin() as cursor:
#     cursor.execute(text(
#         """
        # CREATE TABLE product(
        # number varchar(100),
        # date varchar(100),
        # trek varchar(100),
        # weight varchar(100),
        # price varchar(100),
        # consumption varchar(100),
        # sum varchar(100),
        # status varchar(100),
        # auto varchar(100)
        # );
#         """
#     ))



def get_subscriptions(status=True):
    # connection.ping()
    with engine.begin() as cursor:
        result = cursor.execute(text(
            f"SELECT * FROM users WHERE status={status};"
        ))
        return result.fetchall()


def get_by_gx(gx):
    # connection.ping()
    with engine.begin() as cursor:
        result = cursor.execute(text(
            f"SELECT * FROM users WHERE gx='{gx}';"
        ))
        return result.fetchall()


def user_exists(user_id, gx):
    # connection.ping()
    """Проверяем существует ли пользователь"""
    with engine.begin() as cursor:
        result = cursor.execute(text(
            f"SELECT * FROM users WHERE user_id='{user_id}' AND gx='{gx}';"
        ))
        try:
            result.fetchall()[0]
            return True
        except IndexError:
            return False


def subscriber_status(user_id):
    # connection.ping()
    """Проверяем активен ли пользователь"""
    with engine.begin() as cursor:
        result = cursor.execute(text(
            f"SELECT status FROM users WHERE user_id='{user_id}';"
        ))
        return True in result.fetchone()


def add_subscriber(user_id, gx, status=True):
    # connection.ping()
    """Добавляем пользователя"""
    with engine.begin() as cursor:
        cursor.execute(text(
            f"UPDATE users SET gx = '{gx}', status = {status} WHERE user_id = '{user_id}';"
        ))


def update_subscription(user_id, status):
    # connection.ping()
    """Обновляем статус подписки"""
    with engine.begin() as cursor:
        cursor.execute(text(
            f"UPDATE users SET status = {status} WHERE user_id = '{user_id}';"
        ))


def get_lan(user_id):
    # connection.ping()
    """Получаем язык"""
    with engine.begin() as cursor:
        result = cursor.execute(text(
            f'SELECT lan FROM users WHERE user_id = {user_id};'
        ))
        try:
            return result.fetchone()
        except Exception:
            return False


def add_lan(user_id, lan):
    # connection.ping()
    """Добавляем язык"""
    with engine.begin() as cursor:
        cursor.execute(text(
            f"INSERT INTO users (user_id, lan) VALUES ({user_id}, '{lan}')"
        ))


def update_lan(user_id, lan):   
    # connection.ping()
    """Обновляем язык"""
    with engine.begin() as cursor:
        cursor.execute(text(
            f"UPDATE users SET lan = '{lan}' WHERE user_id = {user_id}"
        ))


def check_admin(user_id):
    # connection.ping()
    """Проверяем на права админа"""
    with engine.begin() as cursor:
        result = cursor.execute(text(
            f"SELECT is_admin FROM admin WHERE user_id={user_id};"
        ))
        try:
            return result.fetchone()
        except TypeError:
            return False


def create_admin(user_id, is_admin=True):
    # connection.ping()
    """Добавляем админа"""
    with engine.begin() as cursor:
        if check_admin(user_id):
            return 'Пользователь уже создан'
        cursor.execute(text(
            f"INSERT INTO admin (user_id, is_admin) VALUES ({user_id}, {is_admin});"
        ))


# create_admin(772658015)
# create_admin(1938610442)509967959
# create_admin(1742767208)
# create_admin(924068499)


def delete_admin(user_id):
    # connection.ping()
    """Удаляем админа"""
    with engine.begin() as cursor:
        cursor.execute(text(
            f"DELETE FROM admin WHERE user_id={user_id};"
        ))


def update_staff(user_id, is_admin):
    # connection.ping()
    """Обновляем статус админа"""
    with engine.begin() as cursor:
        cursor.execute(text(
            f'UPDATE "admin" SET is_admin = {is_admin} WHERE user_id = {user_id};'
        ))


def upload_table(url):
    # connection.ping()
    """Добавляем таблицу в бд"""
    with engine.begin() as cursor:
        dataframe = pandas.read_excel(url, header=None)
        dataframe.columns = ["number", "date", "code", "trek",
                             "weight", "price", "consumption", "sum", "status", ]
        dataframe.to_sql("product", cursor, if_exists="replace")
        dataframe.to_sql("product", cursor, if_exists="replace")


def gx_search_sql(gx):
    """Выполняем поиск по автокоду"""
    with engine.begin() as cursor:
        result = cursor.execute(
            text(f"SELECT * FROM product WHERE code='{gx}'"))
        return result.fetchall()


def trek_search_sql(trek):
    """Выполняем поиск по трек-номеру"""
    with engine.begin() as cursor:
        result = cursor.execute(
            text(f"SELECT * FROM product WHERE trek='{trek}'"))
        return result.fetchall()



# import json
# # Open JSON data
# with open("data.json") as f:
#     data = json.load(f)


# with engine.begin() as cursor:
#     for el in data:
#         # try:
#         if el['GX'] is None:
#             cursor.execute(text(
#                 f"INSERT INTO users (user_id, gx, status, lan) VALUES ({el['user_id']}, '{el['GX']}', {bool(el['status'])}, {el['lan']});"
#             ))
#         else:
#             cursor.execute(text(
#                 f"INSERT INTO users (user_id, status, lan) VALUES ({el['user_id']}, {bool(el['status'])}, '{el['lan']}');"
#             ))
#         # except sqlalchemy.exc.IntegrityError:
#         #     pass