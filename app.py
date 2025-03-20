from flask import Flask, render_template, request, jsonify
import pickle

app = Flask(__name__)

# Load trained model
model_path = "multi_armed_bandit_model (1).pkl"
with open(model_path, "rb") as f:
    model_data = pickle.load(f)

# Extract stored data
topic_to_index = model_data["topic_to_index"]
all_topics = list(topic_to_index.keys())

def get_weakest_topic(student_scores):
    """Identify the weakest subtopic based on the lowest score."""
    return min(student_scores, key=student_scores.get)

@app.route("/")
def index():
    return render_template("index.html", topics=all_topics)

@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input: No data received"}), 400

        # Convert scores to integers and validate input
        student_scores = {}
        for topic in all_topics:
            if topic in data:
                try:
                    student_scores[topic] = int(data[topic])
                except ValueError:
                    return jsonify({"error": f"Invalid score for {topic}. Must be a number."}), 400
        
        # Ensure at least one valid score is provided
        if not student_scores:
            return jsonify({"error": "No valid scores provided"}), 400

        # Identify weakest topic
        weakest_topic = get_weakest_topic(student_scores)
        return jsonify({"recommended_topic": weakest_topic})

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
