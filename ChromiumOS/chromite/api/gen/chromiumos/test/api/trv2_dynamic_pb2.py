# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/test/api/trv2_dynamic.proto
"""Generated protocol buffer code."""
from chromite.third_party.google.protobuf.internal import builder as _builder
from chromite.third_party.google.protobuf import descriptor as _descriptor
from chromite.third_party.google.protobuf import descriptor_pool as _descriptor_pool
from chromite.third_party.google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.third_party.google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from chromite.third_party.google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from chromite.api.gen.chromiumos.build.api import container_metadata_pb2 as chromiumos_dot_build_dot_api_dot_container__metadata__pb2
from chromite.api.gen.chromiumos.test.api import cros_tool_runner_container_service_templates_pb2 as chromiumos_dot_test_dot_api_dot_cros__tool__runner__container__service__templates__pb2
from chromite.api.gen.chromiumos.test.api import provision_pb2 as chromiumos_dot_test_dot_api_dot_provision__pb2
from chromite.api.gen.chromiumos.test.api import cros_publish_service_pb2 as chromiumos_dot_test_dot_api_dot_cros__publish__service__pb2
from chromite.api.gen.chromiumos.test.api import cros_test_cli_pb2 as chromiumos_dot_test_dot_api_dot_cros__test__cli__pb2
from chromite.api.gen.chromiumos.test.api import test_suite_pb2 as chromiumos_dot_test_dot_api_dot_test__suite__pb2
from chromite.api.gen.chromiumos.test.api import post_test_service_pb2 as chromiumos_dot_test_dot_api_dot_post__test__service__pb2
from chromite.api.gen.chromiumos.test.api import generic_service_pb2 as chromiumos_dot_test_dot_api_dot_generic__service__pb2
from chromite.api.gen.chromiumos.test.lab.api import ip_endpoint_pb2 as chromiumos_dot_test_dot_lab_dot_api_dot_ip__endpoint__pb2
from chromite.api.gen.chromiumos.test.lab.api import dut_pb2 as chromiumos_dot_test_dot_lab_dot_api_dot_dut__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&chromiumos/test/api/trv2_dynamic.proto\x12\x13\x63hromiumos.test.api\x1a\x19google/protobuf/any.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a-chromiumos/build/api/container_metadata.proto\x1a\x46\x63hromiumos/test/api/cros_tool_runner_container_service_templates.proto\x1a#chromiumos/test/api/provision.proto\x1a.chromiumos/test/api/cros_publish_service.proto\x1a\'chromiumos/test/api/cros_test_cli.proto\x1a$chromiumos/test/api/test_suite.proto\x1a+chromiumos/test/api/post_test_service.proto\x1a)chromiumos/test/api/generic_service.proto\x1a)chromiumos/test/lab/api/ip_endpoint.proto\x1a!chromiumos/test/lab/api/dut.proto\"\x98\x05\n\x1c\x43rosTestRunnerDynamicRequest\x12/\n\x05\x62uild\x18\x01 \x01(\x0b\x32\x1e.chromiumos.test.api.BuildModeH\x00\x12\x39\n\x06params\x18\x03 \x01(\x0b\x32).chromiumos.test.api.CrosTestRunnerParams\x12M\n\rordered_tasks\x18\x04 \x03(\x0b\x32\x36.chromiumos.test.api.CrosTestRunnerDynamicRequest.Task\x1a\xab\x03\n\x04Task\x12I\n\x1aordered_container_requests\x18\x01 \x03(\x0b\x32%.chromiumos.test.api.ContainerRequest\x12\x37\n\tprovision\x18\x02 \x01(\x0b\x32\".chromiumos.test.api.ProvisionTaskH\x00\x12\x34\n\x08pre_test\x18\x03 \x01(\x0b\x32 .chromiumos.test.api.PreTestTaskH\x00\x12-\n\x04test\x18\x04 \x01(\x0b\x32\x1d.chromiumos.test.api.TestTaskH\x00\x12\x36\n\tpost_test\x18\x05 \x01(\x0b\x32!.chromiumos.test.api.PostTestTaskH\x00\x12\x33\n\x07publish\x18\x06 \x01(\x0b\x32 .chromiumos.test.api.PublishTaskH\x00\x12\x33\n\x07generic\x18\x08 \x01(\x0b\x32 .chromiumos.test.api.GenericTaskH\x00\x12\x10\n\x08required\x18\x07 \x01(\x08\x42\x06\n\x04taskB\x0f\n\rstart_request\"\xca\x03\n\x14\x43rosTestRunnerParams\x12\x33\n\x0btest_suites\x18\x01 \x03(\x0b\x32\x1e.chromiumos.test.api.TestSuite\x12\x43\n\x12\x63ontainer_metadata\x18\x02 \x01(\x0b\x32\'.chromiumos.build.api.ContainerMetadata\x12G\n\x07keyvals\x18\x03 \x03(\x0b\x32\x36.chromiumos.test.api.CrosTestRunnerParams.KeyvalsEntry\x12\x1e\n\x16\x63ontainer_metadata_key\x18\x04 \x01(\t\x12\x36\n\x0bprimary_dut\x18\x05 \x01(\x0b\x32!.chromiumos.test.lab.api.DutModel\x12\x39\n\x0e\x63ompanion_duts\x18\x06 \x03(\x0b\x32!.chromiumos.test.lab.api.DutModel\x12,\n\x08\x64\x65\x61\x64line\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x1a.\n\x0cKeyvalsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"@\n\tBuildMode\x12\x17\n\x0fparent_build_id\x18\x01 \x01(\x03\x12\x1a\n\x12parent_request_uid\x18\x02 \x01(\t\"\xb5\x02\n\rProvisionTask\x12<\n\x0fservice_address\x18\x01 \x01(\x0b\x32#.chromiumos.test.lab.api.IpEndpoint\x12\x45\n\x0fstartup_request\x18\x02 \x01(\x0b\x32,.chromiumos.test.api.ProvisionStartupRequest\x12<\n\x0finstall_request\x18\x03 \x01(\x0b\x32#.chromiumos.test.api.InstallRequest\x12\x35\n\x0c\x64ynamic_deps\x18\x04 \x03(\x0b\x32\x1f.chromiumos.test.api.DynamicDep\x12\x0e\n\x06target\x18\x05 \x01(\t\x12\x1a\n\x12\x64ynamic_identifier\x18\x06 \x01(\t\"\xce\x01\n\x0bPreTestTask\x12<\n\x0fservice_address\x18\x01 \x01(\x0b\x32#.chromiumos.test.lab.api.IpEndpoint\x12.\n\x10pre_test_request\x18\x02 \x01(\x0b\x32\x14.google.protobuf.Any\x12\x35\n\x0c\x64ynamic_deps\x18\x03 \x03(\x0b\x32\x1f.chromiumos.test.api.DynamicDep\x12\x1a\n\x12\x64ynamic_identifier\x18\x04 \x01(\t\"\xd7\x01\n\x08TestTask\x12<\n\x0fservice_address\x18\x01 \x01(\x0b\x32#.chromiumos.test.lab.api.IpEndpoint\x12:\n\x0ctest_request\x18\x02 \x01(\x0b\x32$.chromiumos.test.api.CrosTestRequest\x12\x35\n\x0c\x64ynamic_deps\x18\x03 \x03(\x0b\x32\x1f.chromiumos.test.api.DynamicDep\x12\x1a\n\x12\x64ynamic_identifier\x18\x04 \x01(\t\"\xa9\x03\n\x0cPostTestTask\x12<\n\x0fservice_address\x18\x01 \x01(\x0b\x32#.chromiumos.test.lab.api.IpEndpoint\x12/\n\x11post_test_request\x18\x02 \x01(\x0b\x32\x14.google.protobuf.Any\x12\x35\n\x0c\x64ynamic_deps\x18\x03 \x03(\x0b\x32\x1f.chromiumos.test.api.DynamicDep\x12\x45\n\x10start_up_request\x18\x06 \x01(\x0b\x32+.chromiumos.test.api.PostTestStartUpRequest\x12\x45\n\x14run_activity_request\x18\x04 \x01(\x0b\x32\'.chromiumos.test.api.RunActivityRequest\x12I\n\x16run_activities_request\x18\x07 \x01(\x0b\x32).chromiumos.test.api.RunActivitiesRequest\x12\x1a\n\x12\x64ynamic_identifier\x18\x05 \x01(\t\"\xdc\x01\n\x0bPublishTask\x12<\n\x0fservice_address\x18\x01 \x01(\x0b\x32#.chromiumos.test.lab.api.IpEndpoint\x12<\n\x0fpublish_request\x18\x02 \x01(\x0b\x32#.chromiumos.test.api.PublishRequest\x12\x35\n\x0c\x64ynamic_deps\x18\x03 \x03(\x0b\x32\x1f.chromiumos.test.api.DynamicDep\x12\x1a\n\x12\x64ynamic_identifier\x18\x04 \x01(\t\"\xdb\x02\n\x0bGenericTask\x12<\n\x0fservice_address\x18\x01 \x01(\x0b\x32#.chromiumos.test.lab.api.IpEndpoint\x12?\n\rstart_request\x18\x02 \x01(\x0b\x32(.chromiumos.test.api.GenericStartRequest\x12;\n\x0brun_request\x18\x03 \x01(\x0b\x32&.chromiumos.test.api.GenericRunRequest\x12=\n\x0cstop_request\x18\x04 \x01(\x0b\x32\'.chromiumos.test.api.GenericStopRequest\x12\x35\n\x0c\x64ynamic_deps\x18\x05 \x03(\x0b\x32\x1f.chromiumos.test.api.DynamicDep\x12\x1a\n\x12\x64ynamic_identifier\x18\x06 \x01(\t\"\xa3\x03\n\x10\x43ontainerRequest\x12\x1a\n\x12\x64ynamic_identifier\x18\x01 \x01(\t\x12\x30\n\tcontainer\x18\x02 \x01(\x0b\x32\x1d.chromiumos.test.api.Template\x12\x35\n\x0c\x64ynamic_deps\x18\x03 \x03(\x0b\x32\x1f.chromiumos.test.api.DynamicDep\x12?\n\x06inputs\x18\x04 \x03(\x0b\x32/.chromiumos.test.api.ContainerRequest.FileInput\x12\x0f\n\x07network\x18\x05 \x01(\t\x12\x1b\n\x13\x63ontainer_image_key\x18\x06 \x01(\t\x12\x1c\n\x14\x63ontainer_image_path\x18\x07 \x01(\t\x1a}\n\tFileInput\x12\x12\n\nidentifier\x18\x01 \x01(\t\x12%\n\x07\x63ontent\x18\x02 \x01(\x0b\x32\x14.google.protobuf.Any\x12\x35\n\x0c\x64ynamic_deps\x18\x03 \x03(\x0b\x32\x1f.chromiumos.test.api.DynamicDep\"(\n\nDynamicDep\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\tB/Z-go.chromium.org/chromiumos/config/go/test/apib\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chromiumos.test.api.trv2_dynamic_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z-go.chromium.org/chromiumos/config/go/test/api'
  _CROSTESTRUNNERPARAMS_KEYVALSENTRY._options = None
  _CROSTESTRUNNERPARAMS_KEYVALSENTRY._serialized_options = b'8\001'
  _CROSTESTRUNNERDYNAMICREQUEST._serialized_start=573
  _CROSTESTRUNNERDYNAMICREQUEST._serialized_end=1237
  _CROSTESTRUNNERDYNAMICREQUEST_TASK._serialized_start=793
  _CROSTESTRUNNERDYNAMICREQUEST_TASK._serialized_end=1220
  _CROSTESTRUNNERPARAMS._serialized_start=1240
  _CROSTESTRUNNERPARAMS._serialized_end=1698
  _CROSTESTRUNNERPARAMS_KEYVALSENTRY._serialized_start=1652
  _CROSTESTRUNNERPARAMS_KEYVALSENTRY._serialized_end=1698
  _BUILDMODE._serialized_start=1700
  _BUILDMODE._serialized_end=1764
  _PROVISIONTASK._serialized_start=1767
  _PROVISIONTASK._serialized_end=2076
  _PRETESTTASK._serialized_start=2079
  _PRETESTTASK._serialized_end=2285
  _TESTTASK._serialized_start=2288
  _TESTTASK._serialized_end=2503
  _POSTTESTTASK._serialized_start=2506
  _POSTTESTTASK._serialized_end=2931
  _PUBLISHTASK._serialized_start=2934
  _PUBLISHTASK._serialized_end=3154
  _GENERICTASK._serialized_start=3157
  _GENERICTASK._serialized_end=3504
  _CONTAINERREQUEST._serialized_start=3507
  _CONTAINERREQUEST._serialized_end=3926
  _CONTAINERREQUEST_FILEINPUT._serialized_start=3801
  _CONTAINERREQUEST_FILEINPUT._serialized_end=3926
  _DYNAMICDEP._serialized_start=3928
  _DYNAMICDEP._serialized_end=3968
# @@protoc_insertion_point(module_scope)
