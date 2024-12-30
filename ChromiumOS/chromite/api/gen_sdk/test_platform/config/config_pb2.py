# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test_platform/config/config.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen_sdk.test_platform.migration.test_runner import config_pb2 as test__platform_dot_migration_dot_test__runner_dot_config__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!test_platform/config/config.proto\x12\x14test_platform.config\x1a\x30test_platform/migration/test_runner/config.proto\"\xef\t\n\x06\x43onfig\x12>\n\x0fskylab_swarming\x18\x01 \x01(\x0b\x32%.test_platform.config.Config.Swarming\x12<\n\x0eskylab_isolate\x18\x03 \x01(\x0b\x32$.test_platform.config.Config.Isolate\x12@\n\rskylab_worker\x18\x04 \x01(\x0b\x32).test_platform.config.Config.SkylabWorker\x12;\n\nversioning\x18\x07 \x01(\x0b\x32\'.test_platform.config.Config.Versioning\x12<\n\x0btest_runner\x18\x08 \x01(\x0b\x32\'.test_platform.config.Config.TestRunner\x12J\n\x15test_runner_migration\x18\t \x01(\x0b\x32+.test_platform.migration.test_runner.Config\x12\x37\n\x06pubsub\x18\n \x01(\x0b\x32#.test_platform.config.Config.PubSubB\x02\x18\x01\x12@\n\x13result_flow_channel\x18\x0b \x01(\x0b\x32#.test_platform.config.Config.PubSub\x1a\x32\n\x08Swarming\x12\x0e\n\x06server\x18\x01 \x01(\t\x12\x16\n\x0e\x61uth_json_path\x18\x02 \x01(\t\x1a!\n\x07Isolate\x12\x16\n\x0e\x61uth_json_path\x18\x01 \x01(\t\x1a:\n\x0cSkylabWorker\x12\x14\n\x0cluci_project\x18\x01 \x01(\t\x12\x14\n\x0clog_dog_host\x18\x02 \x01(\t\x1a\x9d\x01\n\nVersioning\x12\x61\n\x19\x63ros_test_platform_binary\x18\x01 \x01(\x0b\x32>.test_platform.config.Config.Versioning.CrosTestPlatformBinary\x1a,\n\x16\x43rosTestPlatformBinary\x12\x12\n\ncipd_label\x18\x01 \x01(\t\x1aM\n\x0b\x42uildbucket\x12\x0c\n\x04host\x18\x01 \x01(\t\x12\x0f\n\x07project\x18\x02 \x01(\t\x12\x0e\n\x06\x62ucket\x18\x03 \x01(\t\x12\x0f\n\x07\x62uilder\x18\x04 \x01(\t\x1a(\n\x06PubSub\x12\x0f\n\x07project\x18\x01 \x01(\t\x12\r\n\x05topic\x18\x02 \x01(\t\x1a\xa4\x02\n\nTestRunner\x12=\n\x0b\x62uildbucket\x18\x01 \x01(\x0b\x32(.test_platform.config.Config.Buildbucket\x12\x37\n\x06pubsub\x18\x02 \x01(\x0b\x32#.test_platform.config.Config.PubSubB\x02\x18\x01\x12@\n\x13result_flow_channel\x18\x03 \x01(\x0b\x32#.test_platform.config.Config.PubSub\x12\x45\n\x18\x62\x62_status_update_channel\x18\x04 \x01(\x0b\x32#.test_platform.config.Config.PubSub\x12\x15\n\rswarming_pool\x18\x05 \x01(\tJ\x04\x08\x02\x10\x03J\x04\x08\x05\x10\x06J\x04\x08\x06\x10\x07\x42@Z>go.chromium.org/chromiumos/infra/proto/go/test_platform/configb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'test_platform.config.config_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z>go.chromium.org/chromiumos/infra/proto/go/test_platform/config'
  _CONFIG_TESTRUNNER.fields_by_name['pubsub']._options = None
  _CONFIG_TESTRUNNER.fields_by_name['pubsub']._serialized_options = b'\030\001'
  _CONFIG.fields_by_name['pubsub']._options = None
  _CONFIG.fields_by_name['pubsub']._serialized_options = b'\030\001'
  _globals['_CONFIG']._serialized_start=110
  _globals['_CONFIG']._serialized_end=1373
  _globals['_CONFIG_SWARMING']._serialized_start=634
  _globals['_CONFIG_SWARMING']._serialized_end=684
  _globals['_CONFIG_ISOLATE']._serialized_start=686
  _globals['_CONFIG_ISOLATE']._serialized_end=719
  _globals['_CONFIG_SKYLABWORKER']._serialized_start=721
  _globals['_CONFIG_SKYLABWORKER']._serialized_end=779
  _globals['_CONFIG_VERSIONING']._serialized_start=782
  _globals['_CONFIG_VERSIONING']._serialized_end=939
  _globals['_CONFIG_VERSIONING_CROSTESTPLATFORMBINARY']._serialized_start=895
  _globals['_CONFIG_VERSIONING_CROSTESTPLATFORMBINARY']._serialized_end=939
  _globals['_CONFIG_BUILDBUCKET']._serialized_start=941
  _globals['_CONFIG_BUILDBUCKET']._serialized_end=1018
  _globals['_CONFIG_PUBSUB']._serialized_start=1020
  _globals['_CONFIG_PUBSUB']._serialized_end=1060
  _globals['_CONFIG_TESTRUNNER']._serialized_start=1063
  _globals['_CONFIG_TESTRUNNER']._serialized_end=1355
# @@protoc_insertion_point(module_scope)
