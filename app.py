

from flask import Flask, request, json, jsonify
import psycopg2

app = Flask(__name__)


@app.route("/")
def index():
    return "hello  how are you today "

def connection():
    db = psycopg2.connect(database="emma", user="postgres", password="password", host="localhost", port=5432)
    return db

@app.route("/create-user", methods=["POST"])
def create():
    con = connection()
    cursor = con.cursor()


    first_name = request.json["firstName"]
    last_name = request.json["lastName"]
    email = request.json["email"]
    password = request.json["password"]

    query = """
        INSERT INTO users(firstname, lastname, email, password)VALUES(%s, %s, %s, %s)
    """

    data = (first_name, last_name, email, password)

    cursor.execute(query, data)
    con.commit()

    return "user created successfully"


@app.route('/get-users', methods=["GET"])
def getUsers():
    con = connection()
    cursor = con.cursor()

    query = "SELECT * FROM users"

    cursor.execute(query)
    rows = cursor.fetchall()
    print(rows)


    user = []

    for row in rows:
        userData = {
            "firstName": row[1],
            "lastName": row[2],
            "email": row[3],
            "password": row[4]
        }

        user.append(userData)
        

    return jsonify(user)


@app.route('/update-user/<int:id>', methods=["PUT"])
def updateUser(id):
    con = connection()
    cursor = con.cursor()

    first_name = request.json["firstName"]
    last_name = request.json["lastName"]
    email = request.json["email"]
    password = request.json["password"]

    query = """
        UPDATE users SET firstname = %s, 
                        lastname = %s,
                        email = %s,
                        password = %s WHERE user_id = %s    """

    bind = (first_name, last_name, email, password, id)

    cursor.execute(query, bind)
    con.commit()
    
    return {"response": "user updated successfully"}


@app.route('/delete-user/<int:id>', methods=["DELETE"])
def deleteUser(id):
    con = connection()
    cursor = con.cursor()

    query = "DELETE FROM users WHERE user_id = %s"
    bind = (id,)

    cursor.execute(query, bind)
    con. commit()


    return {"response": "user deleted successfully!!"}





if __name__ == "__main__":
    app.run(debug=True)
