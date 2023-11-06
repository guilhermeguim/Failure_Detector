import operator
from printer import print_log

def get_next(hex_word, next_states, last_state, SIZE,t_num,curr_path):
    
    print_log('\n\n---FAILURE LOG---' + '\nPOSSIBLE NEXT STATES: ',t_num,curr_path)
    print_log('states: ' + str(next_states),t_num,curr_path)
    print_log('\nlast state: ' + str(last_state),t_num,curr_path)
    
    binary_value = bin(int(hex_word, 16))[2:].zfill(SIZE*8)
    states = []
    similar_list = []
    score_list = []
    
    sum_pop = 0
    for i in next_states:
        sum_pop = sum_pop + int(next_states[i])
    
    
    for i in next_states:
        pop_score = int(next_states[i])/sum_pop
        print(i)
        states.append(i)
        print(next_states[i])
        sum_similar = 0
        binary_pattern = bin(int(i, 16))[2:].zfill(SIZE*8)
        print(binary_pattern)
        for bit in range(len(binary_pattern)):
            if binary_value[bit] == binary_pattern[bit]:
                if binary_value[bit] == '1':
                    sum_similar += 1
                else:
                    sum_similar += 1
                
        similar_score = sum_similar / (SIZE*8)
        similar_list.append(similar_score)
        final_score = (similar_score*2) + pop_score
        score_list.append(final_score)
        
    print_log('\nstate_list: '+ str(states),t_num,curr_path)  
    print_log('\nsimilar_list: '+ str(similar_list),t_num,curr_path)  
    print_log('\nscore_list: '+ str(score_list),t_num,curr_path)  
        
    dict_word_score = {}
    
    for i in range(len(states)):
        key = states[i]
        value = score_list[i]
        dict_word_score[key] = value
        
    dict_word_score = dict(sorted(dict_word_score.items(), key=operator.itemgetter(1),reverse=True))   
    
    print_log('\ndict_word_score: '+ str(dict_word_score),t_num,curr_path)
    
    try_next = list(dict_word_score.keys())
    
    return try_next
    
