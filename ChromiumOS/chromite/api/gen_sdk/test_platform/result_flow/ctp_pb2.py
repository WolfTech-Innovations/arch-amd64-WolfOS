# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test_platform/result_flow/ctp.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen_sdk.test_platform.result_flow import common_pb2 as test__platform_dot_result__flow_dot_common__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#test_platform/result_flow/ctp.proto\x12\x19test_platform.result_flow\x1a&test_platform/result_flow/common.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xa4\x01\n\nCTPRequest\x12.\n\x03\x63tp\x18\x01 \x01(\x0b\x32!.test_platform.result_flow.Source\x12\x38\n\rtest_plan_run\x18\x02 \x01(\x0b\x32!.test_platform.result_flow.Target\x12,\n\x08\x64\x65\x61\x64line\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\">\n\x0b\x43TPResponse\x12/\n\x05state\x18\x01 \x01(\x0e\x32 .test_platform.result_flow.StateBEZCgo.chromium.org/chromiumos/infra/proto/go/test_platform/result_flowb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'test_platform.result_flow.ctp_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'ZCgo.chromium.org/chromiumos/infra/proto/go/test_platform/result_flow'
  _globals['_CTPREQUEST']._serialized_start=140
  _globals['_CTPREQUEST']._serialized_end=304
  _globals['_CTPRESPONSE']._serialized_start=306
  _globals['_CTPRESPONSE']._serialized_end=368
# @@protoc_insertion_point(module_scope)
