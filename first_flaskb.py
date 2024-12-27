from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime
import statistics

app = Flask(__name__)

def parse_inputs_file():
   result_dict = {}
   
   with open('inputs.txt', 'r') as f:
       for line in f:
           
            first_part = line.split(':')
               
               # Extract player number (assuming format "timestamp - PlayerX")
            player_num = first_part[2].split('-')[1].strip()
               
               # Convert the comma-separated numbers into a list of integers
            numbers = [int(num.strip()) for num in first_part[3].strip().split(',')]
               
            result_dict[player_num] = numbers
   
   return result_dict

def calc_winners1b(data_dic):
    #calculate priors per player
    #sort the data_dic by the keys
    sorted_data_dic = sorted(data_dic.items(), key=lambda x: x[0])
    # print('sorted data dic  ', sorted_data_dic)
    priors_per_player = []
    count = 0
    for i in range(len(sorted_data_dic)):
        
        ppp = []    
        for j in range(len(sorted_data_dic)):
            ppp.append(sorted_data_dic[j][1][count])
        
        priors_per_player.append([sorted_data_dic[i][0], ppp])
        count += 1
    # print('priors per player  ', priors_per_player)

    #calculate the adjusted avg prior minus the self guess
    adjusted_avg_prior = []
    players_self_guess = []
    for i in range(len(priors_per_player)):
        adj_avg = []
        
        for j in range(len(priors_per_player)):
            if i+1 == j+1:
                players_self_guess.append([priors_per_player[i][0], priors_per_player[i][1][j]])
            else:
                adj_avg.append(priors_per_player[i][1][j])
        # print('adj avg  ', adj_avg)
        final_avg = (statistics.mean(adj_avg) + statistics.median(adj_avg)) / 2
        adjusted_avg_prior.append([i+1, final_avg])

    # print('adjusted avg prior  ', adjusted_avg_prior)
    # print('players self guess  ', players_self_guess)

    diff_prior = []
    diff_self_guess = []
    for i in range(len(priors_per_player)):
        diff_avg = []
        
        for j in range(len(priors_per_player)):
            if i+1 == j+1:
                diff_self_guess.append([priors_per_player[i][0], abs(priors_per_player[i][1][j]-adjusted_avg_prior[i][1])])
            else:
                diff_avg.append(abs(priors_per_player[j][1][i] - adjusted_avg_prior[j][1]))
        diff_prior.append([i+1, diff_avg])
        # print('diff prior  ', diff_prior)

    # print('diff prior  ', diff_prior)
    # print('diff self guess  ', diff_self_guess)

    #determine winners
    self_awareness = min(diff_self_guess, key=lambda x: x[1])
    other_awareness = min(diff_prior, key=lambda x: sum(x[1]))

    # print('self awareness  ', self_awareness[0])
    # print('other awareness  ', other_awareness[0])
    return self_awareness[0], other_awareness[0]

def handle_game_completion(num_players, submissions):
    if len(submissions) == num_players:
        # Create player dictionary from submissions
        player_dic = parse_inputs_file()
        
        # Calculate winners
        self_awareness, other_awareness = calc_winners1b(player_dic)
        
        return {
            'self_awareness_winner': self_awareness,
            'other_awareness_winner': other_awareness
        }
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Clear any previous game results when starting a new game
        try:
            open('inputs.txt', 'w').close()
            open('game_results.txt', 'w').close()
        except FileNotFoundError:
            pass
            
        num_players = int(request.form['num_inputs'])
        question = request.form['question']
        low_range = int(request.form['low_range'])
        high_range = int(request.form['high_range'])
        
        # Store game settings
        with open('game_settings.txt', 'w') as f:
            f.write(f"{num_players}\n")
            f.write(f"{question}\n")
            f.write(f"{low_range}\n")
            f.write(f"{high_range}\n")
        
        # Instead of rendering the input form directly, 
        # give a URL that players can use
        return render_template('share.html', play_url=url_for('play', _external=True))
        
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    inputs = []
    player_name = request.form.get('player_name', 'Anonymous')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for key, value in request.form.items():
        if key.startswith('input_'):
            inputs.append(value)
    
    # Append to file with player name
    with open('inputs.txt', 'a') as f:
        f.write(f"{timestamp} - {player_name}: {', '.join(inputs)}\n")
    
    return redirect(url_for('display_results'))

@app.route('/results', methods=['GET'])
def display_results():
    # Get required number of players
    with open('game_settings.txt', 'r') as f:
        required_players = int(f.readline().strip())
    
    # Read all submissions and extract player names
    try:
        submitted_players = []
        with open('inputs.txt', 'r') as f:
            submissions = f.readlines()
            for line in submissions:
                # Extract player name from the line format "timestamp - playername: numbers"
                player_name = line.split('- ')[1].split(':')[0].strip()
                submitted_players.append(player_name)
        
        current_players = len(submitted_players)
        
        if current_players < required_players:
            # Not everyone has submitted yet
            return render_template('waiting.html',
                                 current_submissions=current_players,
                                 total_needed=required_players,
                                 submitted_players=submitted_players)
        else:
            # All players have submitted, calculate winners
            player_dic = parse_inputs_file()
            self_awareness, other_awareness = calc_winners1b(player_dic)
            
            # Create a results file to indicate game completion
            with open('game_results.txt', 'w') as f:
                f.write(f"{self_awareness}\n{other_awareness}")
            
            # Don't clear inputs.txt yet
            return render_template('results.html',
                                 self_awareness_winner=self_awareness,
                                 other_awareness_winner=other_awareness)
                                 
    except FileNotFoundError:
        # Check if we have results from a completed game
        try:
            with open('game_results.txt', 'r') as f:
                self_awareness = f.readline().strip()
                other_awareness = f.readline().strip()
            return render_template('results.html',
                                 self_awareness_winner=self_awareness,
                                 other_awareness_winner=other_awareness)
        except FileNotFoundError:
            # No results yet, show waiting page
            return render_template('waiting.html',
                                 current_submissions=0,
                                 total_needed=required_players)


@app.route('/play', methods=['GET'])
def play():
    # Read game settings
    with open('game_settings.txt', 'r') as f:
        num_players = int(f.readline().strip())
        question = f.readline().strip()
        low_range = int(f.readline().strip())
        high_range = int(f.readline().strip())
    
    return render_template('play.html',
                         num_players=num_players,
                         question=question,
                         low_range=low_range,
                         high_range=high_range)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
