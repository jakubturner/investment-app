from flask import Flask, render_template, request, session
from dotenv import dotenv_values

from src.Calculation import Calculation
from src.DBcm import UseDatabase

config = dotenv_values('../.env')

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['dbconfig'] = {
    'host': config['LOCALHOST_URL'],
    'user': config['DB_USER'],
    'password': config['DB_PWD'],
    'database': config['DATABASE_NAME'],
}

app.secret_key='asdas'


def log_request(req: 'flask_request', res: str) -> None:
    with open('vsearch.log', 'a') as log:
        print(req.form, res, file=log, sep=' | ')

    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """insert into calculations (name, money, years, interest, result) values (%s,%s,%s,%s,%s)"""

        cursor.execute(_SQL, (req.form['name'],
                              req.form['money'],
                              req.form['years'],
                              req.form['interest'],
                              Calculation.calculate_result(money=req.form['money'], years=req.form['years'],
                                                           interest=req.form['interest'])))


@app.get('/')
@app.get('/calculation')
def get_calculation() -> "html":
    return render_template("calculations.html", title='Put your calculation here')


@app.route('/result', methods=['POST'])
def do_calculation() -> str:
    name = request.form['name']
    money = request.form['money']
    years = request.form['years']
    interest = request.form['interest']
    title = 'Here is your result'
    results = Calculation.calculate_result(money=money, years=years, interest=interest)
    log_request(request, results)
    return render_template('result.html', name=name, money=money, years=years, interest=interest, title=title,
                           results=results)


@app.route('/calclog')
def show_log():
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select name, money, years, interest, result from calculations"""
        _QUERY = f'{_SQL}'
        cursor.execute(_QUERY)
        data = cursor.fetchall()
        titles = ('Name', 'Money', 'Years', 'Interest', 'Result')
    return render_template('calclog.html', title='calculation log', data=data, the_row_titles=titles)


@app.route('/login')
def do_login() -> str:
    session['logged_in'] = True
    return 'You are logged in'

@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return 'You are logged out'


if __name__ == '__main__':
    app.run(debug=True)
