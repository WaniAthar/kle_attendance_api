from flask import Flask, request, jsonify
import attendance_api
import aiohttp

app = Flask(__name__)

personal_info = None
attendance_info = None

@app.route("/personal/username=<username>_and_password=<password>")
async def handlePersonalData(username, password):
    global personal_info
    global attendance_info
    # check the validity of the username and password
    print(username, password)
    if len(username) != 12:
        return jsonify({"error": "Invalid username"})
    if len(password) != 10:
        return jsonify({"error": "Invalid password"})
    try:
        if personal_info is not None and attendance_info is not None:
            return jsonify(personal_info)
        attendance_info, personal_info = await attendance_api.get_data(username, password)
        return jsonify(personal_info)
    except Exception as e:
        print(e)
        if personal_info is None or attendance_info is None:
            return jsonify({"error": "Invalid USN or DOB"})
        else:
            return jsonify(personal_info)

@app.route("/attendance/username=<username>_and_password=<password>")
async def handleAttendanceData(username, password):
    global attendance_info
    global personal_info
    # check the validity of the username and password
    if len(username) != 12:
        return jsonify({"error": "Invalid username"})
    if len(password) != 10:
        return jsonify({"error": "Invalid password"})
    try:
        if personal_info is not None and attendance_info is not None:
            return jsonify(attendance_info)
        attendance_info, personal_info = await attendance_api.get_data(username, password)
        return jsonify(attendance_info)
    except Exception as e:
        print(e)
        if personal_info is None or attendance_info is None:
            return jsonify({"error": "Invalid USN or DOB"})
        else:
            return jsonify(attendance_info)
    
if __name__ == "__main__":
    app.run()
