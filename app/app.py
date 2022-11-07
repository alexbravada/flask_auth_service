from flask import Flask
from flask_jwt_extended import JWTManager

from api import api_blueprint


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'changeme'
#SECRET_KEY = 'changeme'
jwt = JWTManager(app)

# 'FLASK_APP=wsgi_app flask run --with-threads --reload'


app.register_blueprint(api_blueprint)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8005,
        debug=True
    )
