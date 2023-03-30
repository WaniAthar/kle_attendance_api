from flask import Flask, jsonify, request
from flask_caching import Cache
import attendance_api

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Add route_name as an argument to the make_cache_key function
def make_cache_key(route_name, username, password):
    return f"{route_name}:{username}:{password}"

@app.route("/personal/username=<username>_and_password=<password>")
async def handlePersonalData(username, password):
    # Get the name of the endpoint function
    route_name = request.endpoint.split('.')[-1]
    # Use the endpoint function name to generate a unique cache key
    cache_key = make_cache_key(route_name, username, password)
    # Get the cached personal data using the cache key
    personal_data = cache.get(cache_key)
    if personal_data is not None:
        return jsonify(personal_data)
    # If the personal data is not in the cache, fetch it from the API
    if (len(username) != 12):
        return jsonify({"error": "Invalid username"})
    if (len(password) != 10):
        return jsonify({"error": "Invalid password"})
    try:
        _, personal_info = await attendance_api.get_data(username, password)
        # Store the fetched personal data in the cache using the cache key
        cache.set(cache_key, personal_info, timeout=300)
        return jsonify(personal_info)
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid USN or DOB"})

@app.route("/attendance/username=<username>_and_password=<password>")
async def handleAttendanceData(username, password):
    # Get the name of the endpoint function
    route_name = request.endpoint.split('.')[-1]
    # Use the endpoint function name to generate a unique cache key
    cache_key = make_cache_key(route_name, username, password)
    # Get the cached attendance data using the cache key
    attendance_data = cache.get(cache_key)
    if attendance_data is not None:
        return jsonify(attendance_data)
    # If the attendance data is not in the cache, fetch it from the API
    if (len(username) != 12):
        return jsonify({"error": "Invalid username"})
    if (len(password) != 10):
        return jsonify({"error": "Invalid password"})
    try:
        attendance_info, _ = await attendance_api.get_data(username, password)
        # Store the fetched attendance data in the cache using the cache key
        cache.set(cache_key, attendance_info, timeout=300)
        return jsonify(attendance_info)
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid USN or DOB"})

if __name__ == "__main__":
    app.run()
