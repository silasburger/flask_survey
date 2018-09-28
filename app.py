from flask import Flask, request, session, render_template, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys as s

app = Flask(__name__)
app.config['SECRET_KEY'] = 'seekrit'

debug = DebugToolbarExtension(app)

@app.route('/')
def choose():
    titles = []
    survey_id=[]
    for survey in s:
        titles.append(s[survey].title)
        survey_id.append(survey)

    return render_template('choose.html',titles=zip(titles,survey_id))

@app.route('/instruction')
def homepage():
    survey = request.args['survey']
    session['survey'] = survey
    session['responses'] = {}

    return render_template('start.html', survey_title=s[survey].title, survey_instructions=s[survey].instructions)

@app.route('/survey/<int:question_num>', methods=["POST"])
def survey_page(question_num):
    if not question_num == 0:
        last_question = s[session['survey']].questions[question_num-1].question
        responses = session['responses']
        responses[last_question] = request.form['answer']
        session['responses'] = responses

    if question_num < len(s[session['survey']].questions):
        question = s[session['survey']].questions[question_num].question
        choices = s[session['survey']].questions[question_num].choices
        question_num += 1
        return render_template('question.html', survey_question=question, choices=choices, question_num=question_num)
    else: 
        return redirect('/thanks')
   
@app.route('/thanks')
def thanks():
    responses=session['responses']
    
    return render_template('thanks.html', responses=responses)