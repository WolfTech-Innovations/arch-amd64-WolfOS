# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/test/hpt/perf_event.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$chromiumos/test/hpt/perf_event.proto\x12\x13\x63hromiumos.test.hpt\"\xf4\x01\n\nPerfRecord\x12\x13\n\x06\x62ucket\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x18\n\x0bobject_path\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x17\n\x06\x62ranch\x18\x03 \x01(\tB\x02\x18\x01H\x02\x88\x01\x01\x12\x14\n\x07version\x18\x04 \x01(\tH\x03\x88\x01\x01\x12\x12\n\x05\x62oard\x18\x05 \x01(\tH\x04\x88\x01\x01\x12 \n\x13snapshot_build_path\x18\x06 \x01(\tH\x05\x88\x01\x01\x42\t\n\x07_bucketB\x0e\n\x0c_object_pathB\t\n\x07_branchB\n\n\x08_versionB\x08\n\x06_boardB\x16\n\x14_snapshot_build_pathB/Z-go.chromium.org/chromiumos/config/go/test/hptb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chromiumos.test.hpt.perf_event_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z-go.chromium.org/chromiumos/config/go/test/hpt'
  _PERFRECORD.fields_by_name['branch']._options = None
  _PERFRECORD.fields_by_name['branch']._serialized_options = b'\030\001'
  _globals['_PERFRECORD']._serialized_start=62
  _globals['_PERFRECORD']._serialized_end=306
# @@protoc_insertion_point(module_scope)
