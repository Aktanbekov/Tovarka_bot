# from config import load_config
# import pymysql
# from pymysql import cursors
# import pandas
# from sqlalchemy import create_engine, text
# import sqlalchemy


# # Подключаемся к MySql
# connection = pymysql.connect(
#     host=load_config().get('host'),
#     user=load_config().get('user'),
#     password=load_config().get('password'),
#     database=load_config().get('db_name'),
#     cursorclass=cursors.DictCursor,
#     autocommit=True,
# )

# url_object = sqlalchemy.engine.url.URL(
#     "mysql+pymysql",
#     username=load_config().get('user'),
#     password=load_config().get('password'),
#     host=load_config().get('host'),
#     database=load_config().get('db_name',)
# )

# engine = create_engine(url_object)
# # with connection.cursor() as cursor:
# #     cursor.execute(
# #         """
# #         CREATE TABLE `users`(
# #         id int AUTO_INCREMENT,
# #         user_id int NOT NULL,
# #         GX varchar(8) NOT NULL,
# #         status boolean NOT NULL,
# #         lan varchar(15) NOT NULL,
# #         PRIMARY KEY(id)
# #         );
# #         """
# #     )

# # with connection.cursor() as cursor:
# #     cursor.execute(
# #         """
# #         CREATE TABLE `admin`(
# #         id int AUTO_INCREMENT,
# #         user_id integer NOT NULL UNIQUE,
# #         is_admin boolean NOT NULL,
# #         PRIMARY KEY(id)
# #         );
# #         """
# #     )

# # with engine.begin() as cursor:
# #     cursor.execute(text(
# #         """
# #         CREATE TABLE `product`(
# #         id int AUTO_INCREMENT,
# #         number text,
# #         date text,
# #         trek text,
# #         weight text,
# #         price text,
# #         consumption text,
# #         sum text,
# #         status text,
# #         auto text,
# #         PRIMARY KEY(id)
# #         );
# #         """
# #     ))


# def get_subscriptions(status=True):
#     connection.ping()
#     with connection.cursor() as cursor:
#         cursor.execute(
#             f"SELECT * FROM `users` WHERE status={status};"
#         )
#         return cursor.fetchall()


# def get_by_gx(gx):
#     connection.ping()
#     with connection.cursor() as cursor:
#         cursor.execute(
#             f"SELECT * FROM `users` WHERE gx='{gx}';"
#         )
#         return cursor.fetchall()


# def user_exists(user_id, gx):
#     connection.ping()
#     """Проверяем существует ли пользователь"""
#     with connection.cursor() as cursor:
#         cursor.execute(
#             f"SELECT * FROM `users` WHERE user_id={user_id} AND gx='{gx}';"
#         )
#         try:
#             cursor.fetchall()[0]
#             return True
#         except IndexError:
#             return False


# def subscriber_status(user_id):
#     connection.ping()
#     """Проверяем активен ли пользователь"""
#     with connection.cursor() as cursor:
#         cursor.execute(
#             f"SELECT status FROM `users` WHERE user_id={user_id};"
#         )
#         return cursor.fetchone().get('status')


# def add_subscriber(user_id, gx, status=True):
#     connection.ping()
#     """Добавляем пользователя"""
#     with connection.cursor() as cursor:
#         cursor.execute(
#             f"UPDATE `users` SET gx = '{gx}', status = {status} WHERE user_id = {user_id};"
#         )


# def update_subscription(user_id, status):
#     connection.ping()
#     """Обновляем статус подписки"""
#     with connection.cursor() as cursor:
#         cursor.execute(
#             f"UPDATE `users` SET status = {status} WHERE user_id = {user_id}"
#         )


# def get_lan(user_id):
#     connection.ping()
#     """Получаем язык"""
#     with connection.cursor() as cursor:
#         cursor.execute(
#             f"SELECT lan FROM `users` WHERE user_id = {user_id};"
#         )
#         try:
#             return cursor.fetchone().get('lan')
#         except Exception:
#             return False


# def add_lan(user_id, lan):
#     connection.ping()
#     """Добавляем язык"""
#     with connection.cursor() as cursor:
#         cursor.execute(
#             f"INSERT INTO `users` (user_id, lan) VALUES ({user_id}, '{lan}')"
#         )


# def update_lan(user_id, lan):
#     connection.ping()
#     """Обновляем язык"""
#     with connection.cursor() as cursor:
#         cursor.execute(
#             f"UPDATE `users` SET lan = '{lan}' WHERE user_id = {user_id}"
#         )


# def check_admin(user_id):
#     connection.ping()
#     """Проверяем на права админа"""
#     with connection.cursor() as cursor:
#         cursor.execute(
#             f"SELECT is_admin FROM `admin` WHERE user_id={user_id};"
#         )
#         try:
#             return cursor.fetchone()
#         except TypeError:
#             return False


# def create_admin(user_id, is_admin=True):
#     connection.ping()
#     """Добавляем админа"""
#     with connection.cursor() as cursor:
#         if check_admin(user_id):
#             return 'Пользователь уже создан'
#         cursor.execute(
#             f"INSERT INTO `admin` (user_id, is_admin) VALUES ({user_id}, {is_admin});"
#         )


# # create_admin(772658015)


# def delete_admin(user_id):
#     connection.ping()
#     """Удаляем админа"""
#     with connection.cursor() as cursor:
#         cursor.execute(
#             f"DELETE FROM `admin` WHERE user_id={user_id};"
#         )


# def update_staff(user_id, is_admin):
#     connection.ping()
#     """Обновляем статус админа"""
#     with connection.cursor() as cursor:
#         cursor.execute(
#             f"UPDATE `admin` SET is_admin = {is_admin} WHERE user_id = {user_id};"
#         )


# def upload_table(url):
#     # connection.ping()
#     """Добавляем таблицу в бд"""
#     with engine.begin() as cursor:
#         dataframe = pandas.read_excel(url, header=None)
#         dataframe.columns = ['number', 'date', 'code', 'trek',
#                              'weight', 'price', 'consumption', 'sum', 'status', ]
#         dataframe.to_sql('product', cursor, if_exists='replace')
#         dataframe.to_sql('product', cursor, if_exists='replace')


# def gx_search_sql(gx):
#     """Выполняем поиск по автокоду"""
#     with engine.begin() as cursor:
#         result = cursor.execute(
#             text(f"SELECT * FROM `product` WHERE auto='{gx}'"))
#         return result.fetchall()


# def trek_search_sql(trek):
#     """Выполняем поиск по трек-номеру"""
#     with engine.begin() as cursor:
#         result = cursor.execute(
#             text(f"SELECT * FROM `product` WHERE trek='{trek}'"))
#         return result.fetchall()
