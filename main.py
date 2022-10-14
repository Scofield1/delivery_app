from random import choice

#create a list of play options
option = ["Rock", "Paper", "Scissors"]

#assign a random play to the computer
CPU = choice(option)

#set player to False
player = False

while player == False:
#set player to True
    player = input("Rock, Paper, Scissors? ")
    if player == CPU:
        print("Tie!")
    elif player == "Rock":
        if CPU == "Paper":
            print("You lose!", CPU, "beats", player)
        else:
            print("You win!", player, "beats", CPU)
    elif player == "Paper":
        if CPU == "Scissors":
            print("You lose!", CPU, "beats", player)
        else:
            print("You win!", player, "beats", CPU)
    elif player == "Scissors":
        if CPU == "Rock":
            print("You lose...", CPU, "beats", player)
        else:
            print("You win!", player, "cut", CPU)
    else:
        print("That's not a valid play. Check your spelling!")
    #player was set to True, but we want it to be False so the loop continues
    player = False
    CPU = choice(option)