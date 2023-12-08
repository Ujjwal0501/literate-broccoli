
from models import Task
from activity import validate_query_src, handle_output_req

from flask import request, send_file, Blueprint, session
from config import MAX_REQUEST_SIZE
import csv, io, json


api = Blueprint("api", __name__)


@api.route('/csv-to-barcode', methods=['POST'])
def upload_file():
    user = validate_query_src(request.args)
    if not user or user.quota_left < 1:
        return 'Unauthorized', 403

    if 'file' not in request.files:
        return 'No file part in the request', 400

    file = request.files['file']
    if file.filename == '' or not file:
        return 'No file selected for uploading', 400

    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    data = list(csv.reader(stream))
    data = [item for sublist in data for item in sublist]
    if len(data) > MAX_REQUEST_SIZE:
        return f'Entry limit exceeded. Maximum entry allowed is {MAX_REQUEST_SIZE}', 400
    task = Task.create(session = user.session_id, entry_count = len(data), data_entries = ','.join(data))
    user.update(quota_left=user.quota_left-1).execute()

    return json.dumps({'status': "OK", 'quota': user.quota_left-1}), 200


@api.route('/csv-to-barcode', methods=['GET'])
def download_barcode():
    user = validate_query_src(request.args)
    if not user or user.quota_left < 1:
        return 'Unauthorized', 403

    task = Task.get_or_none(session=user.session_id)
    if not task:
        return 'No task received', 400

    if task.status == Task.STATUS_IN_QUEUE or task.status == Task.STATUS_PROCESSING:
        task.update(status = Task.STATUS_PROCESSING).execute()
        print(task.status)
        # req_pool.map_async(handle_output_req, (task,))
        handle_output_req.delay(task.session, task.data_entries)
        return "", 204

    if task.status == Task.STATUS_PROCESSING:
        return 'Processing', 206

    if task.status == Task.STATUS_COMPLETED:
        zip_ = io.BytesIO(task.svg_output)
        return send_file(zip_, mimetype='application/zip', as_attachment=True, download_name='content.zip')
    else:
        return "Fail", 400
