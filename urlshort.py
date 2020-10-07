from flask import render_template,request,redirect,url_for,flash,abort, session,jsonify,Blueprint
import json
import os.path
from werkzeug.utils import secure_filename

bp = Blueprint('urlshort',__name__)

bp = Flask(__name__)
bp.secret_key = 'djfnfjd3h55u5'
@bp.route('/')
def home():
    return render_template('index.html',Name='Chetan',codes = session.keys())


@bp.route('/add')
def add():
    return render_template('adduser.html')


@bp.route('/details',methods=["Post","GET"])
def details():

    # print(request.args['uname'],request.args['age'])
    if request.method=="POST":
        urls={}

        if os.path.exists('urls.json'):
            with open('urls.json') as url_files:
                urls = json.load(url_files)
        
        if request.form['code'] in urls.keys():
            flash('name already been taken. Please add different')
            return redirect(url_for('urlshort.home'))

        if 'url' in request.form.keys():
            urls[request.form['code']]={'url':request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('C:/Users/cs123/OneDrive/Desktop/PythonFlask/urlshort' + full_name)   
            urls[request.form['code']]={'file':full_name}


        
        with open('urls.json','w') as url_files:
            json.dump(urls,url_files)
            session[request.form['code']] = True

        return render_template('details.html',code=request.form['code'])
    else:
        return redirect(url_for('urlshort.home'))

@bp.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as url_files:
            urls = json.load(url_files)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static',filename='/user_files/' + urls[code]['file']))
    return abort(404)

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404    

@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))

bp.run(debug=True)   