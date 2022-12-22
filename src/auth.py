# dhe blueprint per users
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import validators
from src.database import User, db

# duhet ti themi programit se nga duhet te ekzekutohet prandaj kalojme parametrin __name__
# gjithashtu mund te percaktojme prefiks per url
auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@auth.route('/register', methods=['POST'])
def register():
    # web applications frequently require processing incoming request data from users
    # na lejon aksesin e drejtperdrejte te atributeve merr vlerat qe i percaktojme te body
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
        return jsonify({'error': 'email is taken'}), HTTP_409_CONFLICT  # kur emaili ekziston kthen status code 409

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': 'username is taken'}), HTTP_409_CONFLICT

    # pasi kemi validuar parametrat e tjere hashojme dhe passwordin  dhe mund te krijojme userin
    pwd_hash = generate_password_hash(password)

    user = User(username=username, email=email, password=pwd_hash)  # pasi krijuam userin do e shtojme ne db
    db.session.add(user)
    db.session.commit()

    # e testojme ne postman me metoden POST dhe te Body (JSON) ne nje dictionary percaktojme username, email, password
    return jsonify({'message': 'User created',
                    'user': {
                        'username': username,
                        'email': email}}), HTTP_201_CREATED

    # Nqs do tentojme te krijojme te njejtin user do na shfaqi error {"error": "email is taken"}


# nje funksion qe kthen userin e loguar
@auth.route('/me', methods=['GET'])
def me():
    return {'user': 'me'}
