# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: accounts/v1/user_info_shared.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import kik_unofficial.protobuf.protobuf_validation_pb2 as protobuf__validation__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\"accounts/v1/user_info_shared.proto\x12\x12\x63ommon.accounts.v1\x1a\x19protobuf_validation.proto\"R\n\x15\x44isplayNameComponents\x12\x1d\n\nfirst_name\x18\x01 \x01(\tB\t\xca\x9d%\x05\x08\x01\x30\xff\x01\x12\x1a\n\tlast_name\x18\x02 \x01(\tB\x07\xca\x9d%\x03\x30\xff\x01*r\n\rAccountStatus\x12\t\n\x05UNSET\x10\x00\x12\x19\n\x15\x44\x45\x41\x43TIVATED_CONFIRMED\x10\n\x12\x1b\n\x17\x44\x45\x41\x43TIVATED_UNCONFIRMED\x10\t\x12\x0f\n\x0bUNCONFIRMED\x10\x0b\x12\r\n\tCONFIRMED\x10\x0c\x42\x8c\x01\n\x16\x63om.kik.accounts.modelB\x13UserInfoSharedProtoP\x01ZPgithub.com/kikinteractive/xiphias-model-common/generated/go/accounts/v1;accounts\xa0\x01\x01\xa2\x02\x05XIACCb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'accounts.v1.user_info_shared_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\026com.kik.accounts.modelB\023UserInfoSharedProtoP\001ZPgithub.com/kikinteractive/xiphias-model-common/generated/go/accounts/v1;accounts\240\001\001\242\002\005XIACC'
  _DISPLAYNAMECOMPONENTS.fields_by_name['first_name']._options = None
  _DISPLAYNAMECOMPONENTS.fields_by_name['first_name']._serialized_options = b'\312\235%\005\010\0010\377\001'
  _DISPLAYNAMECOMPONENTS.fields_by_name['last_name']._options = None
  _DISPLAYNAMECOMPONENTS.fields_by_name['last_name']._serialized_options = b'\312\235%\0030\377\001'
  _ACCOUNTSTATUS._serialized_start=169
  _ACCOUNTSTATUS._serialized_end=283
  _DISPLAYNAMECOMPONENTS._serialized_start=85
  _DISPLAYNAMECOMPONENTS._serialized_end=167
# @@protoc_insertion_point(module_scope)
