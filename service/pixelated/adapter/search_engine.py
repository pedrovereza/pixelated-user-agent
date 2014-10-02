from whoosh.fields import *
from whoosh.filedb.filestore import RamStorage
from whoosh.qparser import QueryParser

SCHEMA = Schema(
    ident=ID(stored=True),
    sender=ID(stored=False),
    to=ID(stored=False),
    cc=ID(stored=False),
    bcc=ID(stored=False),
    subject=TEXT(stored=False),
    body=TEXT(stored=False),
    tag=KEYWORD(stored=False, commas=True)
)
IDX = RamStorage().create_index(SCHEMA, indexname='pixelindex')


def add_to_index(mails):
    converted_mails = list()
    for mail in mails:
        mdict = mail.as_dict()
        header = mdict['header']
        tags = mdict.get('tags', [])
        tags.append(mail.mailbox_name.lower())
        converted_mails.append(
            {
                'sender': unicode(header.get('from', '')),
                'subject': unicode(header.get('subject', '')),
                'to': unicode(header.get('to', '')),
                'cc': unicode(header.get('cc', '')),
                'bcc': unicode(header.get('bcc', '')),
                'tag': u','.join(tags),
                'body': unicode(mdict['body']),
                'ident': unicode(mdict['ident'])
            }
        )

    writer = IDX.writer()
    for mail in converted_mails:
        writer.add_document(**mail)
    writer.commit()


def search(query, default_field='body'):
    query = query.replace('\"', '')
    query = query.replace('-in:', 'AND NOT tag:')
    query = query.replace('in:all', '*')
    print 'Using %s of memory' % IDX.storage.total_size()
    with IDX.searcher() as searcher:
        query = QueryParser(default_field, IDX.schema).parse(query)
        results = searcher.search(query)
        return [mail['ident'] for mail in results]
