# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chat.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nchat.proto\x12\x04\x63hat\"\x18\n\x08Username\x12\x0c\n\x04name\x18\x01 \x01(\t\"-\n\x07Unreads\x12\x11\n\terrorFlag\x18\x01 \x01(\x08\x12\x0f\n\x07unreads\x18\x02 \x01(\t\"\x16\n\x07Payload\x12\x0b\n\x03msg\x18\x01 \x01(\t\"\x1e\n\x0b\x42oolPayload\x12\x0f\n\x07\x62oolVal\x18\x01 \x01(\x08\"p\n\x0bSendRequest\x12\x1e\n\x06sender\x18\x01 \x01(\x0b\x32\x0e.chat.Username\x12!\n\trecipient\x18\x02 \x01(\x0b\x32\x0e.chat.Username\x12\x1e\n\x07sentMsg\x18\x03 \x01(\x0b\x32\r.chat.Payload2\xc7\x02\n\x04\x43hat\x12\x31\n\x0eSignInExisting\x12\x0e.chat.Username\x1a\r.chat.Unreads\"\x00\x12*\n\x07\x41\x64\x64User\x12\x0e.chat.Username\x1a\r.chat.Unreads\"\x00\x12*\n\x04Send\x12\x11.chat.SendRequest\x1a\r.chat.Payload\"\x00\x12+\n\x06Listen\x12\x0e.chat.Username\x1a\r.chat.Payload\"\x00\x30\x01\x12)\n\x06Logout\x12\x0e.chat.Username\x1a\r.chat.Payload\"\x00\x12\x31\n\nIsLoggedIn\x12\x0e.chat.Username\x1a\x11.chat.BoolPayload\"\x00\x12)\n\x06\x44\x65lete\x12\x0e.chat.Username\x1a\r.chat.Payload\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chat_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _USERNAME._serialized_start=20
  _USERNAME._serialized_end=44
  _UNREADS._serialized_start=46
  _UNREADS._serialized_end=91
  _PAYLOAD._serialized_start=93
  _PAYLOAD._serialized_end=115
  _BOOLPAYLOAD._serialized_start=117
  _BOOLPAYLOAD._serialized_end=147
  _SENDREQUEST._serialized_start=149
  _SENDREQUEST._serialized_end=261
  _CHAT._serialized_start=264
  _CHAT._serialized_end=591
# @@protoc_insertion_point(module_scope)
