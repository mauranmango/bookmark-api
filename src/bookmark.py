# do percaktojme blueprint per bookmarks
from flask import Blueprint, request
from flask.json import jsonify
import validators
from flask_jwt_extended import current_user, get_jwt_identity, jwt_required
from src.database import Bookmark, db
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK


bookmark = Blueprint('bookmark', __name__, url_prefix='/api/v1/bookmarks')


# view function qe shton dhe kthen listen e bookmark-eve (CREATE READ)
@bookmark.route('/', methods=['POST', 'GET'])
@jwt_required()
def bookmarks():
    current_user = get_jwt_identity()      # na jep id e userit te loguar

    if request.method == 'POST':
        body = request.get_json().get('body', "")
        url = request.get_json().get('url', "")

        # Do kontrollojme nqs url eshte e rregullt dhe nuk ekziston ne databaze. Atehere do e shtojme ne db
        if validators.url(url):
            return jsonify({
                "error": "Enter a valid url"
            }), HTTP_400_BAD_REQUEST

        if Bookmark.query.filter_by(url=url).first():
            return jsonify({
                "error": "URL already exists"
            }), HTTP_409_CONFLICT

        bookmark = Bookmark(url=url, body=body, user_id=current_user, short_url=Bookmark.generate_short_characters)
        db.session.add(bookmark)
        db.session.commit()

        return jsonify({
            "bookmark":
                {
                    "id": bookmark.id,
                    "url": bookmark.url,
                    "short_url": bookmark.short_url,
                    "visits": bookmark.visits,
                    "body": bookmark.body,
                    "created_at": bookmark.created_at,
                    "updated_at": bookmark.update_at
                }
        }), HTTP_201_CREATED

    else:          # nqs nuk rregjistrohet do na ktheje te gjithe bookmarks qe kemi

        # marrim te gjithe bookmarket e userit te loguar
        bookmarks = Bookmark.query.filter_by(user_id=current_user)
        data = []

        for bookmark in bookmarks:
            data.append({
                "id": bookmark.id,
                "url": bookmark.url,
                "short_url": bookmark.short_url,
                "visits": bookmark.visits,
                "body": bookmark.body,
                "created_at": bookmark.created_at,
                "updated_at": bookmark.update_at
            })

        return jsonify({"data": data}), HTTP_200_OK

