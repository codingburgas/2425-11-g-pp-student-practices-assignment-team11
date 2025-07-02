from flaskProject import create_app
from config import Config

app = create_app(Config)

from flask import request, session,redirect,url_for

@app.route('/set_language/<lang>')
def set_language(lang):
    session['language'] = lang
    return redirect(request.referrer or url_for('main.index'))

if __name__ == '__main__':
    app.run(debug=True)
