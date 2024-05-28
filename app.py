from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "538f310c13f64d31bed2a94d6fdc93c6"
API_BASE_URL = "https://api.football-data.org/v2"

headers = {"X-Auth-Token": API_KEY}

def obtener_equipos():
    url = f"{API_BASE_URL}/teams"
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else None

def obtener_info_equipo(equipo_id):
    url = f"{API_BASE_URL}/teams/{equipo_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        equipo = response.json()
        return equipo
    else:
        return None

def obtener_calendario(year):
    url = f"{API_BASE_URL}/competitions/PL/matches?season={year}"
    response = requests.get(url, headers=headers)
    return response.json()['matches'] if response.status_code == 200 else None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar_equipo', methods=['POST'])
def buscar_equipo():
    nombre_equipo = request.form['nombre_equipo']
    equipos = obtener_equipos()
    equipos_coincidentes = [equipo for equipo in equipos['teams'] if nombre_equipo.lower() in equipo['name'].lower()]
    if equipos_coincidentes:
        return render_template('resultados_busqueda.html', equipos=equipos_coincidentes)
    else:
        return render_template('index.html', error_equipo="No se encontraron equipos que coincidan con el nombre proporcionado")

@app.route('/equipos/<int:equipo_id>', methods=['GET'])
def detalle_equipo(equipo_id):
    equipo = obtener_info_equipo(equipo_id)
    return render_template('detalle_equipo.html', equipo=equipo)

@app.route('/mostrar_calendario', methods=['POST'])
def mostrar_calendario():
    year = request.form['year']
    calendario = obtener_calendario(year)
    if calendario:
        # Organizar los partidos por jornadas
        jornadas = {}
        for partido in calendario:
            jornada_numero = partido['matchday']
            if jornada_numero not in jornadas:
                jornadas[jornada_numero] = []
            jornadas[jornada_numero].append(partido)

        return render_template('resultados_calendario.html', calendario=jornadas)
    else:
        return render_template('index.html', error_calendario="No se encontró el calendario para el año especificado")


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run('0.0.0.0', port, debug=False)
