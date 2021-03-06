from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin
import os
import psycopg2
import psycopg2.pool
import sys

minConnections = 1
maxConnections = 20

app = Flask(__name__)
# CORS(app, support_credentials=True)
CORS(app, methods=['POST','GET','PUT','DELETE'])
# cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)


#REVIEW - these two different ways of connecting to the database are platform dependent which is doesnt make sense.
# macos (presumed *nix) uses localhost, windows uses docker ip address
try:
    pool = psycopg2.pool.ThreadedConnectionPool(minConnections, maxConnections, 
            host="172.16.238.11",
            database="data",
            user="docker",
            password="password")
except:
    print("Unable to connect to database with 172.16.238.11 attempting to connect to localhost")
    try:
        pool = psycopg2.pool.ThreadedConnectionPool(minConnections, maxConnections, 
            host="0.0.0.0",
            database="data",
            user="docker",
            password="password")
    except:
        print("Unable to connect to database with 0.0.0.0")
        sys.exit(1)

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

        res = {}
        for r in range(len(rows)):
            res[r] = {
                "id": rows[r][0],
                "title": rows[r][1],
                "done": rows[r][2]
            }

        return res

    def post(self): # create a new todo
        conn = pool.getconn()
        cur = conn.cursor()

        
        # try:
        #     title = request.form['title']
        #     app.logger.info(request.form['title']) # this only works if the data has been submitted as form data python does this but js doesnt

        # finally:
        #     title = request.get_json()["title"]
        #     app.logger.info(request.get_json()["title"]) # this only works if the data has been submitted normally as json data python doesn't do this in the configuration in testing.py


        title = request.get_json()["title"]

        cur.execute("INSERT INTO todo (task, done) VALUES (%s, %s)", (title, False))
        conn.commit()
        
        
        cur.close()
        pool.putconn(conn)


        return 200

    def put(self): # update a todo
        conn = pool.getconn()
        cur = conn.cursor()

        cur.execute("UPDATE todo SET task = %s, done = %s WHERE id = %s", (request.get_json()['title'], request.get_json()['done'], request.get_json()['id']))
        conn.commit()

        cur.close()
        pool.putconn(conn)

        return 200

    def delete(self): # delete a todo
        conn = pool.getconn()
        cur = conn.cursor()

        # app.logger.info(request.get_json()["id"])

        # app.logger.info("delete request received")
        # app.logger.info(request.get_json())

        cur.execute("DELETE FROM todo WHERE id = %s", (request.get_json()['id'],))
        conn.commit()

        cur.close()
        pool.putconn(conn)

        return 200
    
    def options(self):
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

# @cross_origin(supports_credentials=True) # allows cross origin requests from the front end (browser) to the api (server) 
@app.route('/')
def hello():
    return 'Go to todo/ to see methods'

# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response


if __name__ == '__main__':
    try:
        port = os.environ['PORT']
    except KeyError as e:
        port = 8000

    buildDatabase()

    # api.add_resource(Todo, '/todo')
    api.add_resource(Todo, '/todo/')

    app.run(debug = True, host='0.0.0.0', port=port)
    # app.run(debug = False, host='0.0.0.0', port=port)


