from flask import Flask, request, redirect, url_for, send_from_directory

app = Flask(__name__)
app.debug = True

@app.route('/')
def root():
	return redirect("/static/index.html", code=302)

@app.route('/getfile')

if __name__ == '__main__':
	app.run()