from flask import Flask, jsonify

app = Flask(__name__)
app_dict = {"precipitation", "stations", "tobs", "<start>", "<start>/<end>"}

@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

if __name__ == '__main__':
    app.run(debug=True)
   