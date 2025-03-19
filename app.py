from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load trained model
model_path = "multi_armed_bandit_model (1).pkl"
with open(model_path, "rb") as f:
    model_data = pickle.load(f)

# Extract stored data
topic_to_index = model_data["topic_to_index"]
subject_to_topics = model_data["subject_to_topics"]

all_topics = list(topic_to_index.keys())

def get_weakest_topic(student_scores):
    """Identify the weakest subtopic based on the lowest score."""
    return min(student_scores, key=student_scores.get)

@app.route("/", methods=["GET", "POST"])
def index():
    recommendation = None
    if request.method == "POST":
        # Get scores from the form
        student_scores = {topic: int(request.form[topic]) for topic in all_topics}
        
        # Identify weakest topic
        recommended_topic = get_weakest_topic(student_scores)
        recommendation = f"🔍 Recommended Topic for Improvement: {recommended_topic}"
    
    return render_template("index.html", topics=all_topics, recommendation=recommendation)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # Fixed: Added host and port
