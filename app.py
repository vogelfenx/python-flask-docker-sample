import json

from flask import Flask, redirect, request, url_for

from db import connect_db

app = Flask(__name__)


@app.route('/')
def hello_docker():
    return 'Hello, Docker!!'


@app.route('/widgets')
def get_widgets():
    mydb = connect_db()
    cursor = mydb.cursor()

    cursor.execute("USE inventory")
    cursor.execute("SELECT * FROM widgets")

    # this will extract row headers
    row_headers = [x[0] for x in cursor.description]

    results = cursor.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))

    cursor.close()

    return json.dumps(json_data)


@app.route('/initdb')
def db_init():
    mydb = connect_db()
    cursor = mydb.cursor()

    cursor.execute("DROP DATABASE IF EXISTS inventory")
    cursor.execute("CREATE DATABASE inventory")

    cursor.execute("USE inventory")

    cursor.execute("DROP TABLE IF EXISTS widgets")
    cursor.execute(
        "CREATE TABLE widgets (name VARCHAR(255), description VARCHAR(255))")
    cursor.close()

    return redirect(url_for('add_widget'))


@app.route('/widgets/add', methods=['GET', 'POST'])
def add_widget():
    if request.method == 'POST':
        widget_name = request.form['name']
        widget_desc = request.form['desc']
        mydb = connect_db()
        cursor = mydb.cursor()

        cursor.execute("USE inventory")
        cursor.execute(("INSERT INTO widgets (name, description) VALUES ('{}', '{}')").format(
            widget_name, widget_desc))
        mydb.commit()
        cursor.close()

        return redirect(url_for('get_widgets'))
    else:
        return '''
        <form action="/widgets/add" method="post">
            <p>Name <input type="text" name="name"> </p>
            <p>Description <input type="text" name="desc" alue=""></p>
            <p><input type="submit" value="send"></p>
        </form>
        '''


if __name__ == "__main__":
    app.run(host='0.0.0.0')
