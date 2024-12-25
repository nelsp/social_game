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


# # Example usage:
# app.route('/results')
# ef show_results():
#    data = parse_inputs_file()
#    print(data)  # For debugging
#    return str(data)  # Or pass to template