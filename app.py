from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Informations de connexion à PostgreSQL
HOST = "postgresql-rospars.alwaysdata.net"
DATABASE = "rospars_yann"       
USER = "rospars"       
PASSWORD = "alwaysdataTaatbbtcct38%" 

# Fonction de connexion à la base de données
def get_db_connection():
    conn = psycopg2.connect(
        host=HOST,
        database=DATABASE,
        user=USER,
        password=PASSWORD
    )
    return conn

# Route pour récupérer le film Fight Club
@app.route('/get_fight_club', methods=['GET'])
def get_fight_club():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Recherche du film "Fight Club"
        query = "SELECT id, title, runtime FROM movies WHERE title = %s;"
        cursor.execute(query, ('Fight Club',))
        film = cursor.fetchone()

        if not film:
            return jsonify({"message": "Film not found"}), 404

        # Construction de la réponse avec ID, titre et runtime
        film_data = {
            "id": film[0],
            "title": film[1],
            "runtime": film[2]
        }
        return jsonify(film_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Route pour la racine (Home page)
@app.route('/')
def home():
    return "API de recommandation de films fonctionne ! 🎬"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
