# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromite/api/test.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen_sdk.chromite.api import build_api_pb2 as chromite_dot_api_dot_build__api__pb2
from chromite.api.gen_sdk.chromite.api import sysroot_pb2 as chromite_dot_api_dot_sysroot__pb2
from chromite.api.gen_sdk.chromiumos import common_pb2 as chromiumos_dot_common__pb2
from chromite.api.gen_sdk.chromiumos import metrics_pb2 as chromiumos_dot_metrics__pb2
from chromite.api.gen_sdk.chromiumos.build.api import container_metadata_pb2 as chromiumos_dot_build_dot_api_dot_container__metadata__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17\x63hromite/api/test.proto\x12\x0c\x63hromite.api\x1a\x1c\x63hromite/api/build_api.proto\x1a\x1a\x63hromite/api/sysroot.proto\x1a\x17\x63hromiumos/common.proto\x1a\x18\x63hromiumos/metrics.proto\x1a-chromiumos/build/api/container_metadata.proto\"\xcf\x02\n\x1fTestServiceContainerBuildResult\x12\x0c\n\x04name\x18\x01 \x01(\t\x12H\n\x07success\x18\x02 \x01(\x0b\x32\x35.chromite.api.TestServiceContainerBuildResult.SuccessH\x00\x12H\n\x07\x66\x61ilure\x18\x03 \x01(\x0b\x32\x35.chromite.api.TestServiceContainerBuildResult.FailureH\x00\x1a^\n\x07Success\x12<\n\nimage_info\x18\x02 \x01(\x0b\x32(.chromiumos.build.api.ContainerImageInfo\x12\x15\n\rregistry_path\x18\x01 \x01(\t\x1a \n\x07\x46\x61ilure\x12\x15\n\rerror_message\x18\x01 \x01(\tB\x08\n\x06result\"\xd6\x03\n!BuildTestServiceContainersRequest\x12-\n\x0c\x62uild_target\x18\x01 \x01(\x0b\x32\x17.chromiumos.BuildTarget\x12\"\n\x06\x63hroot\x18\x02 \x01(\x0b\x32\x12.chromiumos.Chroot\x12\x0f\n\x07version\x18\x03 \x01(\t\x12\x37\n\nrepository\x18\x04 \x01(\x0b\x32#.chromiumos.build.api.GcrRepository\x12\x0c\n\x04tags\x18\x05 \x03(\t\x12K\n\x06labels\x18\x06 \x03(\x0b\x32;.chromite.api.BuildTestServiceContainersRequest.LabelsEntry\x12Q\n\x0c\x62uilder_type\x18\x07 \x01(\x0e\x32;.chromite.api.BuildTestServiceContainersRequest.BuilderType\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"7\n\x0b\x42uilderType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\n\n\x06PUBLIC\x10\x01\x12\x0b\n\x07PRIVATE\x10\x02\"d\n\"BuildTestServiceContainersResponse\x12>\n\x07results\x18\x01 \x03(\x0b\x32-.chromite.api.TestServiceContainerBuildResult\"\x97\x04\n\x1a\x42uildTargetUnitTestRequest\x12-\n\x0c\x62uild_target\x18\x01 \x01(\x0b\x32\x17.chromiumos.BuildTarget\x12\"\n\x06\x63hroot\x18\x03 \x01(\x0b\x32\x12.chromiumos.Chroot\x12=\n\x05\x66lags\x18\x04 \x01(\x0b\x32..chromite.api.BuildTargetUnitTestRequest.Flags\x12)\n\x08packages\x18\x06 \x03(\x0b\x32\x17.chromiumos.PackageInfo\x12\x32\n\x11package_blocklist\x18\x07 \x03(\x0b\x32\x17.chromiumos.PackageInfo\x12,\n\x0cresults_path\x18\x08 \x01(\x0b\x32\x16.chromiumos.ResultPath\x1a\xc0\x01\n\x05\x46lags\x12\x15\n\rempty_sysroot\x18\x01 \x01(\x08\x12\x19\n\x11toolchain_changed\x18\x02 \x01(\x08\x12\x15\n\rcode_coverage\x18\x03 \x01(\x08\x12\"\n\x1atestable_packages_optional\x18\x04 \x01(\x08\x12\x1f\n\x17\x66ilter_only_cros_workon\x18\x05 \x01(\x08\x12\x1a\n\x12rust_code_coverage\x18\x06 \x01(\x08\x12\r\n\x05\x62\x61zel\x18\x07 \x01(\x08J\x04\x08\x02\x10\x03J\x04\x08\x05\x10\x06R\x0bresult_path\"\xaf\x01\n\x1b\x42uildTargetUnitTestResponse\x12\'\n\x06\x65vents\x18\x03 \x03(\x0b\x32\x17.chromiumos.MetricEvent\x12<\n\x13\x66\x61iled_package_data\x18\x04 \x03(\x0b\x32\x1f.chromite.api.FailedPackageDataJ\x04\x08\x01\x10\x02J\x04\x08\x02\x10\x03R\x0ctarball_pathR\x0f\x66\x61iled_packages\"=\n\x17\x43hromiteUnitTestRequest\x12\"\n\x06\x63hroot\x18\x01 \x01(\x0b\x32\x12.chromiumos.Chroot\"\x1a\n\x18\x43hromiteUnitTestResponse\";\n\x15\x43hromitePytestRequest\x12\"\n\x06\x63hroot\x18\x01 \x01(\x0b\x32\x12.chromiumos.Chroot\"\x18\n\x16\x43hromitePytestResponse\"2\n\x10\x42\x61zelTestRequest\x12\x1e\n\x16\x62\x61zel_output_user_root\x18\x01 \x01(\t\"\x13\n\x11\x42\x61zelTestResponse\"<\n\x16\x43rosSigningTestRequest\x12\"\n\x06\x63hroot\x18\x01 \x01(\x0b\x32\x12.chromiumos.Chroot\"\x19\n\x17\x43rosSigningTestResponse\"\xd2\x03\n\rVmTestRequest\x12-\n\x0c\x62uild_target\x18\x01 \x01(\x0b\x32\x17.chromiumos.BuildTarget\x12\"\n\x06\x63hroot\x18\x02 \x01(\x0b\x32\x12.chromiumos.Chroot\x12!\n\x07vm_path\x18\x03 \x01(\x0b\x32\x10.chromiumos.Path\x12;\n\x0bssh_options\x18\x04 \x01(\x0b\x32&.chromite.api.VmTestRequest.SshOptions\x12=\n\x0ctest_harness\x18\x05 \x01(\x0e\x32\'.chromite.api.VmTestRequest.TestHarness\x12\x34\n\x08vm_tests\x18\x06 \x03(\x0b\x32\".chromite.api.VmTestRequest.VmTest\x1a\x46\n\nSshOptions\x12*\n\x10private_key_path\x18\x01 \x01(\x0b\x32\x10.chromiumos.Path\x12\x0c\n\x04port\x18\x02 \x01(\x05\x1a\x19\n\x06VmTest\x12\x0f\n\x07pattern\x18\x01 \x01(\t\"6\n\x0bTestHarness\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x08\n\x04TAST\x10\x01\x12\x0c\n\x08\x41UTOTEST\x10\x02\"\x10\n\x0eVmTestResponse\">\n\x18RulesCrosUnitTestRequest\x12\"\n\x06\x63hroot\x18\x01 \x01(\x0b\x32\x12.chromiumos.Chroot\"\x1b\n\x19RulesCrosUnitTestResponse\"\x8b\x01\n\x1fSimpleChromeWorkflowTestRequest\x12&\n\x07sysroot\x18\x01 \x01(\x0b\x32\x15.chromite.api.Sysroot\x12\x13\n\x0b\x63hrome_root\x18\x02 \x01(\t\x12+\n\x0bgoma_config\x18\x03 \x01(\x0b\x32\x16.chromiumos.GomaConfig\"\"\n SimpleChromeWorkflowTestResponse2\xb6\x07\n\x0bTestService\x12\x87\x01\n\x1a\x42uildTestServiceContainers\x12/.chromite.api.BuildTestServiceContainersRequest\x1a\x30.chromite.api.BuildTestServiceContainersResponse\"\x06\xc2\xed\x1a\x02\x10\x02\x12j\n\x13\x42uildTargetUnitTest\x12(.chromite.api.BuildTargetUnitTestRequest\x1a).chromite.api.BuildTargetUnitTestResponse\x12\x61\n\x10\x43hromiteUnitTest\x12%.chromite.api.ChromiteUnitTestRequest\x1a&.chromite.api.ChromiteUnitTestResponse\x12[\n\x0e\x43hromitePytest\x12#.chromite.api.ChromitePytestRequest\x1a$.chromite.api.ChromitePytestResponse\x12T\n\tBazelTest\x12\x1e.chromite.api.BazelTestRequest\x1a\x1f.chromite.api.BazelTestResponse\"\x06\xc2\xed\x1a\x02\x10\x02\x12^\n\x0f\x43rosSigningTest\x12$.chromite.api.CrosSigningTestRequest\x1a%.chromite.api.CrosSigningTestResponse\x12\x43\n\x06VmTest\x12\x1b.chromite.api.VmTestRequest\x1a\x1c.chromite.api.VmTestResponse\x12\x64\n\x11RulesCrosUnitTest\x12&.chromite.api.RulesCrosUnitTestRequest\x1a\'.chromite.api.RulesCrosUnitTestResponse\x12\x81\x01\n\x18SimpleChromeWorkflowTest\x12-.chromite.api.SimpleChromeWorkflowTestRequest\x1a..chromite.api.SimpleChromeWorkflowTestResponse\"\x06\xc2\xed\x1a\x02\x10\x02\x1a\x0c\xc2\xed\x1a\x08\n\x04test\x10\x01\x42\x38Z6go.chromium.org/chromiumos/infra/proto/go/chromite/apib\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chromite.api.test_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z6go.chromium.org/chromiumos/infra/proto/go/chromite/api'
  _BUILDTESTSERVICECONTAINERSREQUEST_LABELSENTRY._options = None
  _BUILDTESTSERVICECONTAINERSREQUEST_LABELSENTRY._serialized_options = b'8\001'
  _TESTSERVICE._options = None
  _TESTSERVICE._serialized_options = b'\302\355\032\010\n\004test\020\001'
  _TESTSERVICE.methods_by_name['BuildTestServiceContainers']._options = None
  _TESTSERVICE.methods_by_name['BuildTestServiceContainers']._serialized_options = b'\302\355\032\002\020\002'
  _TESTSERVICE.methods_by_name['BazelTest']._options = None
  _TESTSERVICE.methods_by_name['BazelTest']._serialized_options = b'\302\355\032\002\020\002'
  _TESTSERVICE.methods_by_name['SimpleChromeWorkflowTest']._options = None
  _TESTSERVICE.methods_by_name['SimpleChromeWorkflowTest']._serialized_options = b'\302\355\032\002\020\002'
  _globals['_TESTSERVICECONTAINERBUILDRESULT']._serialized_start=198
  _globals['_TESTSERVICECONTAINERBUILDRESULT']._serialized_end=533
  _globals['_TESTSERVICECONTAINERBUILDRESULT_SUCCESS']._serialized_start=395
  _globals['_TESTSERVICECONTAINERBUILDRESULT_SUCCESS']._serialized_end=489
  _globals['_TESTSERVICECONTAINERBUILDRESULT_FAILURE']._serialized_start=491
  _globals['_TESTSERVICECONTAINERBUILDRESULT_FAILURE']._serialized_end=523
  _globals['_BUILDTESTSERVICECONTAINERSREQUEST']._serialized_start=536
  _globals['_BUILDTESTSERVICECONTAINERSREQUEST']._serialized_end=1006
  _globals['_BUILDTESTSERVICECONTAINERSREQUEST_LABELSENTRY']._serialized_start=904
  _globals['_BUILDTESTSERVICECONTAINERSREQUEST_LABELSENTRY']._serialized_end=949
  _globals['_BUILDTESTSERVICECONTAINERSREQUEST_BUILDERTYPE']._serialized_start=951
  _globals['_BUILDTESTSERVICECONTAINERSREQUEST_BUILDERTYPE']._serialized_end=1006
  _globals['_BUILDTESTSERVICECONTAINERSRESPONSE']._serialized_start=1008
  _globals['_BUILDTESTSERVICECONTAINERSRESPONSE']._serialized_end=1108
  _globals['_BUILDTARGETUNITTESTREQUEST']._serialized_start=1111
  _globals['_BUILDTARGETUNITTESTREQUEST']._serialized_end=1646
  _globals['_BUILDTARGETUNITTESTREQUEST_FLAGS']._serialized_start=1429
  _globals['_BUILDTARGETUNITTESTREQUEST_FLAGS']._serialized_end=1621
  _globals['_BUILDTARGETUNITTESTRESPONSE']._serialized_start=1649
  _globals['_BUILDTARGETUNITTESTRESPONSE']._serialized_end=1824
  _globals['_CHROMITEUNITTESTREQUEST']._serialized_start=1826
  _globals['_CHROMITEUNITTESTREQUEST']._serialized_end=1887
  _globals['_CHROMITEUNITTESTRESPONSE']._serialized_start=1889
  _globals['_CHROMITEUNITTESTRESPONSE']._serialized_end=1915
  _globals['_CHROMITEPYTESTREQUEST']._serialized_start=1917
  _globals['_CHROMITEPYTESTREQUEST']._serialized_end=1976
  _globals['_CHROMITEPYTESTRESPONSE']._serialized_start=1978
  _globals['_CHROMITEPYTESTRESPONSE']._serialized_end=2002
  _globals['_BAZELTESTREQUEST']._serialized_start=2004
  _globals['_BAZELTESTREQUEST']._serialized_end=2054
  _globals['_BAZELTESTRESPONSE']._serialized_start=2056
  _globals['_BAZELTESTRESPONSE']._serialized_end=2075
  _globals['_CROSSIGNINGTESTREQUEST']._serialized_start=2077
  _globals['_CROSSIGNINGTESTREQUEST']._serialized_end=2137
  _globals['_CROSSIGNINGTESTRESPONSE']._serialized_start=2139
  _globals['_CROSSIGNINGTESTRESPONSE']._serialized_end=2164
  _globals['_VMTESTREQUEST']._serialized_start=2167
  _globals['_VMTESTREQUEST']._serialized_end=2633
  _globals['_VMTESTREQUEST_SSHOPTIONS']._serialized_start=2480
  _globals['_VMTESTREQUEST_SSHOPTIONS']._serialized_end=2550
  _globals['_VMTESTREQUEST_VMTEST']._serialized_start=2552
  _globals['_VMTESTREQUEST_VMTEST']._serialized_end=2577
  _globals['_VMTESTREQUEST_TESTHARNESS']._serialized_start=2579
  _globals['_VMTESTREQUEST_TESTHARNESS']._serialized_end=2633
  _globals['_VMTESTRESPONSE']._serialized_start=2635
  _globals['_VMTESTRESPONSE']._serialized_end=2651
  _globals['_RULESCROSUNITTESTREQUEST']._serialized_start=2653
  _globals['_RULESCROSUNITTESTREQUEST']._serialized_end=2715
  _globals['_RULESCROSUNITTESTRESPONSE']._serialized_start=2717
  _globals['_RULESCROSUNITTESTRESPONSE']._serialized_end=2744
  _globals['_SIMPLECHROMEWORKFLOWTESTREQUEST']._serialized_start=2747
  _globals['_SIMPLECHROMEWORKFLOWTESTREQUEST']._serialized_end=2886
  _globals['_SIMPLECHROMEWORKFLOWTESTRESPONSE']._serialized_start=2888
  _globals['_SIMPLECHROMEWORKFLOWTESTRESPONSE']._serialized_end=2922
  _globals['_TESTSERVICE']._serialized_start=2925
  _globals['_TESTSERVICE']._serialized_end=3875
# @@protoc_insertion_point(module_scope)