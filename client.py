def set_symbol(cell, symbol):
    cell = cell.replace(',','')
    # request

def list_board():
    # send request
    # print response
    pass

def set_node_time(node, time):
    # В душе не понимаю, что тут должно быть
    pass

def clock_sync():
    pass

def election():
    pass

def check_win():
    pass

def set_timeout(target, time):
    # request
    pass

# Time-outs calculation can be done in a separate thread, using threading 

def main():
    while True:
        clock_sync()
        leader = election() # Boolean

        command = input('')

        if "Set-symbol" in command:
            cell, symbol = command.split()[1:]
            set_symbol(cell, symbol)
            if leader:
                check_win()

        elif "List-board" in command:
            list_board()

        elif "Set-node-time" in command:
            node, time = command.split()[1:]
            set_node_time(node, time)

        elif "Set-time-out" in command:
            target, time = command.split()[1:]
            set_timeout(target, time)

        # Somehow monitor the game end and restart the game | do the same in timeouts thread
    
    