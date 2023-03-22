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

def main():
    channel = grpc.insecure_channel("localhost:50051")
    stub = tic_tac_toe_pb2_grpc.TicTacToeStub(channel)

    print_instructions()

    while True:
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
                response = stub.SetSymbol(tic_tac_toe_pb2.SetSymbolRequest(cell=cell, symbol=symbol))
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
    main()
