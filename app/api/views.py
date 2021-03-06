from random import sample, shuffle
from flask import render_template, request, make_response, request, jsonify, redirect, url_for
from flask_login import current_user

from . import api
from ..models import MultipleChoiceQuestion, QUESTION_TOPICS, QUIZ_CODES, User
from ..cursos.forms import MultipleChoiceQuizForm

# Reposnds with HTML for the flashed messages
@api.route("/flashed-messages", methods=["POST"])
def flashed_messages():
    return render_template("_flash.html")


"""
QUESTION_TOPICS = (
    "tstc", # Cáncer testicular
    "crvu", # Cáncer cervicouterino
    "plmn", # Cáncer de pulmon
    "psta", # Cáncer de prostata
    "mama", # Cáncer de mama
    "diag"  # Examen diagnostico
)
"""



"""
{
    "quiz_topic": "tstc",
    "num_questions": 4
}

"""

DEFAULT_QUIZ_TOPIC = "diag"
DEFAULT_NUM_QUESTIONS = 3


# Responds with JSON for random quiz given the topic code and number of questions
@api.route("/generate-quiz", methods=["GET"])
def generate_quiz():
    
    # Validate the quiz topic
    quiz_topic = request.args.get("topic", DEFAULT_QUIZ_TOPIC)
    if quiz_topic not in QUESTION_TOPICS:
        quiz_topic = DEFAULT_QUIZ_TOPIC

    # Get the number of questions
    num_questions = request.args.get("num_questions", DEFAULT_NUM_QUESTIONS)
    num_questions = int(num_questions)

    # Sample the database
    db_questions = MultipleChoiceQuestion.objects(topic=quiz_topic)
    total_num_db_questions = db_questions.count()

    # Generate the sample indexes for the db entries    
    sample_indexes = []
    if num_questions >= total_num_db_questions:
        # More entires are demanded, return all of them
        sample_indexes = [i for i in  range(total_num_db_questions)]
        shuffle(sample_indexes)
    else:
        # Valid number of entries asked
        sample_indexes = sample(range(total_num_db_questions), num_questions)
    
    questions = []
    for i in sample_indexes:
        questions.append(db_questions[i].to_json())

    return  jsonify(questions)

@api.route("/get-quiz-html", methods=["POST"])
def get_quiz_html():
    """
    Gives as response:
    {
        answers:[0,1,0],
        scoreToPass: 3,
        htmlForm: "<form> ... </form>"
    }
    """
    # Validate the quiz topic
    quiz_topic = request.args.get("topic", DEFAULT_QUIZ_TOPIC)
    if quiz_topic not in QUESTION_TOPICS:
        quiz_topic = DEFAULT_QUIZ_TOPIC

    # Get the number of questions
    num_questions = request.args.get("num_questions", DEFAULT_NUM_QUESTIONS)
    num_questions = int(num_questions)

    # Generate the quiz
    form = MultipleChoiceQuizForm.generate_random_quiz(topic=quiz_topic, num_questions=num_questions)
    
    num_questions = len(form.questions)

    response = {
        "answers":  [q.correct_answer for q in form.questions],
        "scoreToPass": num_questions,
        "htmlForm": render_template("cursos/_quiz.html", form=form, num_questions=num_questions)
    }

    return response



@api.route("/certificado", methods=["GET"])
def redirect_certificate():
    """Redirects to the certificate page by taking a topic code request arg."""
    # Validate the quiz topic
    quiz_topic = request.args.get("topic", None)
    if quiz_topic is None or quiz_topic not in QUESTION_TOPICS:
        return make_response("INVALID_TOPIC", 400) # Quiz topic not found

    certificate_link = QUIZ_CODES[quiz_topic]["certificate_url"]
    return redirect(url_for("certificate.download_certificate", name=certificate_link))


@api.route("/user-pass-quiz", methods=["POST"])
def user_pass_quiz():
    """Used to make a user pass a quiz"""
    
    # Validate the quiz topic
    quiz_topic = request.args.get("topic", None)
    if quiz_topic is None or quiz_topic not in QUESTION_TOPICS:
        return make_response("INVALID_TOPIC", 400) # Quiz topic not found

    # Validate the email or return error
    email = request.args.get("email", current_user.email)
    if email is None:
        return make_response("INVALID_EMAIL", 400) # Email not found
    
    # Validate user or return error
    user = User.objects(email=email).first()
    if user is None:
        return make_response("USER_NOT_FOUND", 404) # User no found

    # Pass the user'z quiz, return success
    user.set_passed_quiz(quiz_topic, is_passed=True)
    user.save()
    return make_response("1", 200)


@api.route("/get-user-doc", methods=["GET"])
def get_user_doc():
    """GETs user JSON document given an email"""
    # Validate the email or return error
    email = request.args.get("email", current_user.email)
    if email is None:
        return make_response("INVALID_EMAIL", 400) # Email not found
    
    # Validate user or return error
    user = User.objects(email=email).first()
    if user is None:
        return make_response("USER_NOT_FOUND", 404) # User no found

    return user.to_json()



@api.route("/get-user-quiz-data", methods=["GET"])
def get_user_quiz_data():
    """GETs the user's quiz data only"""

    # Validate the email or return error
    email = request.args.get("email", current_user.email)
    if email is None:
        return make_response("INVALID_EMAIL", 400) # Email not found
    
    # Validate user or return error
    user = User.objects(email=email).first()
    if user is None:
        return make_response("USER_NOT_FOUND", 404) # User no found

    return jsonify(user.quiz_data)
    

@api.route("/submit-quiz", methods=["POST"])
def submit_quiz():
    r = request
    d = r.form #TOODO: test this
    return '1'