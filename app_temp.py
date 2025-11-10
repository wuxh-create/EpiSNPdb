from flask import Flask
from flask_pymongo import PyMongo
from flask_restful import Api
from configs import current_config

mongo = PyMongo()
app = Flask(
        __name__,
        template_folder = "templates",
        static_folder   = "static",
        static_url_path = '/EpiSNPdb'
    )
api = Api(app)
app.config.from_object(current_config.get("development"))

# app.config.from_object(current_config.get("development"))

# production

mongo.init_app(app)

from flask import Blueprint
from flask import render_template

views = Blueprint(
    "view", __name__,
    template_folder = "templates",
    static_folder   = "static",
    static_url_path = "/"
)

@views.route("/")
def index():
    return render_template("index.html")

@views.app_errorhandler(500)
def handle_505(e):
    return render_template("505.html")

#import ajax

app.register_blueprint(views, url_prefix = "/")

if __name__ == '__main__':
    app.run(port = 7000,host="0.0.0.0")
