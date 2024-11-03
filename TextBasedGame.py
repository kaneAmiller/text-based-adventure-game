# Kane Miller

# Define the rooms and their connections in a dictionary
rooms = {
    "Garage": {'East': "Citadel of Ricks"},
    "Citadel of Ricks": {
        'North': "Giant's Land",
        'West': "Garage",
        'East': "Alien Hospital",
        'item': 'Plumbus',
        'South': "Blips and Chitz Arcade"
    },
    "Giant's Land": {
        'East': "Unity's planet",
        'South': 'Citadel of Ricks',
        'item': 'Battery'
    },
    "Unity's planet": {
        'West': "Giant's Land",
        'item': 'Portal Fluid'
    },
    "Blips and Chitz Arcade": {
        'North': "Citadel of Ricks",
        'East': 'Anatomy Park',
        'item': 'Meeseeks Box'
    },
    'Alien Hospital': {
        'West': "Citadel of Ricks",
        'North': "Jerry's Bedroom",
        'item': 'Interdimensional Cable-Box'
    },
    'Anatomy Park': {
        'West': "Blips and Chitz Arcade",
        'item': 'Micro-verse Battery'
    },
    "Jerry's Bedroom": {
        'South': 'Alien Hospital',
        'item': 'Evil Morty'
    }  # Boss fight
}

# Define a dictionary to map user input to directions
directions = {
    'north': 'North',
    'south': 'South',
    'east': 'East',
    'west': 'West',
    'go north': 'North',
    'go south': 'South',
    'go east': 'East',
    'go west': 'West'
}


def show_instructions():
    """
    Print the game's instructions and commands.
    """
    print("Rick and Morty Text Adventure Game")
    print("\nYou are Morty, and Rick has tasked you to collect all the parts necessary to build an interdimensional "
          "\nportal gun. However, there's a catch: the pieces are scattered throughout various dimensions and guarded by "
          "\naliens and creatures. You must travel through different rooms and collect the necessary items while avoiding "
          "\nRick's arch-nemesis, Evil Morty. For this game, the rooms are connected via stationary portals.")
    print("\nCollect all the parts to build your portal gun before fighting Evil morty.")
    print("\nMove commands: go South, go North, go East, go West")
    print("\nAdd to Inventory: get 'item name'\n")


def item_pickup(current_room, inventory, player_input):
    """
    Allow the player to pick up an item in the current room.
    """
    # Check if the current room has an item to pick up
    if 'item' in rooms[current_room]:
        item_name = rooms[current_room]['item']
        # If the item is Evil Morty and the player does not have the Portal Gun, the game is over
        if item_name == 'Evil Morty' and 'Portal Gun' not in inventory:
            print("Evil Morty killed you, Game Over!")
            return True
        # If the item is not in the inventory, add it and print a message
        if item_name not in inventory:
            if player_input == 'get ' + item_name:
                print('You picked up a', item_name)
                inventory.append(item_name)
                if len(inventory) >= 1:
                    print('Inventory:', inventory)
                    current_status(current_room, end_room)
                # If the inventory has all the required items, remove them from the rooms
                if len(inventory) == 7:
                    rooms[current_room].pop('item', None)
                    for room in rooms:
                        if 'item' in rooms[room] and rooms[room]['item'] != 'Evil Morty':
                            rooms[room].pop('item', None)
                    print("Congratulations, you have collected all the parts and built the portal gun!")
            else:
                print("You found a", item_name)
                print("Type 'get", item_name + "' to pick it up.")
                build_portalgun()
    return False


def build_portalgun():
    if len(inventory) >= 6:
        inventory.clear()
        print('Portal Gun has been built')
        inventory[:] = ['Portal Gun']
        for room in rooms.values():
            if 'item' in room and 'item' != "Evil Morty":
                del room['item']
    else:
        pass


def current_status(current_room, end_room):
    print('You are in the', current_room)
    if current_room is end_room and 'Portal Gun' in inventory:
        print("Congratulations, you have defeated Evil Morty and won the game!")
        return True  # Exit
    else:
        directions_list = list(rooms[current_room].keys())
        valid_directions = [direction for direction in directions_list if direction != 'item']
        if len(valid_directions) == 2:
            print('You can go', ', or '.join(valid_directions))
        elif len(valid_directions) >= 3:
            print('You can go', ', '.join(valid_directions[:-1]), ', or', valid_directions[-1])
        else:
            print('You can go', ''.join(valid_directions))


# This function takes the dictionary of rooms, the user's input 'move', and the current room name.
# if move (the key for rooms) is valid the new room will be assigned, if not: "You can't go that way." gets printed
def move_between_rooms(rooms, move, current_room):
    new_room = rooms[current_room].get(directions.get(move))
    if new_room:
        return new_room
    else:
        print("You can't go that way.")
        return current_room


if __name__ == '__main__':
    current_room = "Garage"  # Set the starting room
    end_room = "Jerry's Bedroom"  # Set the ending room
    inventory = []  # Initialize the inventory
    command = ''
    show_instructions()
    current_status(current_room, end_room)  # Print the starting room
    health = 100

    while command.lower() != 'exit':
        command = input()
        if command.lower() == 'exit':
            break  # Exit the game loop
        elif command.lower() in directions:
            new_room = move_between_rooms(rooms, command.lower(), current_room)
            if new_room != current_room:
                current_room = new_room
                build_portalgun()
                if item_pickup(current_room, inventory, command):
                    break  # Exit the game loop if player has died
                if current_status(current_room, end_room):
                    break  # Exit the game loop if game is over
        elif command.startswith('get '):
            if item_pickup(current_room, inventory, command):
                break  # Exit the game loop if player has died
        else:
            print("Invalid command.")
            continue
