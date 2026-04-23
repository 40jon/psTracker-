from flask import Flask
from flask_cors import CORS
from routes.main_routes import main_bp

app = Flask(__name__)
app.secret_key = "opstracker-secret-key"

CORS(app)

app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
