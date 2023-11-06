
import pygraphviz as pgv
from sequence_detector_hex import detect_all
from calculate_parameters import get_curr_path

from main_fsm import *


#definindo a classe da Maquina de Estados
class FiniteStateMachine:

    def __init__(self, initials, finals, states, curr_path):
        self.__initials = initials
        self.__finals = finals
        self.__states = states
        self.__current_position = 'not_initialized'
        self.__transitions = {}
        self.__last_state = 'not_initialized'
        self.__way = []
        self.curr_path = curr_path

        self.__initials_list = self.__initials.keys()

        for element in states:
            self.__transitions[element] = {}

    def get_transitions(self):
        for transition in self.__transitions:
            print(transition, '-->', self.__transitions.get(transition))
        return self.__transitions

    def initialize_pointer(self, starter, t_num):
        if starter in self.__initials_list:
            self.__current_position = self.__states.index(starter)
            self.__last_state = self.get_current_state()
            self.__way.append(self.get_current_state())
            #print(t_num, "Initial State: ", self.__states[self.__current_position])
            return True
        else:
            self.__last_state = self.get_current_state()
            print("Can't initialize by this state")
            return False

    def reset_state(self):
        self.__current_position = 'not_initialized'
        self.__last_state = 'not_initialized'
        self.__way = []

    def get_current_position(self):
        if self.__current_position == 'not_initialized':
            print('Position is not initialized')
        else:
            return self.__current_position

    def get_current_state(self):
        if self.__current_position == 'not_initialized':
            print('Position is not initialized')
        else:
            return self.__states[self.__current_position]

    def add_transition(self, state1, state2):
        if state2 in self.__transitions[state1]:
            self.__transitions[state1][state2] = self.__transitions[state1][state2] + 1
        else:
            self.__transitions[state1][state2] = 1

    def change_state(self, where_to,t_num):
        if self.__current_position == 'not_initialized':
            print('Position is not initialized')
            return False
        else:
            possible = self.__transitions[self.__states[self.__current_position]]
            if where_to in possible:
                self.__last_state = self.get_current_state()
                self.__current_position = self.__states.index(where_to)
                #print(t_num, "New State: ", self.__states[self.__current_position])
                self.__way.append(self.get_current_state())
                return True
            else:
                self.__last_state = self.get_current_state()
                print('Mudança não permitida')
                return False

    def get_next_states(self):
        if self.__current_position == 'not_initialized':
            return self.__initials
        else:
            return self.__transitions.get(self.get_current_state())

    def get_last_state(self):
        return self.__last_state

    def get_way(self):
        return self.__way

    def plot_machine(self,name):
        data = self.__transitions

        A = pgv.AGraph(directed=True,rankdir="LR")

        for key in data.keys():
            if key in self.__initials and key in self.__finals:
                A.add_node(key,color='green')
            else:
                if key in self.__initials:
                    A.add_node(key,color='blue')
                elif key in self.__finals:
                    A.add_node(key,color='red')
                else:
                    A.add_node(key)

        for node in data:
            for nbr in data[node]:
                A.add_edge(node, nbr, label=data[node].get(nbr))
        A.layout(prog="dot")  # layout with dot
        file_name = self.curr_path + 'plot/' + str(name) + '.png'
        A.draw(file_name)  # write to file

    def __str__(self):
        if self.__current_position == 'not_initialized':
            to_print = 'States: ' + str(self.__states) + '\n' + 'Current Position: ' + str(self.__current_position) + '\n' + 'Current State: ' + str(self.__current_position)
        else:
            to_print = 'States: ' + str(self.__states) + '\n' + 'Current Position: ' + str(self.__current_position) + '\n' + 'Current State: ' + str(self.__states[self.__current_position])
        return to_print

def find_states(seq_list):
    initial_list = {}
    end_list = []

    for state in seq_list:
        if state[0] in initial_list.keys():
            initial_list[state[0]] = initial_list[state[0]] + 1
        else:
            initial_list[state[0]] = 1
        end_list.append(state[len(state)-1])

    #initial_list = [*set(initial_list)]
    #initial_list.sort()
    end_list = [*set(end_list)]
    end_list.sort()

    all_states = []

    for seq in seq_list:
        for i in seq:
            all_states.append(i)

    all_states = [*set(all_states)]
    all_states.sort()

    return initial_list, end_list, all_states

def find_transition(seq_list, all_states,machine):

    transitions2 = {}

    for element in all_states:
        transitions2[element] = {}

    for seq in seq_list:
        for i in range(len(seq)-1):
            element = seq[i]
            next_element = seq[i+1]
            machine.add_transition(element, next_element)

if __name__ == '__main__':

    curr_path = get_curr_path() 
    path = './datasets/training/0full2.xlsx'
    seq_list = detect_all(path, 0, 1)
    
    print(seq_list)

    initial_list, end_list, all_states = find_states(seq_list)

    machine = FiniteStateMachine(initials = initial_list, finals = end_list, states = all_states, curr_path = curr_path)

    find_transition(seq_list, all_states, machine)

    machine.get_transitions()

    print('############')
    print(machine)
    machine.plot_machine('teste_n0')
    print('############')



    # # #
#     print('next: ', machine.get_next_states())
#     print('last: ', machine.get_last_state())

#     # last_state = machine.get_last_state()
#     # next_states = machine.get_next_states()

#     # process_failure(1, 'e', last_state, next_states, 1, 122)

#     print('##')
#     machine.change_state('5',120.1)
#     print('next: ', machine.get_next_states())
#     print('last: ', machine.get_last_state())
#     print('##')
#     machine.change_state('e',120.1)
#     print('next: ', machine.get_next_states())
#     print('last: ', machine.get_last_state())

#     last_state = machine.get_last_state()
#     next_states = machine.get_next_states()

#     process_failure(1, 'e', last_state, next_states, 1, 122)


# #     machine.change_state('8')
# #     print(machine.get_current_position())
# #     print(machine.get_current_state())ad
# #     machine.change_state('15')
# #     print(machine.get_current_position())
# #     print(machine.get_current_state())
# #     machine.change_state('51')
# #     print(machine.get_current_position())
# #     print(machine.get_current_state())


# #     # machine.change_state()
# #     # machine.current_state = 1
# #     # print(machine.current_state)
# #     # print(machine.get_current_state())
# #     # machine.current_state = 5
# #     # print(machine.current_state)
# #     # print(machine.get_current_state())

# #     # machine._FiniteStateMachine__current_state = 999
# #     # print(machine.current_state)
# #     # print(machine.get_current_state())


