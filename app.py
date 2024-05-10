from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Assuming `Survey` and `Question` are defined elsewhere and imported
from surveys import Survey, Question, surveys

@app.route('/')
def survey_list():
    return render_template('survey_list.html', surveys=surveys)

@app.route('/start/<survey_code>', methods=['GET', 'POST'])
def start_survey_code(survey_code):
    if request.method == 'POST':
        if request.cookies.get('survey_done'):
            flash('You have already completed the survey.')
            return redirect(url_for('survey_list'))
        session['responses'] = []
        session['survey_code'] = survey_code
        return redirect(url_for('show_question', survey_code=survey_code, question_id=0))
    return render_template('start.html', survey_code=survey_code)

@app.route('/questions/<survey_code>/<int:question_id>', methods=['GET'])
def show_question(survey_code, question_id):
    survey = surveys[survey_code]
    if 'responses' not in session or question_id != len(session['responses']):
        flash('Trying to access an invalid question.', 'error')
        return redirect(url_for('show_question', survey_code=survey_code, question_id=len(session.get('responses', []))))
    if question_id >= len(survey.questions):
        return redirect(url_for('complete', survey_code=survey_code))
    return render_template('question.html', question=survey.questions[question_id], question_id=question_id, survey_code=survey_code)

@app.route('/answer/<survey_code>', methods=['POST'])
def handle_answer(survey_code):
    survey = surveys[survey_code]
    responses = session.get('responses', [])
    answer = request.form['answer']
    comment = request.form.get('comment')
    response = {'answer': answer, 'comment': comment} if comment else {'answer': answer}
    responses.append(response)
    session['responses'] = responses

    if len(responses) >= len(survey.questions):
        return redirect(url_for('complete', survey_code=survey_code))
    return redirect(url_for('show_question', survey_code=survey_code, question_id=len(responses)))

@app.route('/', methods=['GET', 'POST'])
def index():
    return '<body><a href="/admin/">Click me to get to Home!</a></body>'

app.run()

@app.route('/complete/<survey_code>')
def complete(survey_code):
    survey = surveys[survey_code]
    responses = session.get('responses', [])
    resp = make_response(render_template('complete.html', survey=survey, responses=responses))
    resp.set_cookie('survey_done', 'true', max_age=60*60*24*30)  # Expires in 30 days
    session.clear()  # Clear the session after completing the survey
    return resp

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)