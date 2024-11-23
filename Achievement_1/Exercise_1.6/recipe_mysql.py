import mysql.connector


conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    passwd='password')

cursor = conn.connect()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

cursor.execute("USE task_database")

cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS recipes (
        id INT NOT NULL  PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(50),
        ingredients VARCHAR(255),
        cooking_time INT,
        difficulty VARCHAR(20)
    )
    '''
)

def create_recipe(conn, cursor):


def search_recipe(conn, cursor):


def update_recipe(conn, cursor):


def delete_recipe(conn, cursor):


def main_menu(conn, cursor):
    
    