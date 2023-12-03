from flask import Flask, jsonify, request, abort
from flask_caching import Cache
import attendance_api

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

def make_cache_key(route_name, username, password):
    return f"{route_name}:{username}:{password}"

@app.route("/api/student_data", methods=['POST'])
def getStudentData():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    route_name = request.endpoint.split('.')[-1]
    cache_key = make_cache_key(route_name, username, password)
    student_data = cache.get(cache_key)
    if student_data is not None:
        return jsonify(student_data)

    if len(username) != 12 or len(password) != 10:
        return jsonify({"error": "Invalid username or password"}), 400

    try:
        student_data = attendance_api.fetch_student_data(username, password)
        cache.set(cache_key, student_data, timeout=300)
        return jsonify(student_data)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500 

@app.route("/api/coe", methods=['POST'])
def handleCoe():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    route_name = request.endpoint.split('.')[-1]
    cache_key = make_cache_key(route_name, username, password)
    coe_data = cache.get(cache_key)
    if coe_data is not None:
        return jsonify(coe_data)

    if len(username) != 12 or len(password) != 10:
        return jsonify({"error": "Invalid username or password"}), 400

    try:
        coe = attendance_api.fetch_calendar_of_events(username, password)
        cache.set(cache_key, coe['coe'], timeout=300)
        return jsonify(coe['coe'])
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid USN or DOB"}), 500

if __name__ == "__main__":
    app.run()
