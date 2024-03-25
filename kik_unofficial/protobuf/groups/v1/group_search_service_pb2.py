# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: groups/v1/group_search_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import kik_unofficial.protobuf.common_model_pb2 as common__model__pb2
import kik_unofficial.protobuf.protobuf_validation_pb2 as protobuf__validation__pb2
from kik_unofficial.protobuf.groups.v1 import groups_common_pb2 as groups_dot_v1_dot_groups__common__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$groups/v1/group_search_service.proto\x12\x10mobile.groups.v1\x1a\x12\x63ommon_model.proto\x1a\x19protobuf_validation.proto\x1a\x1dgroups/v1/groups_common.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"2\n\x14PublicGroupJoinToken\x12\x1a\n\x05token\x18\x01 \x01(\x0c\x42\x0b\xca\x9d%\x07\x08\x01(\x01\x30\x80(\"\x1c\n\x1aGetGroupSuggestionsRequest\"\xd5\x01\n\x1bGetGroupSuggestionsResponse\x12\x44\n\x06result\x18\x01 \x01(\x0e\x32\x34.mobile.groups.v1.GetGroupSuggestionsResponse.Result\x12\x45\n\nsuggestion\x18\x02 \x03(\x0b\x32%.mobile.groups.v1.LimitedGroupDetailsB\n\xca\x9d%\x06\x08\x00\x80\x01\x80\x08\")\n\x06Result\x12\x06\n\x02OK\x10\x00\x12\x17\n\x13RATE_LIMIT_EXCEEDED\x10\x01\"A\n\x11\x46indGroupsRequest\x12,\n\x05query\x18\x01 \x01(\tB\x1d\xca\x9d%\x19\x08\x01\x12\x15^[A-Za-z0-9._]{1,32}$\"\xe0\x01\n\x12\x46indGroupsResponse\x12;\n\x06result\x18\x01 \x01(\x0e\x32+.mobile.groups.v1.FindGroupsResponse.Result\x12?\n\x05match\x18\x02 \x03(\x0b\x32%.mobile.groups.v1.LimitedGroupDetailsB\t\xca\x9d%\x05\x08\x00\x80\x01\x19\x12!\n\x19is_available_for_creation\x18\x03 \x01(\x08\")\n\x06Result\x12\x06\n\x02OK\x10\x00\x12\x17\n\x13RATE_LIMIT_EXCEEDED\x10\x01\"\xc8\x02\n\x13LimitedGroupDetails\x12\'\n\x03jid\x18\x01 \x01(\x0b\x32\x12.common.XiGroupJidB\x06\xca\x9d%\x02\x08\x00\x12@\n\x0c\x64isplay_data\x18\x02 \x01(\x0b\x32\".common.groups.v1.GroupDisplayDataB\x06\xca\x9d%\x02\x08\x00\x12\x14\n\x0cmember_count\x18\x03 \x01(\r\x12>\n\x12last_activity_time\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x06\xca\x9d%\x02\x08\x00\x12\x16\n\x0emax_group_size\x18\x05 \x01(\r\x12\x16\n\x0e\x61\x63tive_members\x18\x06 \x01(\r\x12@\n\x10group_join_token\x18\x64 \x01(\x0b\x32&.mobile.groups.v1.PublicGroupJoinToken2\xde\x01\n\x0bGroupSearch\x12Y\n\nFindGroups\x12#.mobile.groups.v1.FindGroupsRequest\x1a$.mobile.groups.v1.FindGroupsResponse\"\x00\x12t\n\x13GetGroupSuggestions\x12,.mobile.groups.v1.GetGroupSuggestionsRequest\x1a-.mobile.groups.v1.GetGroupSuggestionsResponse\"\x00\x42\\\n\x0e\x63om.kik.groupsZJgithub.com/kikinteractive/xiphias-api-mobile/generated/go/groups/v1;groupsb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'groups.v1.group_search_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\016com.kik.groupsZJgithub.com/kikinteractive/xiphias-api-mobile/generated/go/groups/v1;groups'
  _PUBLICGROUPJOINTOKEN.fields_by_name['token']._options = None
  _PUBLICGROUPJOINTOKEN.fields_by_name['token']._serialized_options = b'\312\235%\007\010\001(\0010\200('
  _GETGROUPSUGGESTIONSRESPONSE.fields_by_name['suggestion']._options = None
  _GETGROUPSUGGESTIONSRESPONSE.fields_by_name['suggestion']._serialized_options = b'\312\235%\006\010\000\200\001\200\010'
  _FINDGROUPSREQUEST.fields_by_name['query']._options = None
  _FINDGROUPSREQUEST.fields_by_name['query']._serialized_options = b'\312\235%\031\010\001\022\025^[A-Za-z0-9._]{1,32}$'
  _FINDGROUPSRESPONSE.fields_by_name['match']._options = None
  _FINDGROUPSRESPONSE.fields_by_name['match']._serialized_options = b'\312\235%\005\010\000\200\001\031'
  _LIMITEDGROUPDETAILS.fields_by_name['jid']._options = None
  _LIMITEDGROUPDETAILS.fields_by_name['jid']._serialized_options = b'\312\235%\002\010\000'
  _LIMITEDGROUPDETAILS.fields_by_name['display_data']._options = None
  _LIMITEDGROUPDETAILS.fields_by_name['display_data']._serialized_options = b'\312\235%\002\010\000'
  _LIMITEDGROUPDETAILS.fields_by_name['last_activity_time']._options = None
  _LIMITEDGROUPDETAILS.fields_by_name['last_activity_time']._serialized_options = b'\312\235%\002\010\000'
  _PUBLICGROUPJOINTOKEN._serialized_start=169
  _PUBLICGROUPJOINTOKEN._serialized_end=219
  _GETGROUPSUGGESTIONSREQUEST._serialized_start=221
  _GETGROUPSUGGESTIONSREQUEST._serialized_end=249
  _GETGROUPSUGGESTIONSRESPONSE._serialized_start=252
  _GETGROUPSUGGESTIONSRESPONSE._serialized_end=465
  _GETGROUPSUGGESTIONSRESPONSE_RESULT._serialized_start=424
  _GETGROUPSUGGESTIONSRESPONSE_RESULT._serialized_end=465
  _FINDGROUPSREQUEST._serialized_start=467
  _FINDGROUPSREQUEST._serialized_end=532
  _FINDGROUPSRESPONSE._serialized_start=535
  _FINDGROUPSRESPONSE._serialized_end=759
  _FINDGROUPSRESPONSE_RESULT._serialized_start=424
  _FINDGROUPSRESPONSE_RESULT._serialized_end=465
  _LIMITEDGROUPDETAILS._serialized_start=762
  _LIMITEDGROUPDETAILS._serialized_end=1090
  _GROUPSEARCH._serialized_start=1093
  _GROUPSEARCH._serialized_end=1315
# @@protoc_insertion_point(module_scope)
