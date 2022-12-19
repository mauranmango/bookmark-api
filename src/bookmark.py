# do percaktojme blueprint per bookmarks
from flask import Blueprint


bookmark = Blueprint('bookmark', __name__, url_prefix='/api/v1/bookmarks')

# view function qe kthen listen e  bookmark-eve
@bookmark.route('/', methods=['GET'])
def get_all():
    return {'bookmarks': []}
