# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/config/api/software/brand_config.proto
"""Generated protocol buffer code."""
from chromite.third_party.google.protobuf.internal import builder as _builder
from chromite.third_party.google.protobuf import descriptor as _descriptor
from chromite.third_party.google.protobuf import descriptor_pool as _descriptor_pool
from chromite.third_party.google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen.chromiumos.config.api import device_brand_id_pb2 as chromiumos_dot_config_dot_api_dot_device__brand__id__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n1chromiumos/config/api/software/brand_config.proto\x12\x1e\x63hromiumos.config.api.software\x1a+chromiumos/config/api/device_brand_id.proto\"\xee\x01\n\x0b\x42randConfig\x12\x36\n\x08\x62rand_id\x18\x01 \x01(\x0b\x32$.chromiumos.config.api.DeviceBrandId\x12\x44\n\x0bscan_config\x18\x02 \x01(\x0b\x32/.chromiumos.config.api.DeviceBrandId.ScanConfig\x12\x11\n\twallpaper\x18\x03 \x01(\t\x12\x18\n\x10regulatory_label\x18\x04 \x01(\t\x12\x17\n\x0fhelp_content_id\x18\x05 \x01(\t\x12\x1b\n\x13\x63loud_gaming_device\x18\x06 \x01(\x08\x42\x33Z1go.chromium.org/chromiumos/config/go/api/softwareb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chromiumos.config.api.software.brand_config_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z1go.chromium.org/chromiumos/config/go/api/software'
  _BRANDCONFIG._serialized_start=131
  _BRANDCONFIG._serialized_end=369
# @@protoc_insertion_point(module_scope)
