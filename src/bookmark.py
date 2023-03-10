# do percaktojme blueprint per bookmarks
import validators
from flask import Blueprint, request
from flask.json import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK, \
    HTTP_404_NOT_FOUND, HTTP_302_FOUND, HTTP_204_NO_CONTENT
from src.database import Bookmark, db
from flasgger import swag_from

bookmark = Blueprint('bookmark', __name__, url_prefix='/api/v1/bookmarks')


# view function qe shton dhe kthen listen e bookmark-eve (CREATE READ) (C)
@bookmark.route('/', methods=['POST', 'GET'])
@jwt_required()
def create_and_show_all_bookmarks():
    current_user = get_jwt_identity()  # na jep id e userit te loguar

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

    # nqs nuk rregjistrohet do na ktheje te gjithe bookmarks qe kemi
    else:
        # per te aplikuar paginate na duhen dy gjera: 1. Faqja nga do marrim te dhenat, 2. per page count
        # page do ta kalojme si argument ne url psh: http://127.0.0.1:5000/api/v1/bookmarks/?page=2
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 1, type=int)

        # marrim te gjithe bookmarket e userit te loguar
        bookmarks = Bookmark.query.filter_by(user_id=current_user).paginate(page=page, per_page=per_page)

        data = []

        for bookmark in bookmarks.items:  # pagination  object is not iterable that's why bookmarks.items
            data.append({
                "id": bookmark.id,
                "url": bookmark.url,
                "short_url": bookmark.short_url,
                "visits": bookmark.visits,
                "body": bookmark.body,
                "created_at": bookmark.created_at,
                "updated_at": bookmark.update_at
            })

            meta = {
                "page": bookmarks.page,
                "pages": bookmarks.pages,
                "total_count": bookmarks.total,
                "prev_page": bookmarks.prev_num,
                "next_page:": bookmarks.next_num,
                "has_next": bookmarks.has_next,
                "has_prev": bookmarks.has_prev
            }

        return jsonify({"data": data, "meta": meta}), HTTP_200_OK


# Si te therrasim nje bookmark te caktuar duke u nisur nga id (R)
@bookmark.route("/<int:id>", methods=['GET'])
@jwt_required()
def get_bookmark(id):
    current_user = get_jwt_identity()

    # bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()
    # funksionon edhe keshtu
    bookmark = Bookmark.query.filter_by(id=id).first()

    if not bookmark:
        return jsonify({
            "message": "Item not found"
        }), HTTP_404_NOT_FOUND

    return jsonify({
        "id": bookmark.id,
        "url": bookmark.url,
        "short_url": bookmark.short_url,
        "visits": bookmark.visits,
        "body": bookmark.body,
        "created_at": bookmark.created_at,
        "updated_at": bookmark.update_at
    }), HTTP_302_FOUND


# Si te rifreskojme nje bookmark (U)
@bookmark.route('/<int:id>', methods=['PUT'])
@jwt_required()
def edit_bookmark(id):
    bookmark = Bookmark.query.filter_by(id=id).first()

    if not bookmark:
        return jsonify({
            "message": "Item not found"
        }), HTTP_404_NOT_FOUND

    body = request.get_json().get('body', "")
    url = request.get_json().get('url', "")

    if validators.url(url):
        return jsonify({
            "error": "Enter a valid url"
        }), HTTP_400_BAD_REQUEST

    bookmark.url = url
    bookmark.body = body
    db.session.commit()

    return jsonify({
        "id": bookmark.id,
        "url": bookmark.url,
        "short_url": bookmark.short_url,
        "visits": bookmark.visits,
        "body": bookmark.body,
        "created_at": bookmark.created_at,
        "updated_at": bookmark.update_at
    }), HTTP_200_OK


# Si te fshijme nje bookmark (D)
@bookmark.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_bookmark(id):
    bookmark = Bookmark.query.filter_by(id=id).first()

    if not bookmark:
        return jsonify({
            "message": "Item not found"
        }), HTTP_404_NOT_FOUND

    db.session.delete(bookmark)
    db.session.commit()

    # ose do kthejme objektin e fshire ose do kthejme no content
    # return jsonify({
    #     "deleted item": {
    #         "id": bookmark.id,
    #         "url": bookmark.url,
    #         "short_url": bookmark.short_url,
    #         "visits": bookmark.visits,
    #         "body": bookmark.body,
    #         "created_at": bookmark.created_at,
    #         "updated_at": bookmark.update_at
    #     }
    # })
    return jsonify({}), HTTP_204_NO_CONTENT


# Do merrim url dhe numrin e hereve qe eshte vizituar
@bookmark.route('/stats', methods=['GET'])
@jwt_required()
@swag_from("./docs/bookmark/stats.yaml")
def get_stats():
    current_user = get_jwt_identity()
    data = []

    items = Bookmark.query.filter_by(user_id=current_user).all()

    for item in items:
        new_link = {
            "url": item.url,
            "visits": item.visits,
            "short_url": item.short_url,
            "id": item.id
        }
        data.append(new_link)

    return jsonify({
        "data": data
    }), HTTP_200_OK