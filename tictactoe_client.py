import time
import grpc
import tic_tac_toe_pb2
import tic_tac_toe_pb2_grpc

def print_instructions():
    print("Commands:")
    print("  start-game")
    print("  set-symbol <cell> <symbol>")
    print("  list-board")
    print("  set-node-time <node_id> <hh:mm:ss>")
    print("  set-time-out <target> <minutes>")
    print("  exit")

def start_game(stub):
    client_time = time.time()
    response = stub.StartGame(tic_tac_toe_pb2.StartGameRequest(client_time=client_time))
    print("Game started.")

def check_winner(stub):
    board = stub.ListBoard(tic_tac_toe_pb2.ListBoardRequest()).board_state
    # Check for horizontal wins
    for i in range(0, 9, 3):
        if board[i] == board[i + 1] == board[i + 2] != "":
            return board[i]
    
    # Check for vertical wins
    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6] != "":
            return board[i]
    
    # Check for diagonal wins
    if board[0] == board[4] == board[8] != "":
        return board[0]
    if board[2] == board[4] == board[6] != "":
        return board[2]
    
    # Check for draw
    if "" not in board:
        return "draw"
    
    # No winner yet
    return ""

def main():
    global is_leader
    channel = grpc.insecure_channel("localhost:50051")
    stub = tic_tac_toe_pb2_grpc.TicTacToeStub(channel)

    print_instructions()

    while True:
        if is_leader:
            verdict = check_winner(stub)
            if verdict != "":
                if verdict == "draw":
                    print("It's a draw!")
                else:
                    print(f"{verdict} wins!")
                print("Restarting game...")
                # start_game(stub)

        try:
            command = input("\n> ").strip().split()

            if not command:
                continue

            if command[0].lower() == "start-game":
                response = stub.StartGame(tic_tac_toe_pb2.StartGameRequest())
                print("Game started.")

            elif command[0].lower() == "set-symbol":
                cell = int(command[1])
                symbol = command[2]
                while True:
                    response = stub.SetSymbol(tic_tac_toe_pb2.SetSymbolRequest(cell=cell, symbol=symbol))
                    if not bool(response.success):
                        print("Cell already taken. Try again.")
                        command = input("\n> Set-symbol ").strip().split()
                        cell = int(command[1])
                        symbol = command[2]
                    else:
                        break
                print("Symbol set.")

            elif command[0].lower() == "list-board":
                response = stub.ListBoard(tic_tac_toe_pb2.ListBoardRequest())
                print("Board state: ", response.board_state)

            elif command[0].lower() == "set-node-time":
                node_id = command[1]
                time = command[2]
                response = stub.SetNodeTime(tic_tac_toe_pb2.SetNodeTimeRequest(node_id=node_id, time=time))
                print(f"Node {node_id} time set to {time}.")

            elif command[0].lower() == "set-time-out":
                target = command[1]
                timeout_minutes = int(command[2])
                response = stub.SetTimeOut(tic_tac_toe_pb2.SetTimeOutRequest(target=target, timeout_minutes=timeout_minutes))
                print(f"Time-out for {target} set to {timeout_minutes} minutes.")

            elif command[0].lower() == "exit":
                print("Exiting...")
                break

            else:
                print("Invalid command.")
                print_instructions()

        except Exception as e:
            print("Error:", e)
            print_instructions()

if __name__ == "__main__":
    is_leader = False
    main()
