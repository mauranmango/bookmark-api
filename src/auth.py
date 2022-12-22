# dhe blueprint per users
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import validators
from src.database import User

# duhet ti themi programit se nga duhet te ekzekutohet prandaj kalojme parametrin __name__
# gjithashtu mund te percaktojme prefiks per url
auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    # bejme disa validations
    if len(password) < 6:
        # duhet te kthje tuple me rezultatin dhe status codin e requestit
        return jsonify({'error': 'password too short'}), HTTP_400_BAD_REQUEST

    if len(username) < 3:
        return jsonify({'error': 'username too short'}), HTTP_400_BAD_REQUEST

    if not username.isalnum() or " " in username:
        return jsonify({'error': 'username should be alphanumeric, also no spaces'}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error': 'email is not valid'}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': 'email is taken'}), HTTP_409_CONFLICT    # kur emaili ekziston kthen status code 409

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': 'username is taken'}), HTTP_409_CONFLICT


    return "User created"


# nje funksion qe kthen userin e loguar
@auth.route('/me', methods=['GET'])
def me():
    return {'user': 'me'}