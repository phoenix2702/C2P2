from flask import Flask, request, jsonify
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

@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        # Get JSON data from request
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input"}), 400

        # Convert scores to integers
        student_scores = {topic: int(data[topic]) for topic in all_topics if topic in data}

        # Identify the weakest topic
        weakest_topic = get_weakest_topic(student_scores)
        return jsonify({"recommended_topic": weakest_topic})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
