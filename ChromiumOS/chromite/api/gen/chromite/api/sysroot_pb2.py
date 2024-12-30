# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromite/api/sysroot.proto
"""Generated protocol buffer code."""
from chromite.third_party.google.protobuf.internal import builder as _builder
from chromite.third_party.google.protobuf import descriptor as _descriptor
from chromite.third_party.google.protobuf import descriptor_pool as _descriptor_pool
from chromite.third_party.google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen.chromite.api import build_api_pb2 as chromite_dot_api_dot_build__api__pb2
from chromite.api.gen.chromiumos import common_pb2 as chromiumos_dot_common__pb2
from chromite.api.gen.chromiumos import metrics_pb2 as chromiumos_dot_metrics__pb2
from chromite.api.gen.chromiumos import prebuilts_cloud_pb2 as chromiumos_dot_prebuilts__cloud__pb2
from chromite.third_party.google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1a\x63hromite/api/sysroot.proto\x12\x0c\x63hromite.api\x1a\x1c\x63hromite/api/build_api.proto\x1a\x17\x63hromiumos/common.proto\x1a\x18\x63hromiumos/metrics.proto\x1a chromiumos/prebuilts_cloud.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"F\n\x07Sysroot\x12\x0c\n\x04path\x18\x01 \x01(\t\x12-\n\x0c\x62uild_target\x18\x02 \x01(\x0b\x32\x17.chromiumos.BuildTarget\"\x17\n\x07Profile\x12\x0c\n\x04name\x18\x01 \x01(\t\"\x93\x03\n\x14SysrootCreateRequest\x12-\n\x0c\x62uild_target\x18\x01 \x01(\x0b\x32\x17.chromiumos.BuildTarget\x12\x37\n\x05\x66lags\x18\x02 \x01(\x0b\x32(.chromite.api.SysrootCreateRequest.Flags\x12&\n\x07profile\x18\x03 \x01(\x0b\x32\x15.chromite.api.Profile\x12\"\n\x06\x63hroot\x18\x04 \x01(\x0b\x32\x12.chromiumos.Chroot\x12I\n\x1b\x62inhost_lookup_service_data\x18\x06 \x01(\x0b\x32$.chromiumos.BinhostLookupServiceData\x1a\x65\n\x05\x46lags\x12\x16\n\x0e\x63hroot_current\x18\x01 \x01(\x08\x12\x0f\n\x07replace\x18\x02 \x01(\x08\x12\x19\n\x11toolchain_changed\x18\x03 \x01(\x08\x12\x18\n\x10use_cq_prebuilts\x18\x04 \x01(\x08J\x04\x08\x05\x10\x06R\x0fpackage_indexes\"?\n\x15SysrootCreateResponse\x12&\n\x07sysroot\x18\x01 \x01(\x0b\x32\x15.chromite.api.Sysroot\"q\n\x1cGetTargetArchitectureRequest\x12-\n\x0c\x62uild_target\x18\x01 \x01(\x0b\x32\x17.chromiumos.BuildTarget\x12\"\n\x06\x63hroot\x18\x02 \x01(\x0b\x32\x12.chromiumos.Chroot\"5\n\x1dGetTargetArchitectureResponse\x12\x14\n\x0c\x61rchitecture\x18\x01 \x01(\t\"\xc9\x01\n\x1dSysrootGenerateArchiveRequest\x12-\n\x0c\x62uild_target\x18\x01 \x01(\x0b\x32\x17.chromiumos.BuildTarget\x12\"\n\x06\x63hroot\x18\x02 \x01(\x0b\x32\x12.chromiumos.Chroot\x12)\n\x08packages\x18\x03 \x03(\x0b\x32\x17.chromiumos.PackageInfo\x12*\n\ntarget_dir\x18\x04 \x01(\x0b\x32\x16.chromiumos.ResultPath\"K\n\x1eSysrootGenerateArchiveResponse\x12)\n\x0fsysroot_archive\x18\x01 \x01(\x0b\x32\x10.chromiumos.Path\"\x9c\x01\n\x1cSysrootExtractArchiveRequest\x12\"\n\x06\x63hroot\x18\x01 \x01(\x0b\x32\x12.chromiumos.Chroot\x12-\n\x0c\x62uild_target\x18\x02 \x01(\x0b\x32\x17.chromiumos.BuildTarget\x12)\n\x0fsysroot_archive\x18\x03 \x01(\x0b\x32\x10.chromiumos.Path\"J\n\x1dSysrootExtractArchiveResponse\x12)\n\x0fsysroot_archive\x18\x01 \x01(\x0b\x32\x10.chromiumos.Path\"\x8a\x02\n\x17InstallToolchainRequest\x12&\n\x07sysroot\x18\x01 \x01(\x0b\x32\x15.chromite.api.Sysroot\x12:\n\x05\x66lags\x18\x02 \x01(\x0b\x32+.chromite.api.InstallToolchainRequest.Flags\x12\"\n\x06\x63hroot\x18\x03 \x01(\x0b\x32\x12.chromiumos.Chroot\x12+\n\x0bresult_path\x18\x04 \x01(\x0b\x32\x16.chromiumos.ResultPath\x1a:\n\x05\x46lags\x12\x16\n\x0e\x63ompile_source\x18\x01 \x01(\x08\x12\x19\n\x11toolchain_changed\x18\x02 \x01(\x08\"o\n\x18InstallToolchainResponse\x12<\n\x13\x66\x61iled_package_data\x18\x04 \x03(\x0b\x32\x1f.chromite.api.FailedPackageDataJ\x04\x08\x01\x10\x02R\x0f\x66\x61iled_packages\"\x8c\x07\n\x16InstallPackagesRequest\x12&\n\x07sysroot\x18\x01 \x01(\x0b\x32\x15.chromite.api.Sysroot\x12\x39\n\x05\x66lags\x18\x02 \x01(\x0b\x32*.chromite.api.InstallPackagesRequest.Flags\x12)\n\x08packages\x18\x03 \x03(\x0b\x32\x17.chromiumos.PackageInfo\x12\"\n\x06\x63hroot\x18\x04 \x01(\x0b\x32\x12.chromiumos.Chroot\x12&\n\tuse_flags\x18\x05 \x03(\x0b\x32\x13.chromiumos.UseFlag\x12+\n\x0bgoma_config\x18\x06 \x01(\x0b\x32\x16.chromiumos.GomaConfig\x12\x37\n\x11remoteexec_config\x18\x08 \x01(\x0b\x32\x1c.chromiumos.RemoteexecConfig\x12+\n\x0bresult_path\x18\t \x01(\x0b\x32\x16.chromiumos.ResultPath\x12H\n\rbazel_targets\x18\n \x01(\x0e\x32\x31.chromite.api.InstallPackagesRequest.BazelTargets\x12I\n\x1b\x62inhost_lookup_service_data\x18\x0b \x01(\x0b\x32$.chromiumos.BinhostLookupServiceData\x12\x35\n\x11timeout_timestamp\x18\x0c \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x1a\xe8\x01\n\x05\x46lags\x12\x16\n\x0e\x63ompile_source\x18\x01 \x01(\x08\x12\x10\n\x08use_goma\x18\x03 \x01(\x08\x12\x19\n\x11toolchain_changed\x18\x04 \x01(\x08\x12\x0e\n\x06\x64ryrun\x18\x05 \x01(\x08\x12\x0e\n\x06workon\x18\x07 \x01(\x08\x12\r\n\x05\x62\x61zel\x18\x08 \x01(\x08\x12\x1f\n\x17skip_clean_package_dirs\x18\t \x01(\x08\x12\"\n\x1a\x62\x61zel_use_remote_execution\x18\n \x01(\x08J\x04\x08\x02\x10\x03J\x04\x08\x06\x10\x07R\nevent_fileR\x0euse_remoteexec\"7\n\x0c\x42\x61zelTargets\x12\x1d\n\x19\x42\x41ZEL_TARGETS_UNSPECIFIED\x10\x00\x12\x08\n\x04LITE\x10\x01J\x04\x08\x07\x10\x08R\x0fpackage_indexes\"\x89\x02\n\x17InstallPackagesResponse\x12\'\n\x06\x65vents\x18\x02 \x03(\x0b\x32\x17.chromiumos.MetricEvent\x12\x31\n\x0egoma_artifacts\x18\x03 \x01(\x0b\x32\x19.chromiumos.GomaArtifacts\x12<\n\x13\x66\x61iled_package_data\x18\x04 \x03(\x0b\x32\x1f.chromite.api.FailedPackageData\x12=\n\x14remoteexec_artifacts\x18\x05 \x01(\x0b\x32\x1f.chromiumos.RemoteexecArtifactsJ\x04\x08\x01\x10\x02R\x0f\x66\x61iled_packages\"^\n\x11\x46\x61iledPackageData\x12%\n\x04name\x18\x01 \x01(\x0b\x32\x17.chromiumos.PackageInfo\x12\"\n\x08log_path\x18\x02 \x01(\x0b\x32\x10.chromiumos.Path\"\xb4\x01\n CreateSimpleChromeSysrootRequest\x12-\n\x0c\x62uild_target\x18\x01 \x01(\x0b\x32\x17.chromiumos.BuildTarget\x12\x11\n\tuse_flags\x18\x02 \x03(\t\x12*\n\ntarget_dir\x18\x03 \x01(\x0b\x32\x16.chromiumos.ResultPath\x12\"\n\x06\x63hroot\x18\x04 \x01(\x0b\x32\x12.chromiumos.Chroot\"N\n!CreateSimpleChromeSysrootResponse\x12)\n\x0fsysroot_archive\x18\x01 \x01(\x0b\x32\x10.chromiumos.Path2\x80\x06\n\x0eSysrootService\x12Q\n\x06\x43reate\x12\".chromite.api.SysrootCreateRequest\x1a#.chromite.api.SysrootCreateResponse\x12p\n\x15GetTargetArchitecture\x12*.chromite.api.GetTargetArchitectureRequest\x1a+.chromite.api.GetTargetArchitectureResponse\x12l\n\x0fGenerateArchive\x12+.chromite.api.SysrootGenerateArchiveRequest\x1a,.chromite.api.SysrootGenerateArchiveResponse\x12i\n\x0e\x45xtractArchive\x12*.chromite.api.SysrootExtractArchiveRequest\x1a+.chromite.api.SysrootExtractArchiveResponse\x12\x61\n\x10InstallToolchain\x12%.chromite.api.InstallToolchainRequest\x1a&.chromite.api.InstallToolchainResponse\x12^\n\x0fInstallPackages\x12$.chromite.api.InstallPackagesRequest\x1a%.chromite.api.InstallPackagesResponse\x12|\n\x19\x43reateSimpleChromeSysroot\x12..chromite.api.CreateSimpleChromeSysrootRequest\x1a/.chromite.api.CreateSimpleChromeSysrootResponse\x1a\x0f\xc2\xed\x1a\x0b\n\x07sysroot\x10\x01\x42\x38Z6go.chromium.org/chromiumos/infra/proto/go/chromite/apib\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chromite.api.sysroot_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z6go.chromium.org/chromiumos/infra/proto/go/chromite/api'
  _SYSROOTSERVICE._options = None
  _SYSROOTSERVICE._serialized_options = b'\302\355\032\013\n\007sysroot\020\001'
  _SYSROOT._serialized_start=192
  _SYSROOT._serialized_end=262
  _PROFILE._serialized_start=264
  _PROFILE._serialized_end=287
  _SYSROOTCREATEREQUEST._serialized_start=290
  _SYSROOTCREATEREQUEST._serialized_end=693
  _SYSROOTCREATEREQUEST_FLAGS._serialized_start=569
  _SYSROOTCREATEREQUEST_FLAGS._serialized_end=670
  _SYSROOTCREATERESPONSE._serialized_start=695
  _SYSROOTCREATERESPONSE._serialized_end=758
  _GETTARGETARCHITECTUREREQUEST._serialized_start=760
  _GETTARGETARCHITECTUREREQUEST._serialized_end=873
  _GETTARGETARCHITECTURERESPONSE._serialized_start=875
  _GETTARGETARCHITECTURERESPONSE._serialized_end=928
  _SYSROOTGENERATEARCHIVEREQUEST._serialized_start=931
  _SYSROOTGENERATEARCHIVEREQUEST._serialized_end=1132
  _SYSROOTGENERATEARCHIVERESPONSE._serialized_start=1134
  _SYSROOTGENERATEARCHIVERESPONSE._serialized_end=1209
  _SYSROOTEXTRACTARCHIVEREQUEST._serialized_start=1212
  _SYSROOTEXTRACTARCHIVEREQUEST._serialized_end=1368
  _SYSROOTEXTRACTARCHIVERESPONSE._serialized_start=1370
  _SYSROOTEXTRACTARCHIVERESPONSE._serialized_end=1444
  _INSTALLTOOLCHAINREQUEST._serialized_start=1447
  _INSTALLTOOLCHAINREQUEST._serialized_end=1713
  _INSTALLTOOLCHAINREQUEST_FLAGS._serialized_start=1655
  _INSTALLTOOLCHAINREQUEST_FLAGS._serialized_end=1713
  _INSTALLTOOLCHAINRESPONSE._serialized_start=1715
  _INSTALLTOOLCHAINRESPONSE._serialized_end=1826
  _INSTALLPACKAGESREQUEST._serialized_start=1829
  _INSTALLPACKAGESREQUEST._serialized_end=2737
  _INSTALLPACKAGESREQUEST_FLAGS._serialized_start=2425
  _INSTALLPACKAGESREQUEST_FLAGS._serialized_end=2657
  _INSTALLPACKAGESREQUEST_BAZELTARGETS._serialized_start=2659
  _INSTALLPACKAGESREQUEST_BAZELTARGETS._serialized_end=2714
  _INSTALLPACKAGESRESPONSE._serialized_start=2740
  _INSTALLPACKAGESRESPONSE._serialized_end=3005
  _FAILEDPACKAGEDATA._serialized_start=3007
  _FAILEDPACKAGEDATA._serialized_end=3101
  _CREATESIMPLECHROMESYSROOTREQUEST._serialized_start=3104
  _CREATESIMPLECHROMESYSROOTREQUEST._serialized_end=3284
  _CREATESIMPLECHROMESYSROOTRESPONSE._serialized_start=3286
  _CREATESIMPLECHROMESYSROOTRESPONSE._serialized_end=3364
  _SYSROOTSERVICE._serialized_start=3367
  _SYSROOTSERVICE._serialized_end=4135
# @@protoc_insertion_point(module_scope)
