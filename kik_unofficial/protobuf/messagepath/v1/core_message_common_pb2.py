# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: messagepath/v1/core_message_common.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import kik_unofficial.protobuf.common_model_pb2 as common__model__pb2
import protobuf_validation_pb2 as protobuf__validation__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(messagepath/v1/core_message_common.proto\x12\x15\x63ommon.messagepath.v1\x1a\x12\x63ommon_model.proto\x1a\x19protobuf_validation.proto\"c\n\x15\x41ttributionAttachment\x12\x15\n\x04name\x18\x01 \x01(\tB\x07\xca\x9d%\x03\x30\xf4\x03\x12\x33\n\x04icon\x18\x02 \x01(\x0b\x32%.common.messagepath.v1.PictureElement\"\xa8\x01\n\x14\x43ontentLayoutElement\x12K\n\x04type\x18\x01 \x01(\x0e\x32=.common.messagepath.v1.ContentLayoutElement.ContentLayoutType\"C\n\x11\x43ontentLayoutType\x12\x0b\n\x07\x44\x45\x46\x41ULT\x10\x00\x12\x0b\n\x07\x41RTICLE\x10\x01\x12\t\n\x05PHOTO\x10\x02\x12\t\n\x05VIDEO\x10\x03\"&\n\x0ePictureElement\x12\x14\n\x03url\x18\x01 \x01(\tB\x07\xca\x9d%\x03\x30\x80(\"\xb5\x01\n\nUriElement\x12\x16\n\x03uri\x18\x01 \x01(\tB\t\xca\x9d%\x05\x08\x01\x30\x80(\x12<\n\x08platform\x18\x64 \x01(\x0e\x32*.common.messagepath.v1.UriElement.Platform\x12\x11\n\x08priority\x18\xe8\x07 \x01(\r\">\n\x08Platform\x12\x07\n\x03\x41LL\x10\x00\x12\x07\n\x03WEB\x10\x01\x12\x07\n\x03IOS\x10\x02\x12\x0b\n\x07\x41NDROID\x10\x03\x12\n\n\x06WIDGET\x10\x04\x42z\n\x19\x63om.kik.messagepath.modelZVgithub.com/kikinteractive/xiphias-model-common/generated/go/messagepath/v1;messagepath\xa2\x02\x04MPTHb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'messagepath.v1.core_message_common_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\031com.kik.messagepath.modelZVgithub.com/kikinteractive/xiphias-model-common/generated/go/messagepath/v1;messagepath\242\002\004MPTH'
  _ATTRIBUTIONATTACHMENT.fields_by_name['name']._options = None
  _ATTRIBUTIONATTACHMENT.fields_by_name['name']._serialized_options = b'\312\235%\0030\364\003'
  _PICTUREELEMENT.fields_by_name['url']._options = None
  _PICTUREELEMENT.fields_by_name['url']._serialized_options = b'\312\235%\0030\200('
  _URIELEMENT.fields_by_name['uri']._options = None
  _URIELEMENT.fields_by_name['uri']._serialized_options = b'\312\235%\005\010\0010\200('
  _ATTRIBUTIONATTACHMENT._serialized_start=114
  _ATTRIBUTIONATTACHMENT._serialized_end=213
  _CONTENTLAYOUTELEMENT._serialized_start=216
  _CONTENTLAYOUTELEMENT._serialized_end=384
  _CONTENTLAYOUTELEMENT_CONTENTLAYOUTTYPE._serialized_start=317
  _CONTENTLAYOUTELEMENT_CONTENTLAYOUTTYPE._serialized_end=384
  _PICTUREELEMENT._serialized_start=386
  _PICTUREELEMENT._serialized_end=424
  _URIELEMENT._serialized_start=427
  _URIELEMENT._serialized_end=608
  _URIELEMENT_PLATFORM._serialized_start=546
  _URIELEMENT_PLATFORM._serialized_end=608
# @@protoc_insertion_point(module_scope)