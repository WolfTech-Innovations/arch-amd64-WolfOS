# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/greenness.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1a\x63hromiumos/greenness.proto\x12\nchromiumos\"\x9b\x03\n\x12\x41ggregateGreenness\x12\x18\n\x10\x61ggregate_metric\x18\x01 \x01(\x03\x12\x42\n\x10target_greenness\x18\x02 \x03(\x0b\x32(.chromiumos.AggregateGreenness.Greenness\x12\x1e\n\x16\x61ggregate_build_metric\x18\x03 \x01(\x03\x12\x43\n\x11\x62uilder_greenness\x18\x04 \x03(\x0b\x32(.chromiumos.AggregateGreenness.Greenness\x1a\xc1\x01\n\tGreenness\x12\x0e\n\x06target\x18\x01 \x01(\t\x12\x0e\n\x06metric\x18\x02 \x01(\x03\x12\x41\n\x07\x63ontext\x18\x03 \x01(\x0e\x32\x30.chromiumos.AggregateGreenness.Greenness.Context\x12\x14\n\x0c\x62uild_metric\x18\x04 \x01(\x03\x12\x0f\n\x07\x62uilder\x18\x05 \x01(\t\"*\n\x07\x43ontext\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0e\n\nIRRELEVANT\x10\x01\x42Y\n!com.google.chrome.crosinfra.protoZ4go.chromium.org/chromiumos/infra/proto/go/chromiumosb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chromiumos.greenness_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n!com.google.chrome.crosinfra.protoZ4go.chromium.org/chromiumos/infra/proto/go/chromiumos'
  _globals['_AGGREGATEGREENNESS']._serialized_start=43
  _globals['_AGGREGATEGREENNESS']._serialized_end=454
  _globals['_AGGREGATEGREENNESS_GREENNESS']._serialized_start=261
  _globals['_AGGREGATEGREENNESS_GREENNESS']._serialized_end=454
  _globals['_AGGREGATEGREENNESS_GREENNESS_CONTEXT']._serialized_start=412
  _globals['_AGGREGATEGREENNESS_GREENNESS_CONTEXT']._serialized_end=454
# @@protoc_insertion_point(module_scope)