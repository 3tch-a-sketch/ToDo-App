from flask import Flask, request
from flask_restful import Api, Resource
import os
import psycopg2
import psycopg2.pool
import sys


minConnections = 1
maxConnections = 20

app = Flask(__name__)
api = Api(app)

pool = psycopg2.pool.ThreadedConnectionPool(minConnections, maxConnections, 
        host="172.16.238.11",
        database="data",
        user="docker",
        password="password")

if pool:
    print("Connection pool created")
else:
    sys.exit("Connection pool not created")

class Todo(Resource):
    def get(self): # return all todos
        conn = pool.getconn()
        cur = conn.cursor()

        cur.execute("SELECT * FROM todo")
        rows = cur.fetchall()

        cur.close()
        pool.putconn(conn)

        dic = {}
        for r in range(len(rows)):
            dic[r] = {
                "id": rows[r][0],
                "title": rows[r][1],
                "done": rows[r][2]
            }

        return dic

    def post(self): # create a new todo
        conn = pool.getconn()
        cur = conn.cursor()

        cur.execute("INSERT INTO todo (task, done) VALUES (%s, %s)", (request.form['title'], False))
        conn.commit()

        cur.close()
        pool.putconn(conn)
        return 200

    def put(self): # update a todo

        conn = pool.getconn()
        cur = conn.cursor()

        cur.execute("UPDATE todo SET task = %s, done = %s WHERE id = %s", (request.form['title'], request.form['done'], request.form['id']))
        conn.commit()

        cur.close()
        pool.putconn(conn)

        return 200

    def delete(self): # delete a todo
        conn = pool.getconn()
        cur = conn.cursor()

        cur.execute("DELETE FROM todo WHERE id = %s", (request.form['id'],))
        conn.commit()

        cur.close()
        pool.putconn(conn)

        return 200
    


def buildDatabase():
    conn = pool.getconn()
    cursor = conn.cursor()
    cursor.execute("""SELECT EXISTS (
    SELECT FROM information_schema.tables 
    WHERE  table_schema = 'public'
    AND    table_name   = 'todo'
    )""")
    exists = cursor.fetchall()
    # print(exists[0][0])

    if not exists[0][0]:
        cursor.execute("""CREATE TABLE todo (
            id serial PRIMARY KEY,
            task text NOT NULL,
            done boolean NOT NULL
        )""")
        conn.commit()
        print("Table created")

    cursor.close()
    pool.putconn(conn)

@app.route('/')
def hello():
    return 'Hello, World!'


if __name__ == '__main__':
    try:
        port = os.environ['PORT']
    except KeyError as e:
        port = 8000

    buildDatabase()

    # api.add_resource(Todo, '/todo')
    api.add_resource(Todo, '/todo/')

    app.run(debug = True, host='0.0.0.0', port=port)

