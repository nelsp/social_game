from flask import Flask, request, render_template
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num_inputs = int(request.form['num_inputs'])
        question = request.form['question']
        low_range = int(request.form['low_range'])
        high_range = int(request.form['high_range'])
        return render_template('inputs.html', 
                             num_inputs=num_inputs,
                             question=question,
                             low_range=low_range,
                             high_range=high_range)
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    inputs = []
    player_name = request.form.get('player_name', 'Anonymous')
    num_inputs = len([k for k in request.form.keys() if k.startswith('input_')])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for key, value in request.form.items():
        if key.startswith('input_'):
            inputs.append(value)
    
    # Append to file
    with open('inputs.txt', 'a') as f:
        f.write(f"\n{timestamp} - {player_name}: {', '.join(inputs)}")
    
    # Redirect back to a fresh form with the same number of inputs
    return render_template('inputs.html', num_inputs=num_inputs, message="Submission successful!")

if __name__ == '__main__':
    app.run(debug=True)