# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test_platform/common/cft_steps_config.proto
"""Generated protocol buffer code."""
from chromite.third_party.google.protobuf.internal import builder as _builder
from chromite.third_party.google.protobuf import descriptor as _descriptor
from chromite.third_party.google.protobuf import descriptor_pool as _descriptor_pool
from chromite.third_party.google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+test_platform/common/cft_steps_config.proto\x12\x14test_platform.common\"]\n\x0e\x43\x66tStepsConfig\x12<\n\x0ehw_test_config\x18\x01 \x01(\x0b\x32\".test_platform.common.HwTestConfigH\x00\x42\r\n\x0b\x63onfig_type\"\xae\x02\n\x0cHwTestConfig\x12!\n\x19skip_loading_dut_topology\x18\x01 \x01(\x08\x12!\n\x19skip_starting_dut_service\x18\x02 \x01(\x08\x12\x16\n\x0eskip_provision\x18\x03 \x01(\x08\x12\x1b\n\x13skip_test_execution\x18\x04 \x01(\x08\x12\x1f\n\x17skip_all_result_publish\x18\x05 \x01(\x08\x12\x18\n\x10skip_gcs_publish\x18\x06 \x01(\x08\x12\x18\n\x10skip_rdb_publish\x18\x07 \x01(\x08\x12\x18\n\x10skip_tko_publish\x18\x08 \x01(\x08\x12\x19\n\x11run_cpcon_publish\x18\t \x01(\x08\x12\x19\n\x11skip_post_process\x18\n \x01(\x08\x42@Z>go.chromium.org/chromiumos/infra/proto/go/test_platform/commonb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'test_platform.common.cft_steps_config_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z>go.chromium.org/chromiumos/infra/proto/go/test_platform/common'
  _CFTSTEPSCONFIG._serialized_start=69
  _CFTSTEPSCONFIG._serialized_end=162
  _HWTESTCONFIG._serialized_start=165
  _HWTESTCONFIG._serialized_end=467
# @@protoc_insertion_point(module_scope)