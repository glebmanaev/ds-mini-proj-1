import grpc
from concurrent import futures
import time
import threading

import tic_tac_toe_pb2
import tic_tac_toe_pb2_grpc

class TicTacToeServicer(tic_tac_toe_pb2_grpc.TicTacToeServicer):

    def __init__(self):
        self.board = [""] * 9
        self.time_differneces = {}
        self.new_times = {}

    def StartGame(self, request, context):
        # Implement Berkely algorithm here
        server_time = time.time()
        self.time_differneces[request.node_id] = server_time - request.client_time
        while len(self.time_differneces) < 3:
            pass
        average_time = sum(self.time_differneces.values()) / len(self.time_differneces)
        corrected_time = time.time() + average_time
        return tic_tac_toe_pb2.StartGameResponse(synced_time=corrected_time)

    def SetSymbol(self, request, context):
        if self.board[request.cell - 1] != "":
            return tic_tac_toe_pb2.SetSymbolResponse(success=0)
        self.board[request.cell - 1] = request.symbol    
        return tic_tac_toe_pb2.SetSymbolResponse(success=1)

    def ListBoard(self, request, context):
        board_state = ", ".join(self.board)
        return tic_tac_toe_pb2.ListBoardResponse(board_state=board_state)

    def SetNodeTime(self, request, context):
        # Implement setting node time here
        self.new_times[request.node_id] = request.time
        while self.new_times[request.node_id]:
            pass
        return tic_tac_toe_pb2.SetNodeTimeResponse()

    def GetNodeTime(self, request, context):
        # Implement setting node time here
        new_time = self.new_times[request.node_id]
        if new_time:
            self.new_times[request.node_id] = False
            return tic_tac_toe_pb2.GetNodeTimeResponse(time=new_time, updated=True)
        return tic_tac_toe_pb2.GetNodeTimeResponse(time=0, updated=False)
    
    def SetTimeOut(self, request, context):
        # Implement setting time-out here
        return tic_tac_toe_pb2.SetTimeOutResponse()
    

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tic_tac_toe_pb2_grpc.add_TicTacToeServicer_to_server(TicTacToeServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
