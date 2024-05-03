from flask import Flask, render_template, redirect, url_for, request, abort, flash, session
from surveys import surveys

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session

@app.route('/')
def home():
    # Render the homepage with a button to start the survey
    return render_template('home.html', surveys=surveys)

@app.route('/start_survey/<survey_name>', methods=['POST'])
def start_survey(survey_name):
    # Initialize session variable for responses
    session['responses'] = []
    # Redirect to the first question of the survey
    return redirect(url_for('survey', survey_name=survey_name, question_index=0))

@app.route('/survey/<survey_name>/questions/<int:question_index>', methods=['GET', 'POST'])
def survey(survey_name, question_index):
    # Retrieve the survey object based on the survey name
    survey = surveys.get(survey_name)

    if survey is None:
        return render_template('error.html', message='Survey not found.')

    # Check if the survey has questions
    if question_index >= len(survey.questions) or question_index < 0:
        # Flash message for invalid question index
        flash('Invalid question index. Redirected to the first question.')
        # Redirect to the first question
        return redirect(url_for('survey', survey_name=survey_name, question_index=0))

    question = survey.questions[question_index]

    if request.method == 'POST':
        # Store the response in the session
        response = request.form['response']
        session_responses = session.get('responses', [])
        session_responses.append(response)
        session['responses'] = session_responses

        # Redirect to the next question or thank you page
        if question_index + 1 < len(survey.questions):
            return redirect(url_for('survey', survey_name=survey_name, question_index=question_index + 1))
        else:
            return redirect(url_for('thank_you'))

    # Render the question form
    return render_template('question.html', survey=survey, survey_name=survey_name, question=question, question_index=question_index)

@app.route('/thank_you')
def thank_you():
    # Render the thank you page
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)