import json
from flask import request
from fmrapi import app, database, fn
from urllib import unquote


@app.route('/<table_name>', methods=['GET', 'POST', 'DELETE'])
@fn.format_response
def table_acts(table_name):
    collection = database[table_name]

    try:
        limit = int(request.args.get('limit'))
    except:
        limit = 0

    if request.method == 'GET':
        items, msg = fn.fetch_items(collection, limit=limit)
        if items is False:
            return {
                'status': 'ERROR',
                'msg': msg,
                'code': 500
            }

        return {
            'status': 'OK',
            'msg': msg,
            'data': items
        }

    try:
        data = json.loads(request.get_data())
    except:
        return {
            'status': 'ERROR',
            'msg': 'Invalid request!',
            'code': 400
        }

    if request.method == 'POST':
        item, msg = fn.insert_item(collection, data)
        if item is False:
            return {
                'status': 'ERROR',
                'msg': msg,
                'code': 500
            }

        return {
            'status': 'OK',
            'msg': msg,
            'data': item
        }

    if request.method == 'DELETE':
        try:
            database.drop_collection(table_name)
            return {
                'status': 'OK',
                'msg': 'Collection successfully dropped!'
            }
        except:
            return {
                'status': 'ERROR',
                'msg': 'Collection drop failed!',
                'code': 500
            }

    return {
        'status': 'ERROR',
        'msg': 'Invalid request!',
        'code': 400
    }


@app.route('/<table_name>/<item_id>',
           methods=['GET', 'PUT', 'DELETE'])
@fn.format_response
def item_acts(table_name, item_id):
    collection = database[table_name]

    item, msg = fn.fetch_item(collection, item_id)
    if item is False:
        return {
            'status': 'ERROR',
            'msg': msg,
            'code': 500
        }

    if request.method == 'GET':
        return {
            'status': 'OK',
            'msg': msg,
            'data': item
        }

    if request.method == 'PUT':
        try:
            data = json.loads(request.get_data())
        except:
            return {
                'status': 'ERROR',
                'msg': 'Invalid request!',
                'code': 400
            }

        data['id'] = item_id

        item, msg = fn.update_item(collection, data)
        if item is False:
            return {
                'status': 'ERROR',
                'msg': msg,
                'code': 500
            }

        return {
            'status': 'OK',
            'msg': msg,
            'data': item
        }

        if request.method == 'GET':
            return {
                'status': 'OK',
                'msg': msg,
                'data': item
            }

    if request.method == 'DELETE':
        item['_id'] = fn.ObjectId(item_id)
        del(item['id'])

        try:
            collection.remove(item)

            return {
                'status': 'OK',
                'msg': 'Successfully deleted item!'
            }
        except:
            return {
                'status': 'ERROR',
                'msg': 'Could not delete the item!',
                'code': 500
            }
