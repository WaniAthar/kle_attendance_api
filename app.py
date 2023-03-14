from flask import Flask, request, jsonify
import attendance_api

app = Flask(__name__)

@app.route("/personal/username=<username>_and_password=<password>")
def handlePersonalData(username, password):
    # check the validity of the username and password
    print(username, password)
    if(len(username) != 12):
        return jsonify({"error": "Invalid username"})
    if(len(password) != 10):
        return jsonify({"error": "Invalid password"})
    try:
        _, personal_info = attendance_api.get_data(username, password)
        return jsonify(personal_info)
    except:
        return jsonify({"error": "Invalid username or password"})

@app.route("/attendance/username=<username>_and_password=<password>")
def handleAttendanceData(username, password):
    print(type(username), type(password))
    # check the validity of the username and password
    if(len(username) != 12):
        return jsonify({"error": "Invalid username"})
    if(len(password) != 10):
        return jsonify({"error": "Invalid password"})
    try:
        attendance_info, _ = attendance_api.get_data(username, password)
        return attendance_info
    except:
        return jsonify({"error": "Invalid username or password"})
    
if __name__ == "__main__":
    app.run()