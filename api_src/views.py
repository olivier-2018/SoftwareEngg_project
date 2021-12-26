from api_src import app


@app.route("/")
def index():
    return "Hello world !"
