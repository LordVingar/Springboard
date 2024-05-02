from flask import Flask, render_template, request, redirect, url_for
from stories import Story

app = Flask(__name__)

# Add multiple story templates
stories = {
    "Story 1": Story(["noun", "verb"], "I love to {verb} a good {noun}."),
    "Story 2": Story(["place", "verb", "noun"], "In a {place}, I {verb} a {noun}."),
    "Story 3": Story(["adjective", "noun", "verb"], "The {adjective} {noun} {verb} swiftly.")
}

@app.route('/', methods=['GET', 'POST'])
def home():
    # Get the list of story templates
    templates = list(stories.keys())

    if request.method == 'POST':
        # Get the selected template from the form
        selected_template = request.form['template']
        # Get the prompts from the selected story
        prompts = stories[selected_template].prompts
        # Redirect to the story page with the selected template
        return redirect(url_for('story', template=selected_template))

    # Render the form with the dropdown menu
    return render_template('home.html', templates=templates)

@app.route('/story/<template>', methods=['GET', 'POST'])
def story(template):
    # Get the prompts from the selected story
    prompts = stories[template].prompts

    if request.method == 'POST':
        # Get user-provided answers from the form
        answers = {prompt: request.form[prompt] for prompt in prompts}
        # Generate the story
        generated_story = stories[template].generate(answers)
        return render_template('story.html', story=generated_story)

    # Render the form for user inputs
    return render_template('story_form.html', prompts=prompts, template=template)

if __name__ == '__main__':
    app.run(debug=True)