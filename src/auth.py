# dhe blueprint per users
from flask import Blueprint

# duhet ti themi programit se nga duhet te ekzekutohet prandaj kalojme parametrin __name__
# gjithashtu mund te percaktojme prefiks per url
auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth.route('/register', methods=['POST'])
def register():
    return "User created"


# nje funksion qe kthen userin e loguar
@auth.route('/me', methods=['GET'])
def me():
    return {'user': 'me'}