# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: entity/v1/element_common.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import kik_unofficial.protobuf.protobuf_validation_pb2 as protobuf__validation__pb2
import kik_unofficial.protobuf.common_model_pb2 as common__model__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from kik_unofficial.protobuf.common.v1 import model_pb2 as common_dot_v1_dot_model__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1e\x65ntity/v1/element_common.proto\x12\x10\x63ommon.entity.v1\x1a\x19protobuf_validation.proto\x1a\x12\x63ommon_model.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x15\x63ommon/v1/model.proto\"?\n\x10KinUserIdElement\x12+\n\x0bkin_user_id\x18\x01 \x01(\x0b\x32\x16.common.v1.XiKinUserId\"\"\n\nBioElement\x12\x14\n\x03\x62io\x18\x01 \x01(\tB\x07\xca\x9d%\x03\x30\x88\'\"(\n\rBylineElement\x12\x17\n\x06\x62yline\x18\x01 \x01(\tB\x07\xca\x9d%\x03\x30\xf4\x03\"H\n\x13RegistrationElement\x12\x31\n\rcreation_date\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"k\n\"OriginalProfilePicExtensionElement\x12\x45\n\x10\x65xtension_detail\x18\x01 \x01(\x0b\x32+.common.entity.v1.ProfilePicExtensionDetail\"m\n$BackgroundProfilePicExtensionElement\x12\x45\n\x10\x65xtension_detail\x18\x01 \x01(\x0b\x32+.common.entity.v1.ProfilePicExtensionDetail\"\x92\x01\n\x19ProfilePicExtensionDetail\x12\x30\n\x03pic\x18\x02 \x01(\x0b\x32!.common.entity.v1.InnerPicElementH\x00\x12;\n\tkik_asset\x18\x03 \x01(\x0b\x32&.common.entity.v1.InnerKikAssetElementH\x00\x42\x06\n\x04kind\"\x8e\x01\n\x0fInnerPicElement\x12\x1f\n\x0e\x66ull_sized_url\x18\x01 \x01(\tB\x07\xca\x9d%\x03\x30\xe8\x07\x12\x1e\n\rthumbnail_url\x18\x02 \x01(\tB\x07\xca\x9d%\x03\x30\xe8\x07\x12:\n\x16last_updated_timestamp\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"5\n\x14InnerKikAssetElement\x12\x1d\n\x0ckik_asset_id\x18\x01 \x01(\tB\x07\xca\x9d%\x03\x30\xf4\x03\"R\n\x12\x45mojiStatusElement\x12<\n\x0c\x65moji_status\x18\x01 \x01(\x0b\x32&.common.entity.v1.InnerKikAssetElement\"-\n\x13MaxGroupSizeElement\x12\x16\n\x0emax_group_size\x18\x01 \x01(\r\"(\n\x11KinEnabledElement\x12\x13\n\x0bkin_enabled\x18\x01 \x01(\x08\"\\\n\rRatingSummary\x12.\n\x0e\x61verage_rating\x18\x01 \x01(\x01\x42\x16\xca\x9d%\x12Y\x00\x00\x00\x00\x00\x00\x00\x00\x61\x00\x00\x00\x00\x00\x00\x14@\x12\x1b\n\x13total_ratings_count\x18\x02 \x01(\x04\"\x90\x03\n\x11GroupMemberRoster\x12/\n\x08user_jid\x18\x01 \x01(\x0b\x32\x15.common.XiBareUserJidB\x06\xca\x9d%\x02\x08\x00\x12\x30\n\talias_jid\x18\x03 \x01(\x0b\x32\x15.common.v1.XiAliasJidB\x06\xca\x9d%\x02\x08\x00\x12\x45\n\x0c\x61\x64min_status\x18\x02 \x01(\x0e\x32/.common.entity.v1.GroupMemberRoster.AdminStatus\x12^\n\x19\x64irect_messaging_disabled\x18\x04 \x01(\x0b\x32;.common.entity.v1.GroupMemberRoster.DirectMessagingDisabled\x1a<\n\x17\x44irectMessagingDisabled\x12!\n\x19\x64irect_messaging_disabled\x18\x01 \x01(\x08\"3\n\x0b\x41\x64minStatus\x12\x08\n\x04NONE\x10\x00\x12\t\n\x05\x41\x44MIN\x10\x01\x12\x0f\n\x0bSUPER_ADMIN\x10\x02\"T\n\x16GroupMemberListElement\x12:\n\rgroup_members\x18\x01 \x03(\x0b\x32#.common.entity.v1.GroupMemberRoster\",\n\x0fUsernameElement\x12\x19\n\x08username\x18\x01 \x01(\tB\x07\xca\x9d%\x03\x30\x80\x08\"3\n\x12\x44isplayNameElement\x12\x1d\n\x0c\x64isplay_name\x18\x01 \x01(\tB\x07\xca\x9d%\x03\x30\x80\x08\"e\n\x11ProfilePicElement\x12\x14\n\x03url\x18\x01 \x01(\tB\x07\xca\x9d%\x03\x30\x80\x08\x12:\n\x16last_updated_timestamp\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"\"\n\rPublicElement\x12\x11\n\tis_public\x18\x01 \x01(\x08\")\n\x10GroupCodeElement\x12\x15\n\x04\x63ode\x18\x01 \x01(\tB\x07\xca\x9d%\x03\x30\xe8\x07\")\n\x10GroupNameElement\x12\x15\n\x04name\x18\x01 \x01(\tB\x07\xca\x9d%\x03\x30\xe8\x07\"$\n\x0eTrustedElement\x12\x12\n\nis_trusted\x18\x01 \x01(\x08\"9\n\x13\x42otExtensionElement\x12\x0e\n\x06is_bot\x18\x02 \x01(\x08\x12\x12\n\nis_trusted\x18\x03 \x01(\x08\"\xa7\x01\n\x10InterestsElement\x12S\n\x11interests_element\x18\x01 \x03(\x0b\x32/.common.entity.v1.InterestsElement.InterestItemB\x07\xca\x9d%\x03\x80\x01\x14\x1a>\n\x0cInterestItem\x12\x12\n\x02id\x18\x01 \x01(\tB\x06\xca\x9d%\x02\x08\x01\x12\x1a\n\x12localized_verbiage\x18\x02 \x01(\t\"6\n\x10\x43hatThemeElement\x12\"\n\nproduct_id\x18\x01 \x01(\x0b\x32\x0e.common.XiUuid\"\x8c\x01\n\x14\x43hatThemeLockElement\x12\x46\n\x0block_status\x18\x01 \x01(\x0e\x32\x31.common.entity.v1.ChatThemeLockElement.LockStatus\",\n\nLockStatus\x12\x0c\n\x08UNLOCKED\x10\x00\x12\x10\n\x0c\x41\x44MIN_LOCKED\x10\x01\";\n\x16\x41nonMatchAvatarElement\x12!\n\tavatar_id\x18\x01 \x01(\x0b\x32\x0e.common.XiUuid\"*\n\x13\x44\x65\x61\x63tivationElement\x12\x13\n\x0b\x64\x65\x61\x63tivated\x18\x01 \x01(\x08\x42m\n\x14\x63om.kik.entity.modelZLgithub.com/kikinteractive/xiphias-model-common/generated/go/entity/v1;entity\xa0\x01\x01\xa2\x02\x03\x45NTb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'entity.v1.element_common_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\024com.kik.entity.modelZLgithub.com/kikinteractive/xiphias-model-common/generated/go/entity/v1;entity\240\001\001\242\002\003ENT'
  _BIOELEMENT.fields_by_name['bio']._options = None
  _BIOELEMENT.fields_by_name['bio']._serialized_options = b'\312\235%\0030\210\''
  _BYLINEELEMENT.fields_by_name['byline']._options = None
  _BYLINEELEMENT.fields_by_name['byline']._serialized_options = b'\312\235%\0030\364\003'
  _INNERPICELEMENT.fields_by_name['full_sized_url']._options = None
  _INNERPICELEMENT.fields_by_name['full_sized_url']._serialized_options = b'\312\235%\0030\350\007'
  _INNERPICELEMENT.fields_by_name['thumbnail_url']._options = None
  _INNERPICELEMENT.fields_by_name['thumbnail_url']._serialized_options = b'\312\235%\0030\350\007'
  _INNERKIKASSETELEMENT.fields_by_name['kik_asset_id']._options = None
  _INNERKIKASSETELEMENT.fields_by_name['kik_asset_id']._serialized_options = b'\312\235%\0030\364\003'
  _RATINGSUMMARY.fields_by_name['average_rating']._options = None
  _RATINGSUMMARY.fields_by_name['average_rating']._serialized_options = b'\312\235%\022Y\000\000\000\000\000\000\000\000a\000\000\000\000\000\000\024@'
  _GROUPMEMBERROSTER.fields_by_name['user_jid']._options = None
  _GROUPMEMBERROSTER.fields_by_name['user_jid']._serialized_options = b'\312\235%\002\010\000'
  _GROUPMEMBERROSTER.fields_by_name['alias_jid']._options = None
  _GROUPMEMBERROSTER.fields_by_name['alias_jid']._serialized_options = b'\312\235%\002\010\000'
  _USERNAMEELEMENT.fields_by_name['username']._options = None
  _USERNAMEELEMENT.fields_by_name['username']._serialized_options = b'\312\235%\0030\200\010'
  _DISPLAYNAMEELEMENT.fields_by_name['display_name']._options = None
  _DISPLAYNAMEELEMENT.fields_by_name['display_name']._serialized_options = b'\312\235%\0030\200\010'
  _PROFILEPICELEMENT.fields_by_name['url']._options = None
  _PROFILEPICELEMENT.fields_by_name['url']._serialized_options = b'\312\235%\0030\200\010'
  _GROUPCODEELEMENT.fields_by_name['code']._options = None
  _GROUPCODEELEMENT.fields_by_name['code']._serialized_options = b'\312\235%\0030\350\007'
  _GROUPNAMEELEMENT.fields_by_name['name']._options = None
  _GROUPNAMEELEMENT.fields_by_name['name']._serialized_options = b'\312\235%\0030\350\007'
  _INTERESTSELEMENT_INTERESTITEM.fields_by_name['id']._options = None
  _INTERESTSELEMENT_INTERESTITEM.fields_by_name['id']._serialized_options = b'\312\235%\002\010\001'
  _INTERESTSELEMENT.fields_by_name['interests_element']._options = None
  _INTERESTSELEMENT.fields_by_name['interests_element']._serialized_options = b'\312\235%\003\200\001\024'
  _KINUSERIDELEMENT._serialized_start=155
  _KINUSERIDELEMENT._serialized_end=218
  _BIOELEMENT._serialized_start=220
  _BIOELEMENT._serialized_end=254
  _BYLINEELEMENT._serialized_start=256
  _BYLINEELEMENT._serialized_end=296
  _REGISTRATIONELEMENT._serialized_start=298
  _REGISTRATIONELEMENT._serialized_end=370
  _ORIGINALPROFILEPICEXTENSIONELEMENT._serialized_start=372
  _ORIGINALPROFILEPICEXTENSIONELEMENT._serialized_end=479
  _BACKGROUNDPROFILEPICEXTENSIONELEMENT._serialized_start=481
  _BACKGROUNDPROFILEPICEXTENSIONELEMENT._serialized_end=590
  _PROFILEPICEXTENSIONDETAIL._serialized_start=593
  _PROFILEPICEXTENSIONDETAIL._serialized_end=739
  _INNERPICELEMENT._serialized_start=742
  _INNERPICELEMENT._serialized_end=884
  _INNERKIKASSETELEMENT._serialized_start=886
  _INNERKIKASSETELEMENT._serialized_end=939
  _EMOJISTATUSELEMENT._serialized_start=941
  _EMOJISTATUSELEMENT._serialized_end=1023
  _MAXGROUPSIZEELEMENT._serialized_start=1025
  _MAXGROUPSIZEELEMENT._serialized_end=1070
  _KINENABLEDELEMENT._serialized_start=1072
  _KINENABLEDELEMENT._serialized_end=1112
  _RATINGSUMMARY._serialized_start=1114
  _RATINGSUMMARY._serialized_end=1206
  _GROUPMEMBERROSTER._serialized_start=1209
  _GROUPMEMBERROSTER._serialized_end=1609
  _GROUPMEMBERROSTER_DIRECTMESSAGINGDISABLED._serialized_start=1496
  _GROUPMEMBERROSTER_DIRECTMESSAGINGDISABLED._serialized_end=1556
  _GROUPMEMBERROSTER_ADMINSTATUS._serialized_start=1558
  _GROUPMEMBERROSTER_ADMINSTATUS._serialized_end=1609
  _GROUPMEMBERLISTELEMENT._serialized_start=1611
  _GROUPMEMBERLISTELEMENT._serialized_end=1695
  _USERNAMEELEMENT._serialized_start=1697
  _USERNAMEELEMENT._serialized_end=1741
  _DISPLAYNAMEELEMENT._serialized_start=1743
  _DISPLAYNAMEELEMENT._serialized_end=1794
  _PROFILEPICELEMENT._serialized_start=1796
  _PROFILEPICELEMENT._serialized_end=1897
  _PUBLICELEMENT._serialized_start=1899
  _PUBLICELEMENT._serialized_end=1933
  _GROUPCODEELEMENT._serialized_start=1935
  _GROUPCODEELEMENT._serialized_end=1976
  _GROUPNAMEELEMENT._serialized_start=1978
  _GROUPNAMEELEMENT._serialized_end=2019
  _TRUSTEDELEMENT._serialized_start=2021
  _TRUSTEDELEMENT._serialized_end=2057
  _BOTEXTENSIONELEMENT._serialized_start=2059
  _BOTEXTENSIONELEMENT._serialized_end=2116
  _INTERESTSELEMENT._serialized_start=2119
  _INTERESTSELEMENT._serialized_end=2286
  _INTERESTSELEMENT_INTERESTITEM._serialized_start=2224
  _INTERESTSELEMENT_INTERESTITEM._serialized_end=2286
  _CHATTHEMEELEMENT._serialized_start=2288
  _CHATTHEMEELEMENT._serialized_end=2342
  _CHATTHEMELOCKELEMENT._serialized_start=2345
  _CHATTHEMELOCKELEMENT._serialized_end=2485
  _CHATTHEMELOCKELEMENT_LOCKSTATUS._serialized_start=2441
  _CHATTHEMELOCKELEMENT_LOCKSTATUS._serialized_end=2485
  _ANONMATCHAVATARELEMENT._serialized_start=2487
  _ANONMATCHAVATARELEMENT._serialized_end=2546
  _DEACTIVATIONELEMENT._serialized_start=2548
  _DEACTIVATIONELEMENT._serialized_end=2590
# @@protoc_insertion_point(module_scope)
