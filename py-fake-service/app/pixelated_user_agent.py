from flask import Flask, request, Response, redirect

import json
import datetime
import requests
from adapter import MailService
from search import SearchQuery

app = Flask(__name__, static_url_path='', static_folder='../../web-ui/app')
client = None
converter = None
account = None
mail_service = MailService()

def respond_json(entity):
    response = json.dumps(entity)
    return Response(response=response, mimetype="application/json")


@app.route('/disabled_features')
def disabled_features():
        return respond_json([]) 


@app.route('/mails', methods=['POST'])
def save_draft_or_send():
    return respond_json({'ident': 123})


@app.route('/mails', methods=['PUT'])
def update_draft():
    return respond_json({'ident': 123})


@app.route('/mails')
def mails():
    query = SearchQuery.compile(request.args.get('q', ''))
    page = request.args.get('p', '') 
    window_size = request.args.get('w', '')
    fetched_mails = mail_service.mails(query, page, window_size)

    mails = [mail.__dict__ for mail in fetched_mails]
    response = {
        "stats": {
            "total": len(mails),
            "read": 0,
            "starred": 0,
            "replied": 0
        },
        "mails": mails
    }

    return respond_json(response)


@app.route('/mail/<int:mail_id>', methods=['DELETE'])
def delete_mails(mail_id):
    mail_service.delete_mail(mail_id)
    return respond_json(None)


@app.route('/tags')
def tags():
    tags = mail_service.tagsset.all_tags()
    return respond_json([tag.__dict__ for tag in tags])


@app.route('/mail/<int:mail_id>')
def mail(mail_id):
    return respond_json(mail_service.mail(mail_id).__dict__)


@app.route('/mail/<int:mail_id>/tags', methods=['POST'])
def mail_tags(mail_id):
    new_tags = request.json['newtags']
    mail_service.update_tags_for(mail_id, new_tags)
    return respond_json(request.json['newtags'])


@app.route('/mail/<int:mail_id>/read', methods=['POST'])
def mark_mail_as_read(mail_id):
    mail_service.mark_as_read(mail_id)
    return ""

@app.route('/contacts')
def contacts():
    contacts_query = request.args.get('q')
    return respond_json({'contacts': mail_service.search_contacts(contacts_query)})


@app.route('/draft_reply_for/<int:mail_id>')
def draft_reply_for(mail_id):
    return respond_json(None)


@app.route('/control/mailset/<mailset>/load', methods=['POST'])
def load_mailset(mailset):
    import os
    from tarfile import TarFile
    mbox_root = os.path.join(os.environ['HOME'], 'mailsets')
    if not os.path.isdir(os.path.join(mbox_root)):
        os.mkdir(mbox_root)

    if len(os.listdir(mbox_root)) == 0:
        response = requests.get('https://example.wazokazi.is:8154/go/static/mediumtagged.tar.gz', verify=False)
        mbox_archive_path = os.path.join(mbox_root, 'mediumtagged.tar.gz')
        mbox_archive = open(mbox_archive_path, 'w')
        mbox_archive.write(response.content)
        mbox_archive.close()
        tarfile = TarFile(name=mbox_archive_path)
        tarfile.extractall(path=mbox_root)

    mail_service.load_mailset()

    return respond_json(None)



@app.route('/')
def index():
    return app.send_static_file('index.html')


def setup():
    app.run(host="0.0.0.0", debug=True, port=4567)


if __name__ == '__main__':
    setup()