# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/config/api/software/power_config.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n1chromiumos/config/api/software/power_config.proto\x12\x1e\x63hromiumos.config.api.software\"\x94\x01\n\x0bPowerConfig\x12Q\n\x0bpreferences\x18\x01 \x03(\x0b\x32<.chromiumos.config.api.software.PowerConfig.PreferencesEntry\x1a\x32\n\x10PreferencesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42\x33Z1go.chromium.org/chromiumos/config/go/api/softwareb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chromiumos.config.api.software.power_config_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z1go.chromium.org/chromiumos/config/go/api/software'
  _POWERCONFIG_PREFERENCESENTRY._options = None
  _POWERCONFIG_PREFERENCESENTRY._serialized_options = b'8\001'
  _globals['_POWERCONFIG']._serialized_start=86
  _globals['_POWERCONFIG']._serialized_end=234
  _globals['_POWERCONFIG_PREFERENCESENTRY']._serialized_start=184
  _globals['_POWERCONFIG_PREFERENCESENTRY']._serialized_end=234
# @@protoc_insertion_point(module_scope)
