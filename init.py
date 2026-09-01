from flask import Flask

from app.helpers.config import Config
from routes.Router import Router

config = Config()
app = Flask(__name__)
app.config["DEBUG"] = config.flask_debug

with app.app_context():
    router = Router()
    router.init_app_routes()

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], host="0.0.0.0", port=config.app_port)
