# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/config/api/device_config.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen_sdk.chromiumos.config.api import design_pb2 as chromiumos_dot_config_dot_api_dot_design__pb2
from chromite.api.gen_sdk.chromiumos.config.api import device_brand_pb2 as chromiumos_dot_config_dot_api_dot_device__brand__pb2
from chromite.api.gen_sdk.chromiumos.config.api import mfg_config_pb2 as chromiumos_dot_config_dot_api_dot_mfg__config__pb2
from chromite.api.gen_sdk.chromiumos.config.api import partner_pb2 as chromiumos_dot_config_dot_api_dot_partner__pb2
from chromite.api.gen_sdk.chromiumos.config.api import program_pb2 as chromiumos_dot_config_dot_api_dot_program__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)chromiumos/config/api/device_config.proto\x12\x15\x63hromiumos.config.api\x1a\"chromiumos/config/api/design.proto\x1a(chromiumos/config/api/device_brand.proto\x1a&chromiumos/config/api/mfg_config.proto\x1a#chromiumos/config/api/partner.proto\x1a#chromiumos/config/api/program.proto\"\xfb\x02\n\x0c\x44\x65viceConfig\x12/\n\x07program\x18\x01 \x01(\x0b\x32\x1e.chromiumos.config.api.Program\x12\x30\n\thw_design\x18\x02 \x01(\x0b\x32\x1d.chromiumos.config.api.Design\x12+\n\x03odm\x18\x03 \x01(\x0b\x32\x1e.chromiumos.config.api.Partner\x12>\n\x10hw_design_config\x18\x04 \x01(\x0b\x32$.chromiumos.config.api.Design.Config\x12\x38\n\x0c\x64\x65vice_brand\x18\x05 \x01(\x0b\x32\".chromiumos.config.api.DeviceBrand\x12+\n\x03oem\x18\x06 \x01(\x0b\x32\x1e.chromiumos.config.api.Partner\x12\x34\n\nmfg_config\x18\x07 \x01(\x0b\x32 .chromiumos.config.api.MfgConfigB*Z(go.chromium.org/chromiumos/config/go/apib\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chromiumos.config.api.device_config_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z(go.chromium.org/chromiumos/config/go/api'
  _globals['_DEVICECONFIG']._serialized_start=261
  _globals['_DEVICECONFIG']._serialized_end=640
# @@protoc_insertion_point(module_scope)
