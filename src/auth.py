# dhe blueprint per users
import validators
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_refresh_token, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED,\
    HTTP_401_UNAUTHORIZED, HTTP_200_OK
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


@auth.route('/login', methods=['POST'])
def login():
    # email eshte key keshtu qe nqs nuk kthen gje atehere merr default hapesire
    email = request.json.get('email', ' ')
    password = request.json.get('password', ' ')

    # do shohim nqs email ekziston dhe password eshte i sakte

    user = User.query.filter_by(email=email).first()

    # nqs useri ekziston dhe passwordi eshte i njejte do krijojme token
    if user and check_password_hash(user.password, password):
        refresh = create_refresh_token(identity=user.id)
        access = create_access_token(identity=user.id)

        return jsonify({
            "user": {
                "refresh": refresh,
                "access": access,
                "username": user.username,
                "email": user.email
            }
        }), HTTP_200_OK

    # nqs username apo password nuk eshte i sakte atehere do ktheje json me error
    return jsonify({"error": "wrong credentials"}), HTTP_401_UNAUTHORIZED


# nje funksion qe kthen userin e loguar
@auth.route('/me', methods=['GET'])
def me():
    return {'user': 'me'}
