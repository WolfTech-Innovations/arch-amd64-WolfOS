# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/config/api/design.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen_sdk.chromiumos.config.api import design_config_id_pb2 as chromiumos_dot_config_dot_api_dot_design__config__id__pb2
from chromite.api.gen_sdk.chromiumos.config.api import design_id_pb2 as chromiumos_dot_config_dot_api_dot_design__id__pb2
from chromite.api.gen_sdk.chromiumos.config.api import hardware_topology_pb2 as chromiumos_dot_config_dot_api_dot_hardware__topology__pb2
from chromite.api.gen_sdk.chromiumos.config.api import partner_id_pb2 as chromiumos_dot_config_dot_api_dot_partner__id__pb2
from chromite.api.gen_sdk.chromiumos.config.api import program_id_pb2 as chromiumos_dot_config_dot_api_dot_program__id__pb2
from chromite.api.gen_sdk.chromiumos.config.api import topology_pb2 as chromiumos_dot_config_dot_api_dot_topology__pb2
from chromite.api.gen_sdk.chromiumos.config.public_replication import public_replication_pb2 as chromiumos_dot_config_dot_public__replication_dot_public__replication__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\"chromiumos/config/api/design.proto\x12\x15\x63hromiumos.config.api\x1a,chromiumos/config/api/design_config_id.proto\x1a%chromiumos/config/api/design_id.proto\x1a-chromiumos/config/api/hardware_topology.proto\x1a&chromiumos/config/api/partner_id.proto\x1a&chromiumos/config/api/program_id.proto\x1a$chromiumos/config/api/topology.proto\x1a=chromiumos/config/public_replication/public_replication.proto\"\xbc\n\n\x06\x44\x65sign\x12S\n\x12public_replication\x18\x07 \x01(\x0b\x32\x37.chromiumos.config.public_replication.PublicReplication\x12+\n\x02id\x18\x01 \x01(\x0b\x32\x1f.chromiumos.config.api.DesignId\x12\x34\n\nprogram_id\x18\x02 \x01(\x0b\x32 .chromiumos.config.api.ProgramId\x12\x30\n\x06odm_id\x18\x03 \x01(\x0b\x32 .chromiumos.config.api.PartnerId\x12\x0c\n\x04name\x18\x04 \x01(\t\x12G\n\x0e\x62oard_id_phase\x18\x05 \x03(\x0b\x32/.chromiumos.config.api.Design.BoardIdPhaseEntry\x12\x35\n\x07\x63onfigs\x18\x06 \x03(\x0b\x32$.chromiumos.config.api.Design.Config\x12@\n\nssfc_value\x18\x08 \x03(\x0b\x32,.chromiumos.config.api.Design.SsfcValueEntry\x12=\n\x0b\x63ustom_type\x18\n \x01(\x0e\x32(.chromiumos.config.api.Design.CustomType\x12Q\n\x13spi_flash_transform\x18\x0b \x03(\x0b\x32\x34.chromiumos.config.api.Design.SpiFlashTransformEntry\x1a\x33\n\x11\x42oardIdPhaseEntry\x12\x0b\n\x03key\x18\x01 \x01(\r\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a\x30\n\x0eSsfcValueEntry\x12\x0b\n\x03key\x18\x01 \x01(\r\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a\x38\n\x16SpiFlashTransformEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a\xfa\x03\n\x06\x43onfig\x12S\n\x12public_replication\x18\x05 \x01(\x0b\x32\x37.chromiumos.config.public_replication.PublicReplication\x12\x31\n\x02id\x18\x01 \x01(\x0b\x32%.chromiumos.config.api.DesignConfigId\x12\x42\n\x11hardware_topology\x18\x02 \x01(\x0b\x32\'.chromiumos.config.api.HardwareTopology\x12\x42\n\x11hardware_features\x18\x03 \x01(\x0b\x32\'.chromiumos.config.api.HardwareFeatures\x1a\xd3\x01\n\nConstraint\x12\x44\n\x05level\x18\x01 \x01(\x0e\x32\x35.chromiumos.config.api.Design.Config.Constraint.Level\x12\x39\n\x08\x66\x65\x61tures\x18\x02 \x01(\x0b\x32\'.chromiumos.config.api.HardwareFeatures\"D\n\x05Level\x12\x10\n\x0cTYPE_UNKNOWN\x10\x00\x12\x0c\n\x08REQUIRED\x10\x01\x12\r\n\tPREFERRED\x10\x02\x12\x0c\n\x08OPTIONAL\x10\x03J\x04\x08\x04\x10\x05J\x04\x08\x07\x10\x08\"8\n\nCustomType\x12\r\n\tNO_CUSTOM\x10\x00\x12\x0e\n\nWHITELABEL\x10\x01\x12\x0b\n\x07REBRAND\x10\x02J\x04\x08\t\x10\nR\x08platformB*Z(go.chromium.org/chromiumos/config/go/apib\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chromiumos.config.api.design_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z(go.chromium.org/chromiumos/config/go/api'
  _DESIGN_BOARDIDPHASEENTRY._options = None
  _DESIGN_BOARDIDPHASEENTRY._serialized_options = b'8\001'
  _DESIGN_SSFCVALUEENTRY._options = None
  _DESIGN_SSFCVALUEENTRY._serialized_options = b'8\001'
  _DESIGN_SPIFLASHTRANSFORMENTRY._options = None
  _DESIGN_SPIFLASHTRANSFORMENTRY._serialized_options = b'8\001'
  _globals['_DESIGN']._serialized_start=375
  _globals['_DESIGN']._serialized_end=1715
  _globals['_DESIGN_BOARDIDPHASEENTRY']._serialized_start=973
  _globals['_DESIGN_BOARDIDPHASEENTRY']._serialized_end=1024
  _globals['_DESIGN_SSFCVALUEENTRY']._serialized_start=1026
  _globals['_DESIGN_SSFCVALUEENTRY']._serialized_end=1074
  _globals['_DESIGN_SPIFLASHTRANSFORMENTRY']._serialized_start=1076
  _globals['_DESIGN_SPIFLASHTRANSFORMENTRY']._serialized_end=1132
  _globals['_DESIGN_CONFIG']._serialized_start=1135
  _globals['_DESIGN_CONFIG']._serialized_end=1641
  _globals['_DESIGN_CONFIG_CONSTRAINT']._serialized_start=1418
  _globals['_DESIGN_CONFIG_CONSTRAINT']._serialized_end=1629
  _globals['_DESIGN_CONFIG_CONSTRAINT_LEVEL']._serialized_start=1561
  _globals['_DESIGN_CONFIG_CONSTRAINT_LEVEL']._serialized_end=1629
  _globals['_DESIGN_CUSTOMTYPE']._serialized_start=1643
  _globals['_DESIGN_CUSTOMTYPE']._serialized_end=1699
# @@protoc_insertion_point(module_scope)
