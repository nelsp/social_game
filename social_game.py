#social_game
import statistics

num_players = int(input("Enter the number of players: "))
question = input("Enter the question: ")
print(question)
high_range = int(input("Enter the high range: "))
low_range = int(input("Enter the low range: "))
print('high range', high_range, 'low range', low_range)


data_list = {}

for i in range(num_players):
    player_guesses = []
    for j in range(num_players):
        guess = int(input(f"Player {i+1}, enter your guess for player {j+1}: "))
        if guess > high_range or guess < low_range:
            print('guess out of range')
            guess = input(f"Player {i+1}, enter your guess for player {j+1}: ")
        player_guesses.append([j+1, float(guess)])
    data_list[i+1] = player_guesses

print('data list  ', data_list)


def calc_winners(num_players, data_list):
    #calculate priors per player    
    priors_per_player = []

    for i in range(num_players):
        ppp = []
        for j in range(num_players):
            ppp.append(data_list[j+1][i][1])
        priors_per_player.append([i+1, ppp])

    # print('priors per player  ', priors_per_player)

    #calculate the adjusted avg prior minus the self guess
    adjusted_avg_prior = []
    players_self_guess = []
    for i in range(num_players):
        adj_avg = []
        
        for j in range(num_players):
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
    for i in range(num_players):
        diff_avg = []
        
        for j in range(num_players):
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

    print('self awareness  ', self_awareness[0])
    print('other awareness  ', other_awareness[0])
    return self_awareness[0], other_awareness[0]

def calc_winners1(data_dic):
    #calculate priors per player    
    priors_per_player = []

    for i in range(data_dic):
        ppp = []
        for j in range(data_dic):
            ppp.append(data_list[j+1])
        priors_per_player.append([i+1, ppp])

    # print('priors per player  ', priors_per_player)

    #calculate the adjusted avg prior minus the self guess
    adjusted_avg_prior = []
    players_self_guess = []
    for i in range(num_players):
        adj_avg = []
        
        for j in range(num_players):
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
    for i in range(num_players):
        diff_avg = []
        
        for j in range(num_players):
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

    print('self awareness  ', self_awareness[0])
    print('other awareness  ', other_awareness[0])
    return self_awareness[0], other_awareness[0]





print(calc_winners1(num_players, data_list))



