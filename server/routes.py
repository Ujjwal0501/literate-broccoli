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


@server.route('/', methods=['GET'])
def render_home():
    route_list = [{"name": "Barcode Generator", "path": "barcode"}, {"name": "Qrcode Generator", "path": "qrcode"}, {"name": "SKU Auto Generator", "path": "sku-generator"}, {"name": "Customized SKU Generator", "path": "customized-sku-generator"}, {"name": "VCard Generator", "path": "vcard-generator"}]
    return render_template('home.html', route_list=route_list), 200 


@server.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@server.route('/create-barcode', methods=['GET'])
def barcode_page():
    handle_visit(session)
    return render_template('barcode.html'), 200     


@server.route('/create-qrcode', methods=['GET'])
def qrcode_page():
    handle_visit(session)
    return render_template('qrcode.html'), 200     


@server.route('/sku-generator', methods=['GET'])
def sku_page():
    return render_template('skuauto.html'), 200     


@server.route('/customized-sku-generator', methods=['GET'])
def custom_sku_page():
    return render_template('skucustomized.html'), 200     


@server.route('/vcard-generator', methods=['GET'])
def vcard_page():
    return render_template('vcardgenerator.html'), 200     


if __name__ == '__main__':
    server.run(port=PORT)