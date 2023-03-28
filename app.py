from flask import Flask, request, jsonify
import attendance_api
import aiohttp

app = Flask(__name__)

@app.route("/personal/username=<username>_and_password=<password>")
async def handlePersonalData(username, password):
    # check the validity of the username and password
    print(username, password)
    if(len(username) != 12):
        return jsonify({"error": "Invalid username"})
    if(len(password) != 10):
        return jsonify({"error": "Invalid password"})
    try:
        _, personal_info = await attendance_api.get_data(username, password)
        return jsonify(personal_info)
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid USN or DOB"})

@app.route("/attendance/username=<username>_and_password=<password>")
async def handleAttendanceData(username, password):
    print(type(username), type(password))
    # check the validity of the username and password
    if(len(username) != 12):
        return jsonify({"error": "Invalid username"})
    if(len(password) != 10):
        return jsonify({"error": "Invalid password"})
    try:
        attendance_info, _ = await attendance_api.get_data(username, password)
        return jsonify(attendance_info)
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid USN or DOB"})
    
if __name__ == "__main__":
    app.run()
