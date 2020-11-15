from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def words():
    return render_template("words.html")

@app.route("/first")
def first():
    return render_template('firstdir.html')

if __name__ == '__main__':
    app.run(debug = True)
