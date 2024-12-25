from flask import Flask, request, render_template
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num_inputs = int(request.form['num_inputs'])
        return render_template('inputs.html', num_inputs=num_inputs)
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    inputs = []
    player_name = request.form.get('player_name', 'Anonymous')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for key, value in request.form.items():
        if key.startswith('input_'):
            inputs.append(value)
    
    # Append to file instead of overwriting
    with open('inputs.txt', 'a') as f:
        f.write(f"\n{timestamp} - {player_name}: {', '.join(inputs)}")
    
    return 'Inputs saved to file!'

if __name__ == '__main__':
    app.run(debug=True)