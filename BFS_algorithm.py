import sys
import math
from collections import deque
import time
#from pkg_resources import resources

class PuzzleState:

    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        if n*n < len(config) or n < 2:
            raise Exception("length of config is not correct");
        else:
            self.config    = config;
            self.n         = n;
            self.parent    = parent;
            self.action    = action;
            self.cost      = cost;
            self.dimension = n;
            self.children  = deque([]);
            li=[];
            self.calc_blank(li,self.config,n);
            self.blank_row = li.__getitem__(0);
            self.blank_col = li.__getitem__(1);
            '''''
                for i, item in enumerate(self.config):
                    if item == 0:
                        #self.blank_row = int(i / self.n);
                        #self.blank_col = int(i % self.n);
                        self.blank_row=0;
                        self.blank_col=0;
                        break;
                        '''
    def calc_blank(self, blank_list,con ,n):
        for i in range(0,len(con),1):
            if int(con.__getitem__(i)) == 0:
                blank_list.append(int(i / self.n));
                blank_list.append(int(i % self.n));

    def get_parent(self):
        return self.parent;
    def get_config(self):
        return self.config;

    def display(self):
        for i in range(self.n):
            line = [];
            offset = i*self.n;
            for j in range(self.n):
                line.append(self.config[offset+j]);

            print(line);

    def move_left(self):
        if self.blank_col == 0:
            return None;
        else:
            self.blank_index = self.blank_row * self.n +self.blank_col;
            target      = self.blank_index - 1;
            new_config  = list(self.config);
            new_config[self.blank_index], new_config[target] = new_config[target],  new_config[self.blank_index];

        return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost+1)

    def move_Right(self):
        if self.blank_col == self.n - 1:
            return None;
        else:
            self.blank_index = self.blank_row * self.n + self.blank_col;
            target = self.blank_index + 1;
            new_config = list(self.config);
            new_config[self.blank_index], new_config[target] = new_config[target], new_config[self.blank_index];

        return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost + 1)

    def move_up(self):
        if self.blank_row == 0:
            return None;
        else:
            self.blank_index = self.blank_row * self.n + self.blank_col;
            target = self.blank_index - self.n;
            new_config = list(self.config);
            new_config[self.blank_index], new_config[target] = new_config[target], new_config[self.blank_index];

        return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost + 1)

    def move_down(self):
        if self.blank_row == self.n -1:
            return None;
        else:
            self.blank_index = self.blank_row * self.n + self.blank_col;
            target = self.blank_index + self.n;
            new_config = list(self.config);
            new_config[self.blank_index], new_config[target] = new_config[target], new_config[self.blank_index];

        return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1)

    def expand(self):
        # expand in UDLR order #
        if len(self.children) == 0:
            up_child = self.move_up();
            if up_child is not None:
                self.children.append(up_child);

            down_child = self.move_down();
            if down_child is not None:
                self.children.append(down_child);

            left_child = self.move_left();
            if left_child is not None:
                self.children.append(left_child);

            right_child = self.move_Right();
            if right_child is not None:
                self.children.append(right_child);
        return self.children;


def bfs_search(initial_state):
    frontier = deque([initial_state]);
    explored = set([])
    counter=0

    while frontier:
        state = frontier.popleft()
        explored.add(state)

        if test_goal(state):
            print("max Search depth->",frontier[len(frontier)-1].cost)
            print("Nodes Expanded = ", counter)
            return state

        state.expand()
        counter +=1
        exTest=False
        frTest=False
        for child in state.children:
            #child.display()
            for exChild in explored:
                if is_states_eq(exChild , child):
                    exTest = False
                    break
                else:
                    exTest = True
            if frontier:
                for frChild in list(frontier):
                    if is_states_eq(frChild , child):
                        frTest = False
                        break
                    else:
                        frTest = True
            else:
                if exTest == True:
                    frontier.append(child)
            #print(exTest,"*******************",frTest)
            if exTest == True and frTest == True:
                frontier.append(child)
    return False



def test_goal(state):
    for i in range(0,len(state.config),1):
        if i != int(state.config[i]):
            return False;
    return True;

def actions(state):
    moves = [];
    temp =state;
    moves.append(temp.action);
    while temp.action !='Initial':
        moves.append(temp.get_parent().action);
        temp =temp.get_parent();
    moves.remove("Initial");
    moves.reverse();
    return moves;

def is_states_eq(state1 , state2):
    for i in range(len(state1.config)):
        if state1.config[i] != state2.config[i]:
            return False

    return True


##################################################################
######################### Main Execution #########################
##################################################################

con1 = "1,0,2,3,4,5,6,7,8"
new_con1=con1.split(",")
state1 = PuzzleState(new_con1,3)

con2 = "1,2,5,3,4,0,6,7,8"
new_con2=con2.split(",")
state2 = PuzzleState(new_con2,3)

result= bfs_search(state2)
#result.display()
act = actions(result)
print(act)
print("cost_of_path: ",result.cost)
print("Search Depth", result.cost)



