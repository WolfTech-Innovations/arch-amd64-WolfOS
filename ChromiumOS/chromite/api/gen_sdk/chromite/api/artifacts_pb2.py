# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromite/api/artifacts.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1c\x63hromite/api/artifacts.proto\x12\x0c\x63hromite.api\x1a\x1c\x63hromite/api/build_api.proto\x1a\x1a\x63hromite/api/sysroot.proto\x1a\x17\x63hromiumos/common.proto\"A\n\x08\x41rtifact\x12\x0c\n\x04path\x18\x01 \x01(\t\x12\'\n\rartifact_path\x18\x02 \x01(\x0b\x32\x10.chromiumos.Path\"W\n\x0b\x44ockerBuild\x12\x12\n\nimage_name\x18\x01 \x01(\t\x12\x18\n\x10\x64ocker_file_path\x18\x02 \x01(\t\x12\x1a\n\x12\x62uild_context_path\x18\x03 \x01(\t\"\xb3\x01\n\x17PrepareForBuildResponse\x12M\n\x0f\x62uild_relevance\x18\x01 \x01(\x0e\x32\x34.chromite.api.PrepareForBuildResponse.BuildRelevance\"I\n\x0e\x42uildRelevance\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\n\n\x06NEEDED\x10\x01\x12\x0b\n\x07UNKNOWN\x10\x02\x12\r\n\tPOINTLESS\x10\x03\"\xb6\x01\n\x11\x42uildSetupRequest\x12\"\n\x06\x63hroot\x18\x01 \x01(\x0b\x32\x12.chromiumos.Chroot\x12&\n\x07sysroot\x18\x02 \x01(\x0b\x32\x15.chromite.api.Sysroot\x12\x35\n\rartifact_info\x18\x03 \x01(\x0b\x32\x1e.chromiumos.ArtifactsByService\x12\x1e\n\x16\x66orced_build_relevance\x18\x04 \x01(\x08\"\xa9\x01\n\x12\x42uildSetupResponse\x12H\n\x0f\x62uild_relevance\x18\x01 \x01(\x0e\x32/.chromite.api.BuildSetupResponse.BuildRelevance\"I\n\x0e\x42uildRelevance\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\n\n\x06NEEDED\x10\x01\x12\x0b\n\x07UNKNOWN\x10\x02\x12\r\n\tPOINTLESS\x10\x03\"\xbc\x01\n\nGetRequest\x12\"\n\x06\x63hroot\x18\x01 \x01(\x0b\x32\x12.chromiumos.Chroot\x12&\n\x07sysroot\x18\x02 \x01(\x0b\x32\x15.chromite.api.Sysroot\x12\x35\n\rartifact_info\x18\x03 \x01(\x0b\x32\x1e.chromiumos.ArtifactsByService\x12+\n\x0bresult_path\x18\x04 \x01(\x0b\x32\x16.chromiumos.ResultPath\"H\n\x0bGetResponse\x12\x39\n\tartifacts\x18\x01 \x01(\x0b\x32&.chromiumos.UploadedArtifactsByService\"\xdc\x01\n\x16\x42undleArtifactsRequest\x12\"\n\x06\x63hroot\x18\x01 \x01(\x0b\x32\x12.chromiumos.Chroot\x12&\n\x07sysroot\x18\x02 \x01(\x0b\x32\x15.chromite.api.Sysroot\x12\x35\n\rartifact_info\x18\x03 \x01(\x0b\x32\x1e.chromiumos.ArtifactsByService\x12\x12\n\noutput_dir\x18\x04 \x01(\t\x12+\n\x0bresult_path\x18\x05 \x01(\x0b\x32\x16.chromiumos.ResultPath\"T\n\x17\x42undleArtifactsResponse\x12\x39\n\tartifacts\x18\x01 \x01(\x0b\x32&.chromiumos.UploadedArtifactsByService\"\xcb\x01\n\rBundleRequest\x12-\n\x0c\x62uild_target\x18\x01 \x01(\x0b\x32\x17.chromiumos.BuildTarget\x12\x12\n\noutput_dir\x18\x02 \x01(\t\x12\"\n\x06\x63hroot\x18\x03 \x01(\x0b\x32\x12.chromiumos.Chroot\x12&\n\x07sysroot\x18\x04 \x01(\x0b\x32\x15.chromite.api.Sysroot\x12+\n\x0bresult_path\x18\x05 \x01(\x0b\x32\x16.chromiumos.ResultPath\"m\n\x0e\x42undleResponse\x12)\n\tartifacts\x18\x01 \x03(\x0b\x32\x16.chromite.api.Artifact\x12\x30\n\rdocker_builds\x18\x02 \x03(\x0b\x32\x19.chromite.api.DockerBuild\"\x90\x01\n\x14\x42undleVmFilesRequest\x12\"\n\x06\x63hroot\x18\x01 \x01(\x0b\x32\x12.chromiumos.Chroot\x12&\n\x07sysroot\x18\x02 \x01(\x0b\x32\x15.chromite.api.Sysroot\x12\x18\n\x10test_results_dir\x18\x03 \x01(\t\x12\x12\n\noutput_dir\x18\x04 \x01(\t\"h\n\x1aPinnedGuestImageUriRequest\x12\"\n\x06\x63hroot\x18\x01 \x01(\x0b\x32\x12.chromiumos.Chroot\x12&\n\x07sysroot\x18\x02 \x01(\x0b\x32\x15.chromite.api.Sysroot\"\xa3\x01\n\x1bPinnedGuestImageUriResponse\x12Q\n\rpinned_images\x18\x01 \x03(\x0b\x32:.chromite.api.PinnedGuestImageUriResponse.PinnedGuestImage\x1a\x31\n\x10PinnedGuestImage\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x0b\n\x03uri\x18\x02 \x01(\t\"b\n\x14\x46\x65tchMetadataRequest\x12\"\n\x06\x63hroot\x18\x01 \x01(\x0b\x32\x12.chromiumos.Chroot\x12&\n\x07sysroot\x18\x02 \x01(\x0b\x32\x15.chromite.api.Sysroot\"B\n\x15\x46\x65tchMetadataResponse\x12)\n\tfilepaths\x18\x01 \x03(\x0b\x32\x16.chromiumos.ResultPath\"m\n\x1f\x46\x65tchTestHarnessMetadataRequest\x12\"\n\x06\x63hroot\x18\x01 \x01(\x0b\x32\x12.chromiumos.Chroot\x12&\n\x07sysroot\x18\x02 \x01(\x0b\x32\x15.chromite.api.Sysroot\"M\n FetchTestHarnessMetadataResponse\x12)\n\tfilepaths\x18\x01 \x03(\x0b\x32\x16.chromiumos.ResultPath\"k\n\x1d\x46\x65tchCentralizedSuitesRequest\x12\"\n\x06\x63hroot\x18\x01 \x01(\x0b\x32\x12.chromiumos.Chroot\x12&\n\x07sysroot\x18\x02 \x01(\x0b\x32\x15.chromite.api.Sysroot\"|\n\x1e\x46\x65tchCentralizedSuitesResponse\x12.\n\x0esuite_set_file\x18\x01 \x01(\x0b\x32\x16.chromiumos.ResultPath\x12*\n\nsuite_file\x18\x02 \x01(\x0b\x32\x16.chromiumos.ResultPath2\xf1\r\n\x10\x41rtifactsService\x12O\n\nBuildSetup\x12\x1f.chromite.api.BuildSetupRequest\x1a .chromite.api.BuildSetupResponse\x12:\n\x03Get\x12\x18.chromite.api.GetRequest\x1a\x19.chromite.api.GetResponse\x12p\n\x19\x46\x65tchPinnedGuestImageUris\x12(.chromite.api.PinnedGuestImageUriRequest\x1a).chromite.api.PinnedGuestImageUriResponse\x12X\n\rFetchMetadata\x12\".chromite.api.FetchMetadataRequest\x1a#.chromite.api.FetchMetadataResponse\x12y\n\x18\x46\x65tchTestHarnessMetadata\x12-.chromite.api.FetchTestHarnessMetadataRequest\x1a..chromite.api.FetchTestHarnessMetadataResponse\x12s\n\x16\x46\x65tchCentralizedSuites\x12+.chromite.api.FetchCentralizedSuitesRequest\x1a,.chromite.api.FetchCentralizedSuitesResponse\x12P\n\x13\x42undleAutotestFiles\x12\x1b.chromite.api.BundleRequest\x1a\x1c.chromite.api.BundleResponse\x12Q\n\x14\x42undleChromeOSConfig\x12\x1b.chromite.api.BundleRequest\x1a\x1c.chromite.api.BundleResponse\x12O\n\x12\x42undleDebugSymbols\x12\x1b.chromite.api.BundleRequest\x1a\x1c.chromite.api.BundleResponse\x12M\n\x10\x42undleEbuildLogs\x12\x1b.chromite.api.BundleRequest\x1a\x1c.chromite.api.BundleResponse\x12K\n\x0e\x42undleFirmware\x12\x1b.chromite.api.BundleRequest\x1a\x1c.chromite.api.BundleResponse\x12P\n\x13\x42undleImageArchives\x12\x1b.chromite.api.BundleRequest\x1a\x1c.chromite.api.BundleResponse\x12K\n\x0e\x42undleImageZip\x12\x1b.chromite.api.BundleRequest\x1a\x1c.chromite.api.BundleResponse\x12T\n\x17\x42undlePinnedGuestImages\x12\x1b.chromite.api.BundleRequest\x1a\x1c.chromite.api.BundleResponse\x12X\n\x1b\x42undleSimpleChromeArtifacts\x12\x1b.chromite.api.BundleRequest\x1a\x1c.chromite.api.BundleResponse\x12L\n\x0f\x42undleTastFiles\x12\x1b.chromite.api.BundleRequest\x1a\x1c.chromite.api.BundleResponse\x12]\n\x18\x42undleTestUpdatePayloads\x12\x1b.chromite.api.BundleRequest\x1a\x1c.chromite.api.BundleResponse\"\x06\xc2\xed\x1a\x02\x10\x01\x12Q\n\rBundleVmFiles\x12\".chromite.api.BundleVmFilesRequest\x1a\x1c.chromite.api.BundleResponse\x12Q\n\x14\x42undleFpmcuUnittests\x12\x1b.chromite.api.BundleRequest\x1a\x1c.chromite.api.BundleResponse\x12M\n\x10\x42undleGceTarball\x12\x1b.chromite.api.BundleRequest\x1a\x1c.chromite.api.BundleResponse\x1a\x11\xc2\xed\x1a\r\n\tartifacts\x10\x02\x42\x38Z6go.chromium.org/chromiumos/infra/proto/go/chromite/apib\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chromite.api.artifacts_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z6go.chromium.org/chromiumos/infra/proto/go/chromite/api'
  _ARTIFACTSSERVICE._options = None
  _ARTIFACTSSERVICE._serialized_options = b'\302\355\032\r\n\tartifacts\020\002'
  _ARTIFACTSSERVICE.methods_by_name['BundleTestUpdatePayloads']._options = None
  _ARTIFACTSSERVICE.methods_by_name['BundleTestUpdatePayloads']._serialized_options = b'\302\355\032\002\020\001'
  _globals['_ARTIFACT']._serialized_start=129
  _globals['_ARTIFACT']._serialized_end=194
  _globals['_DOCKERBUILD']._serialized_start=196
  _globals['_DOCKERBUILD']._serialized_end=283
  _globals['_PREPAREFORBUILDRESPONSE']._serialized_start=286
  _globals['_PREPAREFORBUILDRESPONSE']._serialized_end=465
  _globals['_PREPAREFORBUILDRESPONSE_BUILDRELEVANCE']._serialized_start=392
  _globals['_PREPAREFORBUILDRESPONSE_BUILDRELEVANCE']._serialized_end=465
  _globals['_BUILDSETUPREQUEST']._serialized_start=468
  _globals['_BUILDSETUPREQUEST']._serialized_end=650
  _globals['_BUILDSETUPRESPONSE']._serialized_start=653
  _globals['_BUILDSETUPRESPONSE']._serialized_end=822
  _globals['_BUILDSETUPRESPONSE_BUILDRELEVANCE']._serialized_start=392
  _globals['_BUILDSETUPRESPONSE_BUILDRELEVANCE']._serialized_end=465
  _globals['_GETREQUEST']._serialized_start=825
  _globals['_GETREQUEST']._serialized_end=1013
  _globals['_GETRESPONSE']._serialized_start=1015
  _globals['_GETRESPONSE']._serialized_end=1087
  _globals['_BUNDLEARTIFACTSREQUEST']._serialized_start=1090
  _globals['_BUNDLEARTIFACTSREQUEST']._serialized_end=1310
  _globals['_BUNDLEARTIFACTSRESPONSE']._serialized_start=1312
  _globals['_BUNDLEARTIFACTSRESPONSE']._serialized_end=1396
  _globals['_BUNDLEREQUEST']._serialized_start=1399
  _globals['_BUNDLEREQUEST']._serialized_end=1602
  _globals['_BUNDLERESPONSE']._serialized_start=1604
  _globals['_BUNDLERESPONSE']._serialized_end=1713
  _globals['_BUNDLEVMFILESREQUEST']._serialized_start=1716
  _globals['_BUNDLEVMFILESREQUEST']._serialized_end=1860
  _globals['_PINNEDGUESTIMAGEURIREQUEST']._serialized_start=1862
  _globals['_PINNEDGUESTIMAGEURIREQUEST']._serialized_end=1966
  _globals['_PINNEDGUESTIMAGEURIRESPONSE']._serialized_start=1969
  _globals['_PINNEDGUESTIMAGEURIRESPONSE']._serialized_end=2132
  _globals['_PINNEDGUESTIMAGEURIRESPONSE_PINNEDGUESTIMAGE']._serialized_start=2083
  _globals['_PINNEDGUESTIMAGEURIRESPONSE_PINNEDGUESTIMAGE']._serialized_end=2132
  _globals['_FETCHMETADATAREQUEST']._serialized_start=2134
  _globals['_FETCHMETADATAREQUEST']._serialized_end=2232
  _globals['_FETCHMETADATARESPONSE']._serialized_start=2234
  _globals['_FETCHMETADATARESPONSE']._serialized_end=2300
  _globals['_FETCHTESTHARNESSMETADATAREQUEST']._serialized_start=2302
  _globals['_FETCHTESTHARNESSMETADATAREQUEST']._serialized_end=2411
  _globals['_FETCHTESTHARNESSMETADATARESPONSE']._serialized_start=2413
  _globals['_FETCHTESTHARNESSMETADATARESPONSE']._serialized_end=2490
  _globals['_FETCHCENTRALIZEDSUITESREQUEST']._serialized_start=2492
  _globals['_FETCHCENTRALIZEDSUITESREQUEST']._serialized_end=2599
  _globals['_FETCHCENTRALIZEDSUITESRESPONSE']._serialized_start=2601
  _globals['_FETCHCENTRALIZEDSUITESRESPONSE']._serialized_end=2725
  _globals['_ARTIFACTSSERVICE']._serialized_start=2728
  _globals['_ARTIFACTSSERVICE']._serialized_end=4505
# @@protoc_insertion_point(module_scope)
