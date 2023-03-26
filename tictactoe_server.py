import grpc
from concurrent import futures
import time
import threading

import tic_tac_toe_pb2
import tic_tac_toe_pb2_grpc

class TicTacToeServicer(tic_tac_toe_pb2_grpc.TicTacToeServicer):

    def __init__(self):
        self.board = [""] * 9

    def StartGame(self, request, context):
        # Implement leader election and clock synchronization here
        return tic_tac_toe_pb2.StartGameResponse()

    def SetSymbol(self, request, context):
        self.board[request.cell - 1] = request.symbol
        
        return tic_tac_toe_pb2.SetSymbolResponse(winner=self.CheckWinner())

    def ListBoard(self, request, context):
        board_state = ", ".join(self.board)
        return tic_tac_toe_pb2.ListBoardResponse(board_state=board_state)

    def SetNodeTime(self, request, context):
        # Implement setting node time here
        return tic_tac_toe_pb2.SetNodeTimeResponse()

    def SetTimeOut(self, request, context):
        # Implement setting time-out here
        return tic_tac_toe_pb2.SetTimeOutResponse()
    
    def CheckWinner(self):
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
    

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tic_tac_toe_pb2_grpc.add_TicTacToeServicer_to_server(TicTacToeServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
