# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test_platform/result_flow/publish.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen_sdk.test_platform.result_flow import common_pb2 as test__platform_dot_result__flow_dot_common__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'test_platform/result_flow/publish.proto\x12\x19test_platform.result_flow\x1a&test_platform/result_flow/common.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\x99\x02\n\x0ePublishRequest\x12\x10\n\x08\x62uild_id\x18\x01 \x01(\x03\x12\x1b\n\x0fparent_build_id\x18\x02 \x01(\x03\x42\x02\x18\x01\x12\x34\n\x03\x63tp\x18\x03 \x01(\x0b\x32\'.test_platform.result_flow.PubSubConfig\x12<\n\x0btest_runner\x18\x04 \x01(\x0b\x32\'.test_platform.result_flow.PubSubConfig\x12,\n\x08\x64\x65\x61\x64line\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\"\n\x1ashould_poll_for_completion\x18\x06 \x01(\x08\x12\x12\n\nparent_uid\x18\x07 \x01(\t\"B\n\x0fPublishResponse\x12/\n\x05state\x18\x01 \x01(\x0e\x32 .test_platform.result_flow.StateBEZCgo.chromium.org/chromiumos/infra/proto/go/test_platform/result_flowb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'test_platform.result_flow.publish_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'ZCgo.chromium.org/chromiumos/infra/proto/go/test_platform/result_flow'
  _PUBLISHREQUEST.fields_by_name['parent_build_id']._options = None
  _PUBLISHREQUEST.fields_by_name['parent_build_id']._serialized_options = b'\030\001'
  _globals['_PUBLISHREQUEST']._serialized_start=144
  _globals['_PUBLISHREQUEST']._serialized_end=425
  _globals['_PUBLISHRESPONSE']._serialized_start=427
  _globals['_PUBLISHRESPONSE']._serialized_end=493
# @@protoc_insertion_point(module_scope)
