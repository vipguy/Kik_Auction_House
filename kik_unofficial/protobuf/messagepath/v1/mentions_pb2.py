# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: messagepath/v1/mentions.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import kik_unofficial.protobuf.common_model_pb2 as common__model__pb2
import kik_unofficial.protobuf.common.v1_pb2 as model


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dmessagepath/v1/mentions.proto\x12\x15\x63ommon.messagepath.v1\x1a\x12\x63ommon_model.proto\x1a\x15\x63ommon/v1/model.proto\x1a\x19protobuf_validation.proto\"\x98\x01\n\x16MentionReplyAttachment\x12;\n\x12original_mentioner\x18\x01 \x01(\x0b\x32\x15.common.XiBareUserJidB\x08\x18\x01\xca\x9d%\x02\x08\x00\x12\x41\n\x15original_mentioner_v2\x18\x02 \x01(\x0b\x32\".common.v1.XiBareUserJidOrAliasJidBz\n\x19\x63om.kik.messagepath.modelZVgithub.com/kikinteractive/xiphias-model-common/generated/go/messagepath/v1;messagepath\xa2\x02\x04MPTHb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'messagepath.v1.mentions_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\031com.kik.messagepath.modelZVgithub.com/kikinteractive/xiphias-model-common/generated/go/messagepath/v1;messagepath\242\002\004MPTH'
  _MENTIONREPLYATTACHMENT.fields_by_name['original_mentioner']._options = None
  _MENTIONREPLYATTACHMENT.fields_by_name['original_mentioner']._serialized_options = b'\030\001\312\235%\002\010\000'
  _MENTIONREPLYATTACHMENT._serialized_start=127
  _MENTIONREPLYATTACHMENT._serialized_end=279
# @@protoc_insertion_point(module_scope)
