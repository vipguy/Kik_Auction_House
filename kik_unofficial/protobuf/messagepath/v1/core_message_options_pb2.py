# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: messagepath/v1/core_message_options.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)messagepath/v1/core_message_options.proto\x12\x15\x63ommon.messagepath.v1\x1a google/protobuf/descriptor.proto\"\x87\x01\n\x1c\x43oreMessageOriginRestriction\x12H\n\x04\x64\x65ny\x18\x01 \x03(\x0e\x32:.common.messagepath.v1.CoreMessageOriginRestriction.Origin\"\x1d\n\x06Origin\x12\n\n\x06MOBILE\x10\x00\x12\x07\n\x03\x42OT\x10\x01:p\n\x12origin_restriction\x12\x1d.google.protobuf.FieldOptions\x18\xdb\xd3\x04 \x01(\x0b\x32\x33.common.messagepath.v1.CoreMessageOriginRestrictionBs\n\x19\x63om.kik.messagepath.modelZVgithub.com/kikinteractive/xiphias-model-common/generated/go/messagepath/v1;messagepath')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'messagepath.v1.core_message_options_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
  google_dot_protobuf_dot_descriptor__pb2.FieldOptions.RegisterExtension(origin_restriction)

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\031com.kik.messagepath.modelZVgithub.com/kikinteractive/xiphias-model-common/generated/go/messagepath/v1;messagepath'
  _COREMESSAGEORIGINRESTRICTION._serialized_start=103
  _COREMESSAGEORIGINRESTRICTION._serialized_end=238
  _COREMESSAGEORIGINRESTRICTION_ORIGIN._serialized_start=209
  _COREMESSAGEORIGINRESTRICTION_ORIGIN._serialized_end=238
# @@protoc_insertion_point(module_scope)
