from flask import Flask, request, render_template_string,render_template,json
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'newuser'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'reports'
app.secret_key = 'password'

mysql = MySQL(app)

@app.route('/')
def list_alerts():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM alertas")
    data = cursor.fetchall()
    cursor.close()
    return render_template('list_alerts.html', data=data)



@app.route('/alert', methods=['POST'])
def alert():
    data = request.get_json()
    print(f"==================> {data}")
    for alert in data['alerts']:
        if alert['status'] == 'firing':
            status = alert['status']
            alertname = alert['labels']['alertname']
            instance = alert['labels']['instance']
            severity = alert['labels']['severity']
            startsAt = alert['startsAt']
            endsAt = alert['endsAt']
            cursor = mysql.connection.cursor()
            cursor.execute(f"INSERT INTO alertas (status, alertname, instance,severity,startsAt,endsAt) VALUES ('{status}','{alertname}','{instance}','{severity}','{startsAt}','{endsAt}')")
            mysql.connection.commit()
            cursor.close()
    # Renderiza a página HTML com os alertas
    return "Registro incluído com sucesso", 200

@app.route('/alerts')
@app.route('/alerts/<status>')
def alerts(status=None):
    if status:
        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT * FROM alertas WHERE status='{status}'")
        data = cursor.fetchall()
        cursor.close()
    else:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM alertas")
        data = cursor.fetchall()
        cursor.close()
    return render_template('list_alerts.html', data=data)

@app.route('/charts')
def charts():
    return render_template('charts.html')


@app.route('/data')
def get_alerts_data():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT severity, alertname, COUNT(*) as count FROM alertas GROUP BY severity, alertname')
    data = cursor.fetchall()
    cursor.close()

    # Formata os dados como uma lista de dicionários
    keys = ['severity', 'alertname', 'count']
    alerts = [dict(zip(keys,row)) for row in data]

    # Retorna os dados em formato JSON
    return json.dumps(alerts)

@app.route('/alerts/severity/<severity>')
def alerts_by_severity(severity):
    data = get_alerts_by_severity(severity)
    return render_template('list_alerts.html', data=data)


