with open('inputs.txt', 'r') as file:
    lines = file.readlines()

# print(lines)

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

print(parse_inputs_file())

def handle_game_completion(num_players, submissions):
    if len(submissions) == num_players:
        # Create player dictionary from submissions
        player_dic = read_log(num_players)
        
        # Calculate winners
        self_awareness, other_awareness = calc_winners1b(player_dic)
        
        return {
            'self_awareness_winner': self_awareness,
            'other_awareness_winner': other_awareness
        }
    return None


# # Example usage:
# app.route('/results')
# ef show_results():
#    data = parse_inputs_file()
#    print(data)  # For debugging
#    return str(data)  # Or pass to template