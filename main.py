import io
import os
import urllib.parse
import time

from flask_wtf import Form, RecaptchaField
from wtforms import StringField, HiddenField
from flask import Flask, request, make_response, render_template
from waitress import serve

from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ['APP_SECRET_KEY']
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = os.environ['RECAPTCHA_PUBLIC_KEY']
app.config['RECAPTCHA_PRIVATE_KEY'] = os.environ['RECAPTCHA_PRIVATE_KEY']

table_service = TableService(
	account_name = os.environ['STORAGE_ACCOUNT_NAME'],
	account_key = os.environ['STORAGE_ACCOUNT_KEY']
)

table_name = os.environ['TABLE_NAME']

class CaptchaForm(Form):
    slug_field = HiddenField('slug')
    buildid_field = HiddenField('buildid')
    value_field = HiddenField('value')
    recaptcha = RecaptchaField()

@app.route('/<string:user>/<string:repo>/<string:buildid>/<int:value>', methods=['GET'])
def handle_get(user, repo, buildid, value):
    slug = f'{user}-{repo}'

    form = CaptchaForm(
        slug_field = slug,
        buildid_field = buildid,
        value_field = value
        )

    return render_template("captcha_form.html", form=form)



@app.route('/submit', methods=['POST'])
def handle_post():
    rowkey = f'{request.form["buildid_field"]}-{int(time.time())}'
    data = {'PartitionKey': request.form["slug_field"], 'RowKey': rowkey, 'value': int(request.form["value_field"])}
    print(f'inserting {data} into table...')
    table_service.insert_or_replace_entity(table_name, data)
    response = make_response("The R-Hero team thanks you for your feedback!", 200)
    return response

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=os.environ['PORT'])
