from room import Room
from player import Player
from world import World
from util import Stack

import os

import random
from ast import literal_eval

#method to create dictionary with directions and '?' to help guide us. 
def get_exit_dict(room):
    exits = room.get_exits()
    exit_dict = {}
    for e in exits:
        exit_dict[e] = '?'
    return exit_dict

#gets the  next unexplored direction
def get_next_direction(exit_dict):
    for direction in exit_dict.keys():
        if exit_dict[direction] == '?':
            return direction
    return None




# Load world
world = World()

cwd = os. getcwd() 
dir_name = cwd + '/projects/adventure/'


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()


player = Player(world.starting_room)

print ("Current Room:", player.current_room.id)


# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

path = Stack()
visited = {}
opposite_direction = {'n':'s', 's':'n', 'e':'w', 'w':'e'}


visited[player.current_room.id] = get_exit_dict(player.current_room)
while len(visited) < len(room_graph):

    #check to see if there are  no explored directions
    #if there are no explored directions then traverse into reverse direxction by 
    #going through the stack
    while get_next_direction(visited[player.current_room.id]) == None: 
        previous_dir = path.pop()
        traversal_path.append(previous_dir)
        player.travel(previous_dir)
    
    
    # find the next possible direction and traverse into that direction
    # push the opposite direction into stack so that we can go back later if we hit a dead end
    prior_room = player.current_room.id
    move = get_next_direction(visited[player.current_room.id]) 
    path.push(opposite_direction[move]) 
    player.travel(move)
    traversal_path.append(move)

    # print(traversal_path)
    # print ("Prior Room", prior_room)
    # print ("Current Room", player.current_room.id)

    visited[prior_room][move] = player.current_room.id
    if player.current_room.id not in visited:
        visited[player.current_room.id] = get_exit_dict(player.current_room)
    
    visited[player.current_room.id][opposite_direction[move]] = prior_room

    # print(len(visited), len(room_graph) - 1)
    # print("TP", traversal_path)

    # print ("Visited", visited)
    # inp = input("Press enter to continue(q to quit): ") 
    # if inp == 'quit' or inp == 'q':
    #     exit(0)
    # else:
    #     continue



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)



for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
