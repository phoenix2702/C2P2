from flask import Flask, request, jsonify, render_template
import numpy as np
import pickle
from flask_cors import CORS

app = Flask(__name__)

# ✅ Load trained model
with open("multi_armed_bandit_model_2.pkl", "rb") as f:
    loaded_model = pickle.load(f)
print("Keys in loaded model:", loaded_model.keys())

# Extract model parameters
topic_to_index = loaded_model["topic_to_index"]
rewards = loaded_model["rewards"]
counts = loaded_model["counts"]
avg_rewards = loaded_model["avg_rewards"]
subject_to_topics = loaded_model["subject_to_topics"]  # ✅ Get subject-topic mapping

# ✅ Define subjects
subjects = ["Math", "Science", "English"]
epsilon = 0.1  # Exploration rate
CORS(app)

# ✅ Function to find weakest subject
def determine_weak_subject(scores):
    min_score_index = np.argmin(scores)
    return subjects[min_score_index]

# ✅ Function to recommend a topic (No CSV)
def recommend_topic(weak_subject):
    available_topics = subject_to_topics.get(weak_subject, [])

    if not available_topics:
        return "No data available for this subject."

    topic_indexes = [topic_to_index[topic] for topic in available_topics if topic in topic_to_index]

    if not topic_indexes:
        return "No matching topic found in trained data."

    if np.random.rand() < epsilon:
        selected_index = np.random.choice(topic_indexes)
    else:
        selected_index = max(topic_indexes, key=lambda i: avg_rewards[i])

    return list(topic_to_index.keys())[selected_index]

# ✅ Route to serve index.html
@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

# ✅ API Endpoint
@app.route("/recommend", methods=["POST"])
def get_recommendation():
    data = request.get_json()
    scores = [data["math"], data["science"], data["english"]]

    weak_subject = determine_weak_subject(scores)
    recommended_topic = recommend_topic(weak_subject)  # ✅ No CSV used

    return jsonify({"weak_subject": weak_subject, "recommended_topic": recommended_topic})

if __name__ == "__main__":
    # Run Flask app
    app.run(port=5000)
