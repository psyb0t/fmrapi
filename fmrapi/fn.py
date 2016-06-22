from bson import ObjectId
from functools import wraps
from flask import jsonify


def format_response(fn):
    @wraps(fn)
    def _fr(*args, **kwargs):
        ret_data = fn(*args, **kwargs)

        r = jsonify({
            'status': ret_data.get('status'),
            'msg': ret_data.get('msg'),
            'data': ret_data.get('data')
        })
        r.status_code = ret_data.get('code', 200)

        return r

    return _fr


def fetch_items(collection, limit=0, query={}):
    if 'id' in query:
        query['_id'] = ObjectId(query['id'])
        del(query['id'])

    try:
        res = collection.find(query).sort('_id', -1).limit(limit)
    except:
        return False, 'Could not fetch collection items.'

    items = []
    for item in res:
        item['id'] = str(item['_id'])
        del(item['_id'])

        items.append(item)

    return items, '%s items fetched.' % len(items)


def insert_item(collection, item):
    try:
        collection.insert_one(item)
    except:
        return False, 'Item insertion failed!'

    item['id'] = str(item['_id'])
    del(item['_id'])

    return item, 'Item successfully inserted'


def fetch_item(collection, item_id):
    try:
        item = collection.find_one({'_id': ObjectId(item_id)})
    except:
        return False, 'Could not fetch item!'

    if not item:
        return False, 'Inexistent item!'

    item['id'] = item_id
    del(item['_id'])

    return item, 'Item successfully fetched!'


def update_item(collection, item):
    if 'id' not in item:
        return False, 'Item id not specified!'

    _item_id = ObjectId(item['id'])
    del(item['id'])

    try:
        collection.update({'_id': _item_id}, item)
    except:
        return False, 'Could not update the item!'

    return item, 'Item was successfully updated!'
