# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: messagepath/v1/visibility_rules.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import kik_unofficial.protobuf.common_model_pb2 as common__model__pb2
import kik_unofficial.protobuf.common.v1_pb2 as model


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%messagepath/v1/visibility_rules.proto\x12\x15\x63ommon.messagepath.v1\x1a\x12\x63ommon_model.proto\x1a\x15\x63ommon/v1/model.proto\x1a\x19protobuf_validation.proto\"\xbd\x02\n\x19VisibilityRulesAttachment\x12\x32\n\tinitiator\x18\x01 \x01(\x0b\x32\x15.common.XiBareUserJidB\x08\x18\x01\xca\x9d%\x02\x08\x00\x12\x38\n\x0cinitiator_v2\x18\x04 \x01(\x0b\x32\".common.v1.XiBareUserJidOrAliasJid\x12$\n\x1c\x64rop_if_initiator_not_friend\x18\x02 \x01(\x08\x12\x43\n\x04rule\x18\x03 \x01(\x0e\x32\x35.common.messagepath.v1.VisibilityRulesAttachment.Rule\"G\n\x04Rule\x12\x1d\n\x19USE_SENDER_FOR_VISIBILITY\x10\x00\x12 \n\x1cUSE_INITIATOR_FOR_VISIBILITY\x10\x01\x42z\n\x19\x63om.kik.messagepath.modelZVgithub.com/kikinteractive/xiphias-model-common/generated/go/messagepath/v1;messagepath\xa2\x02\x04MPTHb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'messagepath.v1.visibility_rules_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\031com.kik.messagepath.modelZVgithub.com/kikinteractive/xiphias-model-common/generated/go/messagepath/v1;messagepath\242\002\004MPTH'
  _VISIBILITYRULESATTACHMENT.fields_by_name['initiator']._options = None
  _VISIBILITYRULESATTACHMENT.fields_by_name['initiator']._serialized_options = b'\030\001\312\235%\002\010\000'
  _VISIBILITYRULESATTACHMENT._serialized_start=135
  _VISIBILITYRULESATTACHMENT._serialized_end=452
  _VISIBILITYRULESATTACHMENT_RULE._serialized_start=381
  _VISIBILITYRULESATTACHMENT_RULE._serialized_end=452
# @@protoc_insertion_point(module_scope)
