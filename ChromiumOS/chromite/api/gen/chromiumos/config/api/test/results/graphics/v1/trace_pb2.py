# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/config/api/test/results/graphics/v1/trace.proto
"""Generated protocol buffer code."""
from chromite.third_party.google.protobuf.internal import builder as _builder
from chromite.third_party.google.protobuf import descriptor as _descriptor
from chromite.third_party.google.protobuf import descriptor_pool as _descriptor_pool
from chromite.third_party.google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen.chromiumos.config.api.test.results.graphics.v1 import trace_id_pb2 as chromiumos_dot_config_dot_api_dot_test_dot_results_dot_graphics_dot_v1_dot_trace__id__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n:chromiumos/config/api/test/results/graphics/v1/trace.proto\x12.chromiumos.config.api.test.results.graphics.v1\x1a=chromiumos/config/api/test/results/graphics/v1/trace_id.proto\"\xc9\x02\n\x05Trace\x12\x43\n\x02id\x18\x01 \x01(\x0b\x32\x37.chromiumos.config.api.test.results.graphics.v1.TraceId\x12\x10\n\x08\x66ilename\x18\x02 \x01(\t\x12\x0c\n\x04size\x18\x03 \x01(\x04\x12\x0e\n\x06source\x18\x04 \x01(\t\x12\x16\n\x0e\x61pplication_id\x18\x05 \x01(\t\x12\x13\n\x0b\x66rame_count\x18\x06 \x01(\r\x12P\n\x0b\x66rame_range\x18\x07 \x01(\x0b\x32;.chromiumos.config.api.test.results.graphics.v1.Trace.Range\x12\x12\n\nkey_frames\x18\x08 \x03(\r\x12\x13\n\x0bloop_frames\x18\t \x03(\r\x1a#\n\x05Range\x12\r\n\x05start\x18\x01 \x01(\r\x12\x0b\n\x03\x65nd\x18\x02 \x01(\r\"Q\n\tTraceList\x12\x44\n\x05value\x18\x01 \x03(\x0b\x32\x35.chromiumos.config.api.test.results.graphics.v1.TraceBLZJgo.chromium.org/chromiumos/config/go/api/test/results/graphics/v1;graphicsb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chromiumos.config.api.test.results.graphics.v1.trace_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'ZJgo.chromium.org/chromiumos/config/go/api/test/results/graphics/v1;graphics'
  _TRACE._serialized_start=174
  _TRACE._serialized_end=503
  _TRACE_RANGE._serialized_start=468
  _TRACE_RANGE._serialized_end=503
  _TRACELIST._serialized_start=505
  _TRACELIST._serialized_end=586
# @@protoc_insertion_point(module_scope)
