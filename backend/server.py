import flask

app = flask.Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024**2


@app.post('/api/submit')
def handle_submit():
    data = flask.request.get_data() 
    print(data)
    print(flask.request.form)
    print(flask.request.files)
    fnames = list(flask.request.files)
    print(flask.request.files[fnames[1]].read())
    # print(k)
    # print(v)
    return data