# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/test/scheduling/swarming_dimensions.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n4chromiumos/test/scheduling/swarming_dimensions.proto\x12\x1a\x63hromiumos.test.scheduling\"\xba\x01\n\x12SwarmingDimensions\x12M\n\x08\x64ims_map\x18\x01 \x03(\x0b\x32;.chromiumos.test.scheduling.SwarmingDimensions.DimsMapEntry\x1aU\n\x0c\x44imsMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x34\n\x05value\x18\x02 \x01(\x0b\x32%.chromiumos.test.scheduling.DimValues:\x02\x38\x01\"\x1b\n\tDimValues\x12\x0e\n\x06values\x18\x02 \x03(\tB\tZ\x07./protob\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chromiumos.test.scheduling.swarming_dimensions_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z\007./proto'
  _SWARMINGDIMENSIONS_DIMSMAPENTRY._options = None
  _SWARMINGDIMENSIONS_DIMSMAPENTRY._serialized_options = b'8\001'
  _globals['_SWARMINGDIMENSIONS']._serialized_start=85
  _globals['_SWARMINGDIMENSIONS']._serialized_end=271
  _globals['_SWARMINGDIMENSIONS_DIMSMAPENTRY']._serialized_start=186
  _globals['_SWARMINGDIMENSIONS_DIMSMAPENTRY']._serialized_end=271
  _globals['_DIMVALUES']._serialized_start=273
  _globals['_DIMVALUES']._serialized_end=300
# @@protoc_insertion_point(module_scope)
