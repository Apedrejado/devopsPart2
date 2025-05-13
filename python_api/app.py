from flask import Flask, request, jsonify  
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route("/")
def hello():
    db = mysql.connector.connect(
        user=os.getenv("DB_USER"),
        host=os.getenv("DB_HOST"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    cursor = db.cursor()
    cursor.execute("SELECT NOW();")  
    result = cursor.fetchone()

    cursor.close()
    db.close()

    return f"Database Query Result: {result}"

@app.route("/user", methods=["POST"])  
def add_user():
    try:
        data = request.get_json()
        name = data.get("name")

        if not name:
            return jsonify({"error": "Nome precisa ser fornecido"}), 400 
        
        db = mysql.connector.connect(
            user=os.getenv("DB_USER"),
            host=os.getenv("DB_HOST"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        cursor = db.cursor()
        
        cursor.execute("INSERT INTO users (name) VALUES (%s)", (name,))
        db.commit()

        user_id = cursor.lastrowid

        cursor.close()
        db.close()

        return jsonify({"message": "User created", "user_id": user_id}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    

@app.route("/users", methods=["GET"])
def get_all_users():
    try:
        db = mysql.connector.connect(
            user=os.getenv("DB_USER"),
            host=os.getenv("DB_HOST"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        cursor = db.cursor(dictionary=True) 
        cursor.execute("SELECT * FROM users;")
        users = cursor.fetchall()

        cursor.close()
        db.close()

        return jsonify({"users": users}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route("/user/<int:id>", methods=["DELETE"])
def delete_user(id):
    try:
        db = mysql.connector.connect(
            user=os.getenv("DB_USER"),
            host=os.getenv("DB_HOST"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        cursor = db.cursor()

        cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
        user = cursor.fetchone()

        if user is None:
            cursor.close()
            db.close()
            return jsonify({"error": "User not found"}), 404

        cursor.execute("DELETE FROM users WHERE id = %s", (id,))
        db.commit()

        cursor.close()
        db.close()

        return jsonify({"message": f"User with id {id} deleted successfully"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route("/user/<int:id>", methods=["PUT"])
def update_user_name(id):
    try:
        data = request.get_json()  
        new_name = data.get("name")

        if not new_name:
            return jsonify({"error": "Name is required"}), 400

        db = mysql.connector.connect(
            user=os.getenv("DB_USER"),
            host=os.getenv("DB_HOST"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        cursor = db.cursor()

        cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
        user = cursor.fetchone()

        if user is None:
            cursor.close()
            db.close()
            return jsonify({"error": "User not found"}), 404

        cursor.execute("UPDATE users SET name = %s WHERE id = %s", (new_name, id))
        db.commit()

        cursor.close()
        db.close()

        return jsonify({"message": f"User with id {id} updated successfully"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)  
