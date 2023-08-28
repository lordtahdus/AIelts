from flask import Flask, render_template, request, jsonify


app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/generate_feedback', methods=['POST'])
def generate_feedback():
    data = request.json  # Get data sent by frontend 
    
    writing_question = data['writingQuestion']
    user_writing = data['userWriting']
    prompt = "Topic: \n" + writing_question + "\n" + "Essay: \n" + user_writing + "\n\n###\n\n"
    
    feedback = "em dep lam"
    
    
    # get feedback
    # get 5 feedbacks
    response = {'feedback': feedback}
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
