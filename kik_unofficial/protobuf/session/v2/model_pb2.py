# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: session/v2/model.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16session/v2/model.proto\x12\x11\x63ommon.session.v2\x1a\x1fgoogle/protobuf/timestamp.proto\"\x8c\x01\n\x0cSessionToken\x12\x34\n\x05token\x18\x01 \x01(\x0b\x32%.common.session.v2.SessionToken.Token\x12*\n\x06\x65xpiry\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x1a\x1a\n\x05Token\x12\x11\n\traw_value\x18\x01 \x01(\x0c\x42}\n\x16\x63om.kik.gen.session.v2ZNgithub.com/kikinteractive/xiphias-model-common/generated/go/session/v2;session\xa2\x02\x12KPBCommonSessionV2b\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'session.v2.model_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\026com.kik.gen.session.v2ZNgithub.com/kikinteractive/xiphias-model-common/generated/go/session/v2;session\242\002\022KPBCommonSessionV2'
  _SESSIONTOKEN._serialized_start=79
  _SESSIONTOKEN._serialized_end=219
  _SESSIONTOKEN_TOKEN._serialized_start=193
  _SESSIONTOKEN_TOKEN._serialized_end=219
# @@protoc_insertion_point(module_scope)
