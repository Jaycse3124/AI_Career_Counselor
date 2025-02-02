import openai
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import spacy
from sqlalchemy import or_

app = Flask(__name__, template_folder='frontent')
CORS(app)

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Jay%402003@localhost:3306/ai_career_counselor"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Load spaCy NLP Model
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# JobRole Model
class JobRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(100), nullable=False)
    skills_required = db.Column(db.String(300), nullable=False)

# ChatGPT Configuration
openai.api_key = 'key'  # Replace with your OpenAI API key

# Home Route
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# Upload Resume and Get Recommended Jobs
@app.route("/upload_resume", methods=["POST"])
def upload_resume():
    try:
        data = request.json
        skills = data.get("skills", [])

        if not skills:
            return jsonify({"error": "No skills provided"}), 400

        # Find matching job roles based on skills
        matching_jobs = JobRole.query.filter(
            or_(*[JobRole.skills_required.like(f"%{skill}%") for skill in skills])
        ).all()

        jobs = [{"id": job.id, "role_name": job.role_name} for job in matching_jobs]
        return jsonify({"recommended_jobs": jobs})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Chat Route to interact with ChatGPT
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('input')

    if not user_input:
        return jsonify({'error': 'No input provided'}), 400

    try:
        # Send input to ChatGPT API
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use the latest engine
            prompt=user_input,
            max_tokens=150,
            temperature=0.7
        )

        # Get the response from ChatGPT
        chatgpt_response = response.choices[0].text.strip()

        return jsonify({'response': chatgpt_response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask App
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
