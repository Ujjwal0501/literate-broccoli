from models import Task, UserSession
from api import api
from activity import handle_visit

from flask import render_template, session
from app import server, db
from config import PORT


server.config.from_prefixed_env()
server.register_blueprint(api, url_prefix="/api")
db.create_tables([Task, UserSession], safe=True)

# fix test API
root_key, new = UserSession.get_or_create(session_id='13717e9b-5406-4839-a184-b2f3c9af4b25')
root_key.update(quota_left=4294967296).execute()


@server.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@server.route('/create-barcode', methods=['GET'])
def form_page():
    handle_visit(session)
    return render_template('form.html'), 200     


if __name__ == '__main__':
    server.run(port=PORT)