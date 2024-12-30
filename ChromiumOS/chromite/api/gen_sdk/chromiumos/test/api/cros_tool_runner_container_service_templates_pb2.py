# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/test/api/cros_tool_runner_container_service_templates.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen_sdk.chromiumos.test.api import cros_provision_cli_pb2 as chromiumos_dot_test_dot_api_dot_cros__provision__cli__pb2
from chromite.api.gen_sdk.chromiumos.test.api import android_provision_pb2 as chromiumos_dot_test_dot_api_dot_android__provision__pb2
from chromite.api.gen_sdk.chromiumos.test.lab.api import ip_endpoint_pb2 as chromiumos_dot_test_dot_lab_dot_api_dot_ip__endpoint__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nFchromiumos/test/api/cros_tool_runner_container_service_templates.proto\x12\x13\x63hromiumos.test.api\x1a,chromiumos/test/api/cros_provision_cli.proto\x1a+chromiumos/test/api/android_provision.proto\x1a)chromiumos/test/lab/api/ip_endpoint.proto\"\x83\x06\n\x08Template\x12\x38\n\x08\x63ros_dut\x18\x01 \x01(\x0b\x32$.chromiumos.test.api.CrosDutTemplateH\x00\x12\x44\n\x0e\x63ros_provision\x18\x02 \x01(\x0b\x32*.chromiumos.test.api.CrosProvisionTemplateH\x00\x12:\n\tcros_test\x18\x03 \x01(\x0b\x32%.chromiumos.test.api.CrosTestTemplateH\x00\x12@\n\x0c\x63ros_publish\x18\x04 \x01(\x0b\x32(.chromiumos.test.api.CrosPublishTemplateH\x00\x12O\n\x11\x63ros_fw_provision\x18\x05 \x01(\x0b\x32\x32.chromiumos.test.api.CrosFirmwareProvisionTemplateH\x00\x12@\n\x0c\x63\x61\x63he_server\x18\x06 \x01(\x0b\x32(.chromiumos.test.api.CacheServerTemplateH\x00\x12G\n\x10\x63ros_test_finder\x18\x07 \x01(\x0b\x32+.chromiumos.test.api.CrosTestFinderTemplateH\x00\x12J\n\x11\x61ndroid_provision\x18\x08 \x01(\x0b\x32-.chromiumos.test.api.AndroidProvisionTemplateH\x00\x12\x37\n\x07generic\x18\t \x01(\x0b\x32$.chromiumos.test.api.GenericTemplateH\x00\x12I\n\x11\x63ros_vm_provision\x18\n \x01(\x0b\x32,.chromiumos.test.api.CrosVMProvisionTemplateH\x00\x12@\n\x0cpost_process\x18\x0b \x01(\x0b\x32(.chromiumos.test.api.PostProcessTemplateH\x00\x42\x0b\n\tcontainer\"\x92\x01\n\x0f\x43rosDutTemplate\x12\x39\n\x0c\x63\x61\x63he_server\x18\x03 \x01(\x0b\x32#.chromiumos.test.lab.api.IpEndpoint\x12\x38\n\x0b\x64ut_address\x18\x04 \x01(\x0b\x32#.chromiumos.test.lab.api.IpEndpointJ\x04\x08\x01\x10\x02J\x04\x08\x02\x10\x03\"e\n\x15\x43rosProvisionTemplate\x12@\n\rinput_request\x18\x03 \x01(\x0b\x32).chromiumos.test.api.CrosProvisionRequestJ\x04\x08\x01\x10\x02J\x04\x08\x02\x10\x03\"_\n\x18\x41ndroidProvisionTemplate\x12\x43\n\rinput_request\x18\x01 \x01(\x0b\x32,.chromiumos.test.api.AndroidProvisionRequest\"\x1e\n\x10\x43rosTestTemplateJ\x04\x08\x01\x10\x02J\x04\x08\x02\x10\x03\"\x18\n\x16\x43rosTestFinderTemplate\"\x19\n\x17\x43rosVMProvisionTemplate\"\x91\x01\n\x0fGenericTemplate\x12\x13\n\x0b\x62inary_name\x18\x01 \x01(\t\x12\x13\n\x0b\x62inary_args\x18\x02 \x03(\t\x12\x1b\n\x13\x64ocker_artifact_dir\x18\x03 \x01(\t\x12\x1a\n\x12\x61\x64\x64itional_volumes\x18\x04 \x03(\t\x12\x0e\n\x06\x65xpose\x18\x05 \x03(\t\x12\x0b\n\x03\x65nv\x18\x06 \x03(\t\"[\n\x13\x43\x61\x63heServerTemplate\x12!\n\x17service_account_keyfile\x18\x01 \x01(\tH\x00\x42!\n\x1f\x61pplication_default_credentials\"\xe8\x01\n\x13\x43rosPublishTemplate\x12J\n\x0cpublish_type\x18\x01 \x01(\x0e\x32\x34.chromiumos.test.api.CrosPublishTemplate.PublishType\x12\x17\n\x0fpublish_src_dir\x18\x02 \x01(\t\"l\n\x0bPublishType\x12\x17\n\x13PUBLISH_UNSPECIFIED\x10\x00\x12\x0f\n\x0bPUBLISH_GCS\x10\x01\x12\x0f\n\x0bPUBLISH_TKO\x10\x02\x12\x0f\n\x0bPUBLISH_RDB\x10\x03\x12\x11\n\rPUBLISH_CPCON\x10\x04\"\x1f\n\x1d\x43rosFirmwareProvisionTemplate\"3\n\x13PostProcessTemplate\x12\x1c\n\x14post_process_src_dir\x18\x01 \x01(\tB/Z-go.chromium.org/chromiumos/config/go/test/apib\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chromiumos.test.api.cros_tool_runner_container_service_templates_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z-go.chromium.org/chromiumos/config/go/test/api'
  _globals['_TEMPLATE']._serialized_start=230
  _globals['_TEMPLATE']._serialized_end=1001
  _globals['_CROSDUTTEMPLATE']._serialized_start=1004
  _globals['_CROSDUTTEMPLATE']._serialized_end=1150
  _globals['_CROSPROVISIONTEMPLATE']._serialized_start=1152
  _globals['_CROSPROVISIONTEMPLATE']._serialized_end=1253
  _globals['_ANDROIDPROVISIONTEMPLATE']._serialized_start=1255
  _globals['_ANDROIDPROVISIONTEMPLATE']._serialized_end=1350
  _globals['_CROSTESTTEMPLATE']._serialized_start=1352
  _globals['_CROSTESTTEMPLATE']._serialized_end=1382
  _globals['_CROSTESTFINDERTEMPLATE']._serialized_start=1384
  _globals['_CROSTESTFINDERTEMPLATE']._serialized_end=1408
  _globals['_CROSVMPROVISIONTEMPLATE']._serialized_start=1410
  _globals['_CROSVMPROVISIONTEMPLATE']._serialized_end=1435
  _globals['_GENERICTEMPLATE']._serialized_start=1438
  _globals['_GENERICTEMPLATE']._serialized_end=1583
  _globals['_CACHESERVERTEMPLATE']._serialized_start=1585
  _globals['_CACHESERVERTEMPLATE']._serialized_end=1676
  _globals['_CROSPUBLISHTEMPLATE']._serialized_start=1679
  _globals['_CROSPUBLISHTEMPLATE']._serialized_end=1911
  _globals['_CROSPUBLISHTEMPLATE_PUBLISHTYPE']._serialized_start=1803
  _globals['_CROSPUBLISHTEMPLATE_PUBLISHTYPE']._serialized_end=1911
  _globals['_CROSFIRMWAREPROVISIONTEMPLATE']._serialized_start=1913
  _globals['_CROSFIRMWAREPROVISIONTEMPLATE']._serialized_end=1944
  _globals['_POSTPROCESSTEMPLATE']._serialized_start=1946
  _globals['_POSTPROCESSTEMPLATE']._serialized_end=1997
# @@protoc_insertion_point(module_scope)
