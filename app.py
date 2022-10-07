from flask import Flask, render_template, request,redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, jsonify, request, abort
import os
app = Flask(__name__)

credential = ServiceAccountCredentials.from_json_keyfile_name("credentials.json",
                                                              ["https://spreadsheets.google.com/feeds",                                                               "https://www.googleapis.com/auth/spreadsheets",                                                        "https://www.googleapis.com/auth/drive.file",                                                        "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(credential)

gsheet = client.open("Police info").sheet1

@app.route('/all_reviews', methods=["GET"])
def all_reviews():
    return jsonify(gsheet.get_all_records())

@app.route('/add_review', methods=["GET", "POST"])
def add_review():
    if request.method == "POST":
        data = request.get_json()
        gsheet.append_row(list(data.values()))
        return render_template('index.html')
    elif request.method == "GET":
        data = request.args
        gsheet.append_row(list(data.values()))
        return redirect('https://viveks-codes.github.io/Pratipushti/vishal/index.html',code=302)
        return jsonify({"success": False, "error": "Invalid request method"})

# @app.route('/del_review/<email>', methods=["DELETE"])
# def del_review(email):
#     cells = gsheet.findall(str(email))
#     for c in cells:
#         gsheet.delete_row(c.row)
#     return jsonify(gsheet.get_all_records())


# @app.route('/update_review', methods=["PATCH"])
# def update_review():
#     req = request.get_json()
#     cells = gsheet.findall(req["email"])
#     for c in cells:
#         gsheet.update_cell(c.row, 3, req["score"])
#     return jsonify(gsheet.get_all_records())
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=os.environ.get('PORT', 80))

# http://192.168.200.186/add_review?District=Surat&Taluka=mahuva&District=anawal&subdiv=Sub%20div-1&Polics-station=police%20chawki-3surat&How%20did%20you%20come%20to%20police%20station?=idontknow&After%20how%20much%20time%20you%20were%20heard%20in%20police%20station?=i%20dkkkkkk&Describe%20your%20expiriance%20with%20police%20in%20police%20station=idkif%20this%20works&
