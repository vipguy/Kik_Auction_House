# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: matching/v1/anon_matching_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import kik_unofficial.protobuf.protobuf_validation_pb2 as protobuf__validation__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
import kik_unofficial.protobuf.common_model_pb2 as common__model__pb2
import kik_unofficial.protobuf.common.v1_pb2 as model


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'matching/v1/anon_matching_service.proto\x12\x12mobile.matching.v1\x1a\x19protobuf_validation.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x12\x63ommon_model.proto\x1a\x15\x63ommon/v1/model.proto\x1a!matching/v1/matching_common.proto\"p\n\x16\x46indChatPartnerRequest\x12<\n\tinterests\x18\x01 \x03(\x0b\x32 .mobile.matching.v1.ChatInterestB\x07\xca\x9d%\x03\x80\x01\x05\x12\x18\n\x10matching_variant\x18\x02 \x01(\t\"\x80\x03\n\x17\x46indChatPartnerResponse\x12\x42\n\x06result\x18\x01 \x01(\x0e\x32\x32.mobile.matching.v1.FindChatPartnerResponse.Result\x12,\n\x14\x66ind_chat_request_id\x18\x02 \x01(\x0b\x32\x0e.common.XiUuid\x12;\n\x0fsession_details\x18\x03 \x01(\x0b\x32\".mobile.matching.v1.SessionDetails\x12\x38\n\x14rejected_expiry_time\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"|\n\x06Result\x12\x11\n\rPARTNER_FOUND\x10\x00\x12\x0c\n\x08IN_QUEUE\x10\x01\x12\x0c\n\x08REJECTED\x10\x02\x12\"\n\x1eREJECTED_NO_REMAINING_SESSIONS\x10\x03\x12\x1f\n\x1bREJECTED_TEMPORARILY_BANNED\x10\x04\"T\n\x1c\x43\x61ncelFindChatPartnerRequest\x12\x34\n\x14\x66ind_chat_request_id\x18\x01 \x01(\x0b\x32\x0e.common.XiUuidB\x06\xca\x9d%\x02\x08\x01\"\x98\x01\n\x1d\x43\x61ncelFindChatPartnerResponse\x12H\n\x06result\x18\x01 \x01(\x0e\x32\x38.mobile.matching.v1.CancelFindChatPartnerResponse.Result\"-\n\x06Result\x12\x06\n\x02OK\x10\x00\x12\x1b\n\x17SESSION_ALREADY_CREATED\x10\x01\"`\n\x15GetChatSessionRequest\x12G\n\x0bsession_key\x18\x01 \x01(\x0b\x32*.common.matching.v1.AnonMatchingSessionKeyB\x06\xca\x9d%\x02\x08\x01\"\xb9\x01\n\x16GetChatSessionResponse\x12\x41\n\x06result\x18\x01 \x01(\x0e\x32\x31.mobile.matching.v1.GetChatSessionResponse.Result\x12;\n\x0fsession_details\x18\x02 \x01(\x0b\x32\".mobile.matching.v1.SessionDetails\"\x1f\n\x06Result\x12\x06\n\x02OK\x10\x00\x12\r\n\tNOT_FOUND\x10\x01\"`\n\x15\x45ndChatSessionRequest\x12G\n\x0bsession_key\x18\x01 \x01(\x0b\x32*.common.matching.v1.AnonMatchingSessionKeyB\x06\xca\x9d%\x02\x08\x01\"m\n\x16\x45ndChatSessionResponse\x12\x41\n\x06result\x18\x01 \x01(\x0e\x32\x31.mobile.matching.v1.EndChatSessionResponse.Result\"\x10\n\x06Result\x12\x06\n\x02OK\x10\x00\"\x1e\n\x1cGetRemainingAnonChatsRequest\"\x94\x01\n\x1dGetRemainingAnonChatsResponse\x12H\n\x06result\x18\x01 \x01(\x0e\x32\x38.mobile.matching.v1.GetRemainingAnonChatsResponse.Result\x12\x17\n\x0fremaining_chats\x18\x02 \x01(\x05\"\x10\n\x06Result\x12\x06\n\x02OK\x10\x00\"T\n\x0c\x43hatInterest\x12 \n\x0binterest_id\x18\x01 \x01(\tB\x0b\xca\x9d%\x07\x08\x01(\x01\x30\xff\x01\x12\"\n\rinterest_name\x18\x02 \x01(\tB\x0b\xca\x9d%\x07\x08\x01(\x01\x30\xff\x01\"\xa3\x02\n\x0eSessionDetails\x12*\n\nsession_id\x18\x01 \x01(\x0b\x32\x0e.common.XiUuidB\x06\xca\x9d%\x02\x08\x01\x12\x39\n\x12\x63hat_partner_alias\x18\x03 \x01(\x0b\x32\x15.common.v1.XiAliasJidB\x06\xca\x9d%\x02\x08\x01\x12\x34\n\x10session_end_time\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x37\n\x13session_expiry_time\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12;\n\rsession_state\x18\x06 \x01(\x0e\x32$.common.matching.v1.ChatSessionState2\xc8\x04\n\x0c\x41nonMatching\x12j\n\x0f\x46indChatPartner\x12*.mobile.matching.v1.FindChatPartnerRequest\x1a+.mobile.matching.v1.FindChatPartnerResponse\x12|\n\x15\x43\x61ncelFindChatPartner\x12\x30.mobile.matching.v1.CancelFindChatPartnerRequest\x1a\x31.mobile.matching.v1.CancelFindChatPartnerResponse\x12g\n\x0e\x45ndChatSession\x12).mobile.matching.v1.EndChatSessionRequest\x1a*.mobile.matching.v1.EndChatSessionResponse\x12g\n\x0eGetChatSession\x12).mobile.matching.v1.GetChatSessionRequest\x1a*.mobile.matching.v1.GetChatSessionResponse\x12|\n\x15GetRemainingAnonChats\x12\x30.mobile.matching.v1.GetRemainingAnonChatsRequest\x1a\x31.mobile.matching.v1.GetRemainingAnonChatsResponseBf\n\x14\x63om.kik.matching.rpcZNgithub.com/kikinteractive/xiphias-api-mobile/generated/go/matching/v1;matchingb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'matching.v1.anon_matching_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\024com.kik.matching.rpcZNgithub.com/kikinteractive/xiphias-api-mobile/generated/go/matching/v1;matching'
  _FINDCHATPARTNERREQUEST.fields_by_name['interests']._options = None
  _FINDCHATPARTNERREQUEST.fields_by_name['interests']._serialized_options = b'\312\235%\003\200\001\005'
  _CANCELFINDCHATPARTNERREQUEST.fields_by_name['find_chat_request_id']._options = None
  _CANCELFINDCHATPARTNERREQUEST.fields_by_name['find_chat_request_id']._serialized_options = b'\312\235%\002\010\001'
  _GETCHATSESSIONREQUEST.fields_by_name['session_key']._options = None
  _GETCHATSESSIONREQUEST.fields_by_name['session_key']._serialized_options = b'\312\235%\002\010\001'
  _ENDCHATSESSIONREQUEST.fields_by_name['session_key']._options = None
  _ENDCHATSESSIONREQUEST.fields_by_name['session_key']._serialized_options = b'\312\235%\002\010\001'
  _CHATINTEREST.fields_by_name['interest_id']._options = None
  _CHATINTEREST.fields_by_name['interest_id']._serialized_options = b'\312\235%\007\010\001(\0010\377\001'
  _CHATINTEREST.fields_by_name['interest_name']._options = None
  _CHATINTEREST.fields_by_name['interest_name']._serialized_options = b'\312\235%\007\010\001(\0010\377\001'
  _SESSIONDETAILS.fields_by_name['session_id']._options = None
  _SESSIONDETAILS.fields_by_name['session_id']._serialized_options = b'\312\235%\002\010\001'
  _SESSIONDETAILS.fields_by_name['chat_partner_alias']._options = None
  _SESSIONDETAILS.fields_by_name['chat_partner_alias']._serialized_options = b'\312\235%\002\010\001'
  _FINDCHATPARTNERREQUEST._serialized_start=201
  _FINDCHATPARTNERREQUEST._serialized_end=313
  _FINDCHATPARTNERRESPONSE._serialized_start=316
  _FINDCHATPARTNERRESPONSE._serialized_end=700
  _FINDCHATPARTNERRESPONSE_RESULT._serialized_start=576
  _FINDCHATPARTNERRESPONSE_RESULT._serialized_end=700
  _CANCELFINDCHATPARTNERREQUEST._serialized_start=702
  _CANCELFINDCHATPARTNERREQUEST._serialized_end=786
  _CANCELFINDCHATPARTNERRESPONSE._serialized_start=789
  _CANCELFINDCHATPARTNERRESPONSE._serialized_end=941
  _CANCELFINDCHATPARTNERRESPONSE_RESULT._serialized_start=896
  _CANCELFINDCHATPARTNERRESPONSE_RESULT._serialized_end=941
  _GETCHATSESSIONREQUEST._serialized_start=943
  _GETCHATSESSIONREQUEST._serialized_end=1039
  _GETCHATSESSIONRESPONSE._serialized_start=1042
  _GETCHATSESSIONRESPONSE._serialized_end=1227
  _GETCHATSESSIONRESPONSE_RESULT._serialized_start=1196
  _GETCHATSESSIONRESPONSE_RESULT._serialized_end=1227
  _ENDCHATSESSIONREQUEST._serialized_start=1229
  _ENDCHATSESSIONREQUEST._serialized_end=1325
  _ENDCHATSESSIONRESPONSE._serialized_start=1327
  _ENDCHATSESSIONRESPONSE._serialized_end=1436
  _ENDCHATSESSIONRESPONSE_RESULT._serialized_start=896
  _ENDCHATSESSIONRESPONSE_RESULT._serialized_end=912
  _GETREMAININGANONCHATSREQUEST._serialized_start=1438
  _GETREMAININGANONCHATSREQUEST._serialized_end=1468
  _GETREMAININGANONCHATSRESPONSE._serialized_start=1471
  _GETREMAININGANONCHATSRESPONSE._serialized_end=1619
  _GETREMAININGANONCHATSRESPONSE_RESULT._serialized_start=896
  _GETREMAININGANONCHATSRESPONSE_RESULT._serialized_end=912
  _CHATINTEREST._serialized_start=1621
  _CHATINTEREST._serialized_end=1705
  _SESSIONDETAILS._serialized_start=1708
  _SESSIONDETAILS._serialized_end=1999
  _ANONMATCHING._serialized_start=2002
  _ANONMATCHING._serialized_end=2586
# @@protoc_insertion_point(module_scope)
