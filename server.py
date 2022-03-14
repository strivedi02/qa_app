import time
import json
import flask
import MySQLdb
from datetime import datetime
from flask import Flask, request, render_template, make_response, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_question', methods=["POST"])
def search_question():
    if request.method == "POST":
        question = request.form['question']
        db = MySQLdb.connect("localhost", "root", "root",
                         "question_answer", charset='utf8')
        sql = f"select * from qa_table where question='{question}'"
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            sql = f"insert into qa_table(question) values('{question}')"
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
            cursor.close()
            return make_response(jsonify("Question Added in DB"), 200)
        cursor.close()
        return make_response(jsonify(result), 200)

@app.route('/upsearch_question', methods=["POST"])
def upsearch_question():
    if request.method == "POST":
        question = request.form['question']
        db = MySQLdb.connect("localhost", "root", "root",
                         "question_answer", charset='utf8')
        sql = f"select * from qa_table where question='{question}'"
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        if len(result) == 0:
            return make_response(jsonify("Question Not found in DB"), 200)
        return make_response(jsonify(result), 200)

@app.route('/update_answer', methods=["POST"])
def update_answer():
    if request.method == "POST":
        print(request.get_json())
        db = MySQLdb.connect("localhost", "root", "root",
                         "question_answer", charset='utf8')
        cursor = db.cursor()
        answer_1 = request.get_json()['answer_1']
        answer_2 = request.get_json()['answer_2']
        answer_3 = request.get_json()['answer_3']
        sql_answer_1 = f"update qa_table set answer_1='{request.get_json()['answer_1']}' where q_id={request.get_json()['id']}" if request.get_json()['answer_1'] != '' else f"update qa_table set answer_1=NULL where q_id='{request.get_json()['id']}'"
        sql_answer_2 = f"update qa_table set answer_2='{request.get_json()['answer_2']}' where q_id={request.get_json()['id']}" if request.get_json()['answer_2'] != '' else f"update qa_table set answer_2=NULL where q_id='{request.get_json()['id']}'"
        sql_answer_3 = f"update qa_table set answer_3='{request.get_json()['answer_3']}' where q_id={request.get_json()['id']}" if request.get_json()['answer_3'] != '' else f"update qa_table set answer_3=NULL where q_id='{request.get_json()['id']}'"
        cursor.execute(sql_answer_1)
        cursor.execute(sql_answer_2)
        cursor.execute(sql_answer_3)
        db.commit()
        cursor.close()
    return make_response(jsonify("DB has been updated"), 200)
        

if __name__ == '__main__':
    app.run(debug=True, port=8000, use_reloader=True)