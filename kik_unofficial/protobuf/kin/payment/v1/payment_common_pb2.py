# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: kin/payment/v1/payment_common.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import kik_unofficial.protobuf.protobuf_validation_pb2 as protobuf__validation__pb2
import kik_unofficial.protobuf.common_model_pb2 as common__model__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#kin/payment/v1/payment_common.proto\x12\x15\x63ommon.kin.payment.v1\x1a\x19protobuf_validation.proto\x1a\x12\x63ommon_model.proto\"\xb6\x01\n\x0bPaymentInfo\x12/\n\x07\x66\x65\x61ture\x18\x01 \x01(\x0e\x32\x1e.common.kin.payment.v1.Feature\x12\x38\n\x0c\x66\x65\x61ture_data\x18\x02 \x01(\x0b\x32\".common.kin.payment.v1.FeatureData\x12<\n\nkin_amount\x18\x03 \x01(\x0b\x32 .common.kin.payment.v1.KinAmountB\x06\xca\x9d%\x02\x08\x01\"l\n\x0b\x46\x65\x61tureData\x12U\n\x1bpublic_group_admin_tip_data\x18\x01 \x01(\x0b\x32..common.kin.payment.v1.PublicGroupAdminTipDataH\x00\x42\x06\n\x04kind\"D\n\x17PublicGroupAdminTipData\x12)\n\x05group\x18\x01 \x01(\x0b\x32\x12.common.XiGroupJidB\x06\xca\x9d%\x02\x08\x01\"\x1b\n\tKinAmount\x12\x0e\n\x06\x61mount\x18\x01 \x01(\x01*2\n\x07\x46\x65\x61ture\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x1a\n\x16PUBLIC_GROUP_ADMIN_TIP\x10\x01\x42o\n\x19\x63om.kik.kin.payment.modelZRgithub.com/kikinteractive/xiphias-model-common/generated/go/kin/payment/v1;paymentb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'kin.payment.v1.payment_common_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\031com.kik.kin.payment.modelZRgithub.com/kikinteractive/xiphias-model-common/generated/go/kin/payment/v1;payment'
  _PAYMENTINFO.fields_by_name['kin_amount']._options = None
  _PAYMENTINFO.fields_by_name['kin_amount']._serialized_options = b'\312\235%\002\010\001'
  _PUBLICGROUPADMINTIPDATA.fields_by_name['group']._options = None
  _PUBLICGROUPADMINTIPDATA.fields_by_name['group']._serialized_options = b'\312\235%\002\010\001'
  _FEATURE._serialized_start=503
  _FEATURE._serialized_end=553
  _PAYMENTINFO._serialized_start=110
  _PAYMENTINFO._serialized_end=292
  _FEATUREDATA._serialized_start=294
  _FEATUREDATA._serialized_end=402
  _PUBLICGROUPADMINTIPDATA._serialized_start=404
  _PUBLICGROUPADMINTIPDATA._serialized_end=472
  _KINAMOUNT._serialized_start=474
  _KINAMOUNT._serialized_end=501
# @@protoc_insertion_point(module_scope)
