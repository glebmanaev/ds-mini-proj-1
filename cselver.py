import sys
import time
import datetime
from concurrent import futures
import grpc
import tic_tac_toe_pb2
import tic_tac_toe_pb2_grpc
import threading

class TicTacToeNode:
    def __init__(self, channels, id):
        self.id = id
        self.time_correction = 0
        self.first_player = False
        self.leader = None
        self.timeout_leader = None
        self.timeout_player = None
        self.node_last_seen_at = [time.time() if i != self.id else None for i in range(3)]
        self.stubs = []
        for i, channel in enumerate(channels):
            if i == id:
                self.stubs.append(None)
            else:
                self.stubs.append(tic_tac_toe_pb2_grpc.TicTacToeStub(grpc.insecure_channel(channel)))

    def register_interactions(self, node_id):
        self.node_last_seen_at[node_id] = time.time() + self.client.time_correction

    def start_game(self):
        # Do Barclay time sync here
        print(f"Game started. You are player {self.id}.")
        print("Doing time sync with other nodes...")
        if self.first_player:
            node_times = [time.time()]*3
            for i in range(3):
                if i != self.id:
                     response = self.stubs[i].StartGame(tic_tac_toe_pb2.StartGameRequest(node_id=self.id))
                     node_times[i] = response.node_time
            self.time_correction = sum(node_times)/3 - node_times[self.id]
            for i in range(3):
                if i != self.id:
                     self.stubs[i].BerkleyTimeSync(tic_tac_toe_pb2.BerkleyTimeSyncRequest(time_correction=sum(node_times)/3 - node_times[i]))
        print(f"Time sync done. Correction: {self.time_correction} seconds.")
        
        # Do leader election here
        print("Doing leader election...")
        if self.first_player:
            self.stubs[(self.id + 1) % 3].LeaderElection(tic_tac_toe_pb2.LeaderElectionRequest(proposed_leader=None, node_list=[self.id]))
        while self.leader is None:
            time.sleep(1)
        print("The leader is", self.client.leader)

    def set_symbol(self, cell, symbol):
        # send to leader, it will check if it is correct and returns the success of the move
        while True:
            response = self.stubs[self.leader].SetSymbol(tic_tac_toe_pb2.SetSymbolRequest(cell=cell, symbol=symbol, node_id=self.id))
            self.register_interactions(self.leader)
            if not bool(response.success):
                print("Cell already taken. Try again.")
                command = input("\n> Set-symbol ").strip().split()
                cell = int(command[1])
                symbol = command[2]
            else:
                break
        print("Symbol set.")

    def list_board(self):
        response =  self.stubs[self.leader].ListBoard(tic_tac_toe_pb2.ListBoardRequest(node_id=self.id))
        self.register_interactions(self.leader)
        board = response.board_state
        timestamp = datetime.datetime.fromtimestamp(response.board_last_time).strftime('%H:%M:%S')
        board[response.board_last_idx] = f"{board[response.board_last_idx]}: {timestamp}"
        print("Board state: ", )

    def set_node_time(self, node_id, settime):
        dt = datetime.combine(datetime.today(), datetime.strptime(settime, '%H:%M:%S').time())
        settime = dt.timestamp() # could be a problem if the node is not in the same timezone
        if node_id == self.id:
            self.time = settime
        elif self.leader == self.id:
            response = self.stubs[node_id].SetNodeTime(tic_tac_toe_pb2.SetNodeTimeRequest(node_id=self.id, time=settime))
            self.register_interactions(node_id)
            print(f"Node {node_id} time set to {settime}.")
        else:
            print("Only the leader can set the time of other nodes.")

    def set_timeout(self, target, timeout_minutes):
        if self.leader == self.id:
            if target == "players":
                self.timeout_player = timeout_minutes * 60
            else:
                for i, stub in enumerate(self.stubs):
                    if i != self.id:
                        stub.SetTimeOut(tic_tac_toe_pb2.SetTimeOutRequest(timeout=timeout_minutes, node_id=self.id))
                        self.register_interactions(i)
        else:
            print("Only the leader can set timeouts.")
    

class TicTacToeServicer(tic_tac_toe_pb2_grpc.TicTacToeServicer):
    def __init__(self):
        self.client = client
        self.time_differneces = {}

    def init_as_leader(self):
        self.board = [""] * 9
        self.board_last_idx = None
        self.board_last_time = None

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
    
    def StartGame(self, request, context):
        self.client.start_game()
        return tic_tac_toe_pb2.StartGameResponse(node_time=time.time())

    def BerkleyTimeSync(self, request, context):
        self.client.time_correction = request.time_correction
        return tic_tac_toe_pb2.BerkleyTimeSyncResponse()
    
    def LeaderElection(self, request, context):
        if request.proposed_leader is None:
            proposed_leader = None
            if self.clinet.first_player:
                proposed_leader = max(request.node_list)
            self.client.stubs[(self.client.id + 1) % 3].LeaderElection(tic_tac_toe_pb2.LeaderElectionRequest(proposed_leader=proposed_leader,node_list=request.node_list + [self.client.id]))
        else:
            self.client.leader = request.proposed_leader
            self.client.stubs[(self.client.id + 1) % 3].LeaderElection(tic_tac_toe_pb2.LeaderElectionRequest(proposed_leader=request.proposed_leader,node_list=request.node_list + [self.client.id]))
            if self.client.leader == self.client.id:
                self.init_as_leader()
        return tic_tac_toe_pb2.LeaderElectionResponse()

    def SetSymbol(self, request, context):
        if self.board[request.cell - 1] != "":
            self.register_interactions(request.node_id)
            return tic_tac_toe_pb2.SetSymbolResponse(success=0)
        self.board[request.cell - 1] = request.symbol
        self.board_last_idx = request.cell - 1
        self.board_last_time = time.time() + self.client.time_correction
        self.register_interactions(request.node_id) 
        
        winner = self.check_winner()
        if winner != "":
            print("Game over. Winner is", winner)
            self.client.start_game()
    
        return tic_tac_toe_pb2.SetSymbolResponse(success=1)
    
    def ListBoard(self, request, context):
        self.register_interactions(request.node_id)
        return tic_tac_toe_pb2.ListBoardResponse(board_state=self.board, board_last_idx=self.board_last_idx, board_last_time=self.board_last_time)
    
    def SetNodeTime(self, request, context):
        self.client.time = request.time
        self.register_interactions(request.node_id)
        return tic_tac_toe_pb2.SetNodeTimeResponse(success=1)
    
    def SetTimeOut(self, request, context):
        self.client.timeout_leader = request.timeout*60
        self.register_interactions(request.node_id)
        return tic_tac_toe_pb2.SetTimeOutResponse(success=1)
    
    def CheckTimeout(self, request, context):
        leader_dead = False
        if self.client.node_last_seen_at[self.client.leader] - time.time() > self.client.timeout_leader:
            leader_dead = True
        return tic_tac_toe_pb2.CheckTimeoutResponse(leader_dead=leader_dead)


def check_timeout():
    while True:
        if client.leader is not None:
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


def run_server(client, channels, node_id):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server.add_insecure_port(channels[node_id])
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

node_id = int(sys.argv[1])

channels = ["[::]:20048", "[::]:20049", "[::]:20050"]
client = TicTacToeNode(channels, node_id)

threading.Thread(target=check_timeout).start()
threading.Thread(target=run_server(client, channels, node_id)).start()
#threading.Thread(target=server.wait_for_termination()).start()

# run_server(client, channels, node_id)

while True:
    command = input("\n> ").strip().split()
    if command[0] == "start-game":
        client.first_player = True
        response = client.start_game()

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