import time
from concurrent import futures
import grpc
import tic_tac_toe_pb2
import tic_tac_toe_pb2_grpc
import threading

class TicTacToeNode:
    def __init__(self, channels, id):
        self.id = id
        self.time_correction = 0
        self.leader = None
        self.timeout_leader = None
        self.timeout_player = None
        self.node_last_seen_at = [time.time() if i != self.client.id else None for i in range(3)]
        self.stubs = []
        for i, channel in enumerate(channels):
            if i == id:
                self.stubs.append(None)
            else:
                self.stubs.append(tic_tac_toe_pb2_grpc.TicTacToeStub(channel))

    def start_game(self):
        # Do Barclay time sync here
        # Do democracy here
        return self.stub.StartGame(tic_tac_toe_pb2.StartGameRequest())

    def set_symbol(self, cell, symbol):
        # send to leader, it will check if it is correct and returns the success of the move
        while True:
            response = self.stubs[self.leader].SetSymbol(tic_tac_toe_pb2.SetSymbolRequest(cell=cell, symbol=symbol))
            if not bool(response.success):
                print("Cell already taken. Try again.")
                command = input("\n> Set-symbol ").strip().split()
                cell = int(command[1])
                symbol = command[2]
            else:
                break
        print("Symbol set.")

    def list_board(self):
        return self.stubs[self.leader].ListBoard(tic_tac_toe_pb2.ListBoardRequest())

    def set_node_time(self, node_id, settime):
        if node_id == self.id:
            self.time = settime
        elif self.leader == self.id:
            response = self.stubs[node_id].SetNodeTime(tic_tac_toe_pb2.SetNodeTimeRequest(node_id=node_id, time=settime))
            print(f"Node {node_id} time set to {settime}.")
        else:
            print("Only the leader can set the time of other nodes.")

    def set_timeout(self, target, timeout_minutes):
        if self.leader == self.id:
            if target == "players":
                self.timeout_player = timeout_minutes
            else:
                for i, stub in enumerate(self.stubs):
                    if i != self.id:
                        stub.SetTimeOut(tic_tac_toe_pb2.SetTimeOutRequest(timeout=timeout_minutes))
        else:
            print("Only the leader can set timeouts.")
    

class TicTacToeServicer(tic_tac_toe_pb2_grpc.TicTacToeServicer):
    def __init__(self, client):
        self.client = client

    def init_as_leader(self):
        self.board = [""] * 9

    def register_interactions(self, node_id):
        self.client.node_last_seen_at[node_id] = time.time() + self.client.time_correction

    def check_winner(self):
        # Check for horizontal wins
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i + 1] == self.board[i + 2] != "":
                return self.board[i]
        # Check for vertical wins
        for i in range(3):
            if self.board[i] == self.board[i + 3] == self.board[i + 6] != "":
                return self.board[i]
        # Check for diagonal wins
        if self.board[0] == self.board[4] == self.board[8] != "":
            return self.board[0]
        if self.board[2] == self.board[4] == self.board[6] != "":
            return self.board[2]
        # Check for draw
        if "" not in self.board:
            return "draw"
        # No winner yet
        return ""

    def SetSymbol(self, request, context):
        if self.board[request.cell - 1] != "":
            self.register_interactions(request.node_id)
            return tic_tac_toe_pb2.SetSymbolResponse(success=0)
        self.board[request.cell - 1] = request.symbol
        self.register_interactions(request.node_id) 
        
        winner = self.check_winner()
        if winner != "":
            print("Game over. Winner is", winner)
            self.client.start_game()
    
        return tic_tac_toe_pb2.SetSymbolResponse(success=1)
    
    def ListBoard(self, request, context):
        self.register_interactions(request.node_id)
        return tic_tac_toe_pb2.ListBoardResponse(board_state=self.board)
    
    def SetNodeTime(self, request, context):
        self.client.time = request.time
        self.register_interactions(request.node_id)
        return tic_tac_toe_pb2.SetNodeTimeResponse(success=1)
    
    def SetTimeOut(self, request, context):
        self.client.timeout_leader = request.timeout
        self.register_interactions(request.node_id)
        return tic_tac_toe_pb2.SetTimeOutResponse(success=1)
    
    def CheckTimeout(self, request, context):
        leader_dead = False
        if self.client.node_last_seen_at[self.client.leader] - time.time() > self.client.timeout_leader:
            leader_dead = True
        return tic_tac_toe_pb2.CheckTimeoutResponse(leader_dead=leader_dead)


def check_timeout():
    while True:
        for i, node in enumerate(client.node_last_seen_at):
            if node is not None and client.id != client.leader and time.time() - node > client.timeout_leader:
                node_id = [node_id for node_id in [0,1,2] if node_id not in [client.id, client.leader]][0]
                response = client.stubs[node_id].CheckTimeout(tic_tac_toe_pb2.CheckTimeoutRequest())
                if response.leader_dead:
                    print(f"Leader {client.leader} timed out. Restarting the game")
                    client.start_game()
            elif node is not None and client.id == client.leader and time.time() - node > client.timeout_player:
                print(f"Player {i} timed out. Restarting the game")
                client.start_game()


channels = []
client = TicTacToeNode(channels, id)
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), client=client)
server.add_insecure_port(channels[id])
server.start()
server.wait_for_termination()
threading.Thread(target=check_timeout).start()

while True:

    command = input("\n> ").strip().split()
    if command[0] == "start-game":
        # Needs to be checked after democracy implemented
        response = client.start_game()
        print(f"Game started. You are player {response.player_id}.")

    elif command[0] == "set-symbol":
        cell = int(command[1])
        symbol = command[2]
        client.set_symbol(cell, symbol)

    elif command[0] == "list-board":
        response = client.list_board()
        print(response.board_state)

    elif command[0] == "set-node-time":
        node_id = int(command[1])
        settime = int(command[2])
        client.set_node_time(node_id, settime)

    elif command[0] == "set-timeout":
        target = command[1]
        timeout_minutes = int(command[2])
        client.set_timeout(target, timeout_minutes)

    elif command[0] == "exit":
        break
    else:
        print("Unknown command.")