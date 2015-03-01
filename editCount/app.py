from flask import Flask, jsonify
from flask import abort
from flask import make_response
from update_json import readJson

app = Flask(__name__,static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('index.html')

''' To get the total number of edits across the edit a thon '''
@app.route('/editCount/api/v1.0/total', methods = ['GET'])
def get_total_count():
    return jsonify( { 'data': data } )

''' To get the edit count of each article '''
@app.route('/editCount/api/v1.0/article/<name>', methods = ['GET'])
def get_article_count(name):
    articleEditInfo = readJson()
    if name in articleEditInfo['articles']:
        return jsonify( { 'count': articleEditInfo['articles'][name] } )
    else:
        abort(404)

''' To get all article related info & edit count '''
@app.route('/editCount/api/v1.0/article/', methods = ['GET'])
def get_article_count_all():
    return jsonify( readJson() )

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

if __name__ == '__main__':
    app.run(debug = True)
