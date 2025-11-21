from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/boys')
def boys():
    return render_template("boys.html")

@app.route('/girls')
def girls():
    return render_template("girls.html")
if __name__ == '__main__':
    app.run()
