# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test_platform/skylab_test_runner/config.proto
"""Generated protocol buffer code."""
from chromite.third_party.google.protobuf.internal import builder as _builder
from chromite.third_party.google.protobuf import descriptor as _descriptor
from chromite.third_party.google.protobuf import descriptor_pool as _descriptor_pool
from chromite.third_party.google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen.test_platform.phosphorus import common_pb2 as test__platform_dot_phosphorus_dot_common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n-test_platform/skylab_test_runner/config.proto\x12 test_platform.skylab_test_runner\x1a%test_platform/phosphorus/common.proto\"\x96\x06\n\x06\x43onfig\x12\x39\n\x03lab\x18\x01 \x01(\x0b\x32,.test_platform.skylab_test_runner.Config.Lab\x12\x41\n\x07harness\x18\x02 \x01(\x0b\x32\x30.test_platform.skylab_test_runner.Config.Harness\x12?\n\x06output\x18\x03 \x01(\x0b\x32/.test_platform.skylab_test_runner.Config.Output\x12K\n\x12result_flow_pubsub\x18\x04 \x01(\x0b\x32/.test_platform.skylab_test_runner.Config.PubSub\x12I\n\x14log_data_upload_step\x18\x05 \x01(\x0b\x32+.test_platform.phosphorus.LogDataUploadStep\x12\x46\n\x12\x66\x65tch_crashes_step\x18\x06 \x01(\x0b\x32*.test_platform.phosphorus.FetchCrashesStep\x12\x39\n\x0bprejob_step\x18\x07 \x01(\x0b\x32$.test_platform.phosphorus.PrejobStep\x1aV\n\x03Lab\x12\x15\n\radmin_service\x18\x01 \x01(\t\x12\x1e\n\x16\x63ros_inventory_service\x18\x02 \x01(\t\x12\x18\n\x10\x63ros_ufs_service\x18\x03 \x01(\t\x1ay\n\x07Harness\x12\x14\n\x0c\x61utotest_dir\x18\x01 \x01(\t\x12\x1b\n\x13ssp_base_image_name\x18\x03 \x01(\t\x12\x1f\n\x17prejob_deadline_seconds\x18\x04 \x01(\x03J\x04\x08\x02\x10\x03R\x14synch_offload_subdir\x1a\x35\n\x06Output\x12\x18\n\x10log_data_gs_root\x18\x02 \x01(\tJ\x04\x08\x01\x10\x02R\x0bgs_root_dir\x1a(\n\x06PubSub\x12\x0f\n\x07project\x18\x01 \x01(\t\x12\r\n\x05topic\x18\x02 \x01(\tBLZJgo.chromium.org/chromiumos/infra/proto/go/test_platform/skylab_test_runnerb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'test_platform.skylab_test_runner.config_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'ZJgo.chromium.org/chromiumos/infra/proto/go/test_platform/skylab_test_runner'
  _CONFIG._serialized_start=123
  _CONFIG._serialized_end=913
  _CONFIG_LAB._serialized_start=607
  _CONFIG_LAB._serialized_end=693
  _CONFIG_HARNESS._serialized_start=695
  _CONFIG_HARNESS._serialized_end=816
  _CONFIG_OUTPUT._serialized_start=818
  _CONFIG_OUTPUT._serialized_end=871
  _CONFIG_PUBSUB._serialized_start=873
  _CONFIG_PUBSUB._serialized_end=913
# @@protoc_insertion_point(module_scope)
