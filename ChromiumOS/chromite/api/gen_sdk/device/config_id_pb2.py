# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: device/config_id.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen_sdk.device import platform_id_pb2 as device_dot_platform__id__pb2
from chromite.api.gen_sdk.device import model_id_pb2 as device_dot_model__id__pb2
from chromite.api.gen_sdk.device import brand_id_pb2 as device_dot_brand__id__pb2
from chromite.api.gen_sdk.device import variant_id_pb2 as device_dot_variant__id__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16\x64\x65vice/config_id.proto\x12\x06\x64\x65vice\x1a\x18\x64\x65vice/platform_id.proto\x1a\x15\x64\x65vice/model_id.proto\x1a\x15\x64\x65vice/brand_id.proto\x1a\x17\x64\x65vice/variant_id.proto\"\xa0\x01\n\x08\x43onfigId\x12\'\n\x0bplatform_id\x18\x01 \x01(\x0b\x32\x12.device.PlatformId\x12!\n\x08model_id\x18\x02 \x01(\x0b\x32\x0f.device.ModelId\x12%\n\nvariant_id\x18\x03 \x01(\x0b\x32\x11.device.VariantId\x12!\n\x08\x62rand_id\x18\x04 \x01(\x0b\x32\x0f.device.BrandIdB2Z0go.chromium.org/chromiumos/infra/proto/go/deviceb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'device.config_id_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z0go.chromium.org/chromiumos/infra/proto/go/device'
  _globals['_CONFIGID']._serialized_start=132
  _globals['_CONFIGID']._serialized_end=292
# @@protoc_insertion_point(module_scope)
