# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/test/api/test_execution_metadata.proto
"""Generated protocol buffer code."""
from chromite.third_party.google.protobuf.internal import builder as _builder
from chromite.third_party.google.protobuf import descriptor as _descriptor
from chromite.third_party.google.protobuf import descriptor_pool as _descriptor_pool
from chromite.third_party.google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n1chromiumos/test/api/test_execution_metadata.proto\x12\x13\x63hromiumos.test.api\"\x9e\x01\n\x19\x41utotestExecutionMetadata\x12\x44\n\x04\x61rgs\x18\x01 \x03(\x0b\x32\x32.chromiumos.test.api.AutotestExecutionMetadata.ArgB\x02\x18\x01\x12\x17\n\x0fresults_sub_dir\x18\x02 \x01(\t\x1a\"\n\x03\x41rg\x12\x0c\n\x04\x66lag\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"\"\n\x03\x41rg\x12\x0c\n\x04\x66lag\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"C\n\x15TastExecutionMetadata\x12&\n\x04\x61rgs\x18\x01 \x03(\x0b\x32\x18.chromiumos.test.api.Arg:\x02\x18\x01\";\n\x11\x45xecutionMetadata\x12&\n\x04\x61rgs\x18\x01 \x03(\x0b\x32\x18.chromiumos.test.api.ArgB/Z-go.chromium.org/chromiumos/config/go/test/apib\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chromiumos.test.api.test_execution_metadata_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z-go.chromium.org/chromiumos/config/go/test/api'
  _AUTOTESTEXECUTIONMETADATA.fields_by_name['args']._options = None
  _AUTOTESTEXECUTIONMETADATA.fields_by_name['args']._serialized_options = b'\030\001'
  _TASTEXECUTIONMETADATA._options = None
  _TASTEXECUTIONMETADATA._serialized_options = b'\030\001'
  _AUTOTESTEXECUTIONMETADATA._serialized_start=75
  _AUTOTESTEXECUTIONMETADATA._serialized_end=233
  _AUTOTESTEXECUTIONMETADATA_ARG._serialized_start=199
  _AUTOTESTEXECUTIONMETADATA_ARG._serialized_end=233
  _ARG._serialized_start=199
  _ARG._serialized_end=233
  _TASTEXECUTIONMETADATA._serialized_start=271
  _TASTEXECUTIONMETADATA._serialized_end=338
  _EXECUTIONMETADATA._serialized_start=340
  _EXECUTIONMETADATA._serialized_end=399
# @@protoc_insertion_point(module_scope)
