# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: messagepath/v1/carousels.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import kik_unofficial.protobuf.common_model_pb2 as common__model__pb2
import kik_unofficial.protobuf.protobuf_validation_pb2 as protobuf__validation__pb2
import kik_unofficial.protobuf.messagepath.v1_pb2 as keyboards


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1emessagepath/v1/carousels.proto\x12\x15\x63ommon.messagepath.v1\x1a\x12\x63ommon_model.proto\x1a\x19protobuf_validation.proto\x1a\x1emessagepath/v1/keyboards.proto\x1a!messagepath/v1/link_message.proto\"]\n\x19\x43\x61rouselMessageAttachment\x12@\n\x05items\x18\x01 \x03(\x0b\x32#.common.messagepath.v1.CarouselItemB\x0c\xca\x9d%\x08\x08\x01x\x01\x80\x01\xe8\x07\"{\n\x0c\x43\x61rouselItem\x12$\n\nmessage_id\x18\x01 \x01(\x0b\x32\x0e.common.XiUuidH\x00\x12=\n\x07\x63ontent\x18\x02 \x01(\x0b\x32*.common.messagepath.v1.CarouselItemContentH\x00\x42\x06\n\x04item\"\xb6\x01\n\x13\x43\x61rouselItemContent\x12\x46\n\x13keyboard_attachment\x18\x1e \x01(\x0b\x32).common.messagepath.v1.KeyboardAttachment\x12O\n\x17link_message_attachment\x18\x1f \x01(\x0b\x32,.common.messagepath.v1.LinkMessageAttachmentH\x00\x42\x06\n\x04typeBz\n\x19\x63om.kik.messagepath.modelZVgithub.com/kikinteractive/xiphias-model-common/generated/go/messagepath/v1;messagepath\xa2\x02\x04MPTHb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'messagepath.v1.carousels_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\031com.kik.messagepath.modelZVgithub.com/kikinteractive/xiphias-model-common/generated/go/messagepath/v1;messagepath\242\002\004MPTH'
  _CAROUSELMESSAGEATTACHMENT.fields_by_name['items']._options = None
  _CAROUSELMESSAGEATTACHMENT.fields_by_name['items']._serialized_options = b'\312\235%\010\010\001x\001\200\001\350\007'
  _CAROUSELMESSAGEATTACHMENT._serialized_start=171
  _CAROUSELMESSAGEATTACHMENT._serialized_end=264
  _CAROUSELITEM._serialized_start=266
  _CAROUSELITEM._serialized_end=389
  _CAROUSELITEMCONTENT._serialized_start=392
  _CAROUSELITEMCONTENT._serialized_end=574
# @@protoc_insertion_point(module_scope)
