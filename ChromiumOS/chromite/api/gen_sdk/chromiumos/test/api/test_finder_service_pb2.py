# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/test/api/test_finder_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen_sdk.chromiumos.test.api import cros_test_finder_cli_pb2 as chromiumos_dot_test_dot_api_dot_cros__test__finder__cli__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n-chromiumos/test/api/test_finder_service.proto\x12\x13\x63hromiumos.test.api\x1a.chromiumos/test/api/cros_test_finder_cli.proto2y\n\x11TestFinderService\x12\x64\n\tFindTests\x12*.chromiumos.test.api.CrosTestFinderRequest\x1a+.chromiumos.test.api.CrosTestFinderResponseB/Z-go.chromium.org/chromiumos/config/go/test/apib\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chromiumos.test.api.test_finder_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z-go.chromium.org/chromiumos/config/go/test/api'
  _globals['_TESTFINDERSERVICE']._serialized_start=118
  _globals['_TESTFINDERSERVICE']._serialized_end=239
# @@protoc_insertion_point(module_scope)
