# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/config/api/software/audio_config.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen_sdk.chromiumos.config.public_replication import public_replication_pb2 as chromiumos_dot_config_dot_public__replication_dot_public__replication__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n1chromiumos/config/api/software/audio_config.proto\x12\x1e\x63hromiumos.config.api.software\x1a=chromiumos/config/public_replication/public_replication.proto\"\xd2\x02\n\x0b\x41udioConfig\x12S\n\x12public_replication\x18\t \x01(\x0b\x32\x37.chromiumos.config.public_replication.PublicReplication\x12\x11\n\tcard_name\x18\x01 \x01(\t\x12\x18\n\x10\x63\x61rd_config_file\x18\x02 \x01(\t\x12\x10\n\x08\x64sp_file\x18\x03 \x01(\t\x12\x10\n\x08ucm_file\x18\x04 \x01(\t\x12\x17\n\x0fucm_master_file\x18\x05 \x01(\t\x12\x12\n\nucm_suffix\x18\x06 \x01(\t\x12\x13\n\x0bmodule_file\x18\x07 \x01(\t\x12\x12\n\nboard_file\x18\x08 \x01(\t\x12\x1c\n\x14sound_card_init_file\x18\n \x01(\t\x12\x0f\n\x07\x63\x61rd_id\x18\x0b \x01(\t\x12\x18\n\x10\x63ras_custom_name\x18\x0c \x01(\tB3Z1go.chromium.org/chromiumos/config/go/api/softwareb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chromiumos.config.api.software.audio_config_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z1go.chromium.org/chromiumos/config/go/api/software'
  _globals['_AUDIOCONFIG']._serialized_start=149
  _globals['_AUDIOCONFIG']._serialized_end=487
# @@protoc_insertion_point(module_scope)
