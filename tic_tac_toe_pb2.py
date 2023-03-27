# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tic_tac_toe.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11tic_tac_toe.proto\"#\n\x10StartGameRequest\x12\x0f\n\x07node_id\x18\x01 \x01(\x05\"&\n\x11StartGameResponse\x12\x11\n\tnode_time\x18\x01 \x01(\x05\"C\n\x15LeaderElectionRequest\x12\x17\n\x0fproposed_leader\x18\x01 \x01(\x05\x12\x11\n\tnode_list\x18\x02 \x03(\x05\"\x18\n\x16LeaderElectionResponse\"1\n\x16\x42\x65rkleyTimeSyncRequest\x12\x17\n\x0ftime_correction\x18\x01 \x01(\x05\"\x19\n\x17\x42\x65rkleyTimeSyncResponse\"A\n\x10SetSymbolRequest\x12\x0c\n\x04\x63\x65ll\x18\x01 \x01(\x05\x12\x0e\n\x06symbol\x18\x02 \x01(\t\x12\x0f\n\x07node_id\x18\x03 \x01(\x05\"$\n\x11SetSymbolResponse\x12\x0f\n\x07success\x18\x01 \x01(\x05\"#\n\x10ListBoardRequest\x12\x0f\n\x07node_id\x18\x01 \x01(\x05\"Y\n\x11ListBoardResponse\x12\x13\n\x0b\x62oard_state\x18\x01 \x03(\x05\x12\x16\n\x0e\x62oard_last_idx\x18\x02 \x01(\x05\x12\x17\n\x0f\x62oard_last_time\x18\x03 \x01(\x05\"3\n\x12SetNodeTimeRequest\x12\x0f\n\x07node_id\x18\x01 \x01(\x05\x12\x0c\n\x04time\x18\x02 \x01(\x05\"&\n\x13SetNodeTimeResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"5\n\x11SetTimeOutRequest\x12\x0f\n\x07node_id\x18\x01 \x01(\x05\x12\x0f\n\x07timeout\x18\x02 \x01(\x05\"%\n\x12SetTimeOutResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x15\n\x13\x43heckTimeOutRequest\"+\n\x14\x43heckTimeoutResponse\x12\x13\n\x0bleader_dead\x18\x01 \x01(\x08\x32\xee\x03\n\tTicTacToe\x12\x34\n\tStartGame\x12\x11.StartGameRequest\x1a\x12.StartGameResponse\"\x00\x12\x43\n\x0eLeaderElection\x12\x16.LeaderElectionRequest\x1a\x17.LeaderElectionResponse\"\x00\x12\x46\n\x0f\x42\x65rkleyTimeSync\x12\x17.BerkleyTimeSyncRequest\x1a\x18.BerkleyTimeSyncResponse\"\x00\x12\x34\n\tSetSymbol\x12\x11.SetSymbolRequest\x1a\x12.SetSymbolResponse\"\x00\x12\x34\n\tListBoard\x12\x11.ListBoardRequest\x1a\x12.ListBoardResponse\"\x00\x12:\n\x0bSetNodeTime\x12\x13.SetNodeTimeRequest\x1a\x14.SetNodeTimeResponse\"\x00\x12\x37\n\nSetTimeOut\x12\x12.SetTimeOutRequest\x1a\x13.SetTimeOutResponse\"\x00\x12=\n\x0c\x43heckTimeOut\x12\x14.CheckTimeOutRequest\x1a\x15.CheckTimeoutResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tic_tac_toe_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _STARTGAMEREQUEST._serialized_start=21
  _STARTGAMEREQUEST._serialized_end=56
  _STARTGAMERESPONSE._serialized_start=58
  _STARTGAMERESPONSE._serialized_end=96
  _LEADERELECTIONREQUEST._serialized_start=98
  _LEADERELECTIONREQUEST._serialized_end=165
  _LEADERELECTIONRESPONSE._serialized_start=167
  _LEADERELECTIONRESPONSE._serialized_end=191
  _BERKLEYTIMESYNCREQUEST._serialized_start=193
  _BERKLEYTIMESYNCREQUEST._serialized_end=242
  _BERKLEYTIMESYNCRESPONSE._serialized_start=244
  _BERKLEYTIMESYNCRESPONSE._serialized_end=269
  _SETSYMBOLREQUEST._serialized_start=271
  _SETSYMBOLREQUEST._serialized_end=336
  _SETSYMBOLRESPONSE._serialized_start=338
  _SETSYMBOLRESPONSE._serialized_end=374
  _LISTBOARDREQUEST._serialized_start=376
  _LISTBOARDREQUEST._serialized_end=411
  _LISTBOARDRESPONSE._serialized_start=413
  _LISTBOARDRESPONSE._serialized_end=502
  _SETNODETIMEREQUEST._serialized_start=504
  _SETNODETIMEREQUEST._serialized_end=555
  _SETNODETIMERESPONSE._serialized_start=557
  _SETNODETIMERESPONSE._serialized_end=595
  _SETTIMEOUTREQUEST._serialized_start=597
  _SETTIMEOUTREQUEST._serialized_end=650
  _SETTIMEOUTRESPONSE._serialized_start=652
  _SETTIMEOUTRESPONSE._serialized_end=689
  _CHECKTIMEOUTREQUEST._serialized_start=691
  _CHECKTIMEOUTREQUEST._serialized_end=712
  _CHECKTIMEOUTRESPONSE._serialized_start=714
  _CHECKTIMEOUTRESPONSE._serialized_end=757
  _TICTACTOE._serialized_start=760
  _TICTACTOE._serialized_end=1254
# @@protoc_insertion_point(module_scope)
