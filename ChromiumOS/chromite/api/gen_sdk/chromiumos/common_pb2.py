# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/common.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17\x63hromiumos/common.proto\x12\nchromiumos\x1a google/protobuf/descriptor.proto\"A\n\x0b\x42uildTarget\x12\x0c\n\x04name\x18\x01 \x01(\t\x12$\n\x07profile\x18\x02 \x01(\x0b\x32\x13.chromiumos.Profile\"\'\n\x07GcsPath\x12\x0e\n\x06\x62ucket\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\"\xe2\x01\n\x06\x43hroot\x12\x0c\n\x04path\x18\x01 \x01(\t\x12\x11\n\tcache_dir\x18\x02 \x01(\t\x12)\n\x03\x65nv\x18\x03 \x01(\x0b\x32\x1c.chromiumos.Chroot.ChrootEnv\x12\x12\n\nchrome_dir\x18\x04 \x01(\t\x12\x10\n\x08out_path\x18\x06 \x01(\t\x1aZ\n\tChrootEnv\x12&\n\tuse_flags\x18\x01 \x03(\x0b\x32\x13.chromiumos.UseFlag\x12%\n\x08\x66\x65\x61tures\x18\x02 \x03(\x0b\x32\x13.chromiumos.FeatureJ\x04\x08\x05\x10\x06R\x04goma\"\x1a\n\x07\x46\x65\x61ture\x12\x0f\n\x07\x66\x65\x61ture\x18\x01 \x01(\t\"j\n\x10RemoteexecConfig\x12\x14\n\x0creclient_dir\x18\x01 \x01(\t\x12\x18\n\x10reproxy_cfg_file\x18\x02 \x01(\t\x12&\n\x07log_dir\x18\x03 \x01(\x0b\x32\x15.chromiumos.SyncedDir\"(\n\x13RemoteexecArtifacts\x12\x11\n\tlog_files\x18\x01 \x03(\t\"\xcd\x02\n\nGomaConfig\x12\x10\n\x08goma_dir\x18\x01 \x01(\t\x12\x19\n\x11\x63hromeos_goma_dir\x18\x03 \x01(\t\x12:\n\rgoma_approach\x18\x04 \x01(\x0e\x32#.chromiumos.GomaConfig.GomaApproach\x12&\n\x07log_dir\x18\x05 \x01(\x0b\x32\x15.chromiumos.SyncedDir\x12\x12\n\nstats_file\x18\x06 \x01(\t\x12\x15\n\rcounterz_file\x18\x07 \x01(\t\"k\n\x0cGomaApproach\x12\x1d\n\x19GOMA_APPROACH_UNSPECIFIED\x10\x00\x12\x0b\n\x07\x44\x45\x46\x41ULT\x10\x01\x12\x0c\n\x08RBE_PROD\x10\x02\x12\x0f\n\x0bRBE_STAGING\x10\x03\x12\x10\n\x0cRBE_CHROMEOS\x10\x04J\x04\x08\x02\x10\x03R\x10goma_client_json\"M\n\rGomaArtifacts\x12\x12\n\nstats_file\x18\x01 \x01(\t\x12\x15\n\rcounterz_file\x18\x02 \x01(\t\x12\x11\n\tlog_files\x18\x03 \x03(\t\"F\n\x0bPackageInfo\x12\x14\n\x0cpackage_name\x18\x01 \x01(\t\x12\x10\n\x08\x63\x61tegory\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\t\"\x17\n\x07Profile\x12\x0c\n\x04name\x18\x01 \x01(\t\"\xa8\x01\n\x10PackageIndexInfo\x12\x14\n\x0csnapshot_sha\x18\x01 \x01(\t\x12\x17\n\x0fsnapshot_number\x18\x02 \x01(\x05\x12-\n\x0c\x62uild_target\x18\x03 \x01(\x0b\x32\x17.chromiumos.BuildTarget\x12\x10\n\x08location\x18\x04 \x01(\t\x12$\n\x07profile\x18\x05 \x01(\x0b\x32\x13.chromiumos.Profile\"w\n\x04Path\x12\x0c\n\x04path\x18\x01 \x01(\t\x12+\n\x08location\x18\x02 \x01(\x0e\x32\x19.chromiumos.Path.Location\"4\n\x08Location\x12\x0f\n\x0bNO_LOCATION\x10\x00\x12\n\n\x06INSIDE\x10\x01\x12\x0b\n\x07OUTSIDE\x10\x02\"\xb0\x01\n\nResultPath\x12\x1e\n\x04path\x18\x01 \x01(\x0b\x32\x10.chromiumos.Path\x12\x31\n\x08transfer\x18\x02 \x01(\x0e\x32\x1f.chromiumos.ResultPath.Transfer\"O\n\x08Transfer\x12\x18\n\x14TRANSFER_UNSPECIFIED\x10\x00\x12\x11\n\rTRANSFER_COPY\x10\x01\x12\x16\n\x12TRANSFER_TRANSLATE\x10\x02\"\x18\n\tSyncedDir\x12\x0b\n\x03\x64ir\x18\x01 \x01(\t\"O\n\x0cGerritChange\x12\x0c\n\x04host\x18\x01 \x01(\t\x12\x0f\n\x07project\x18\x02 \x01(\t\x12\x0e\n\x06\x63hange\x18\x03 \x01(\x03\x12\x10\n\x08patchset\x18\x04 \x01(\x03\"Y\n\rGitilesCommit\x12\x0c\n\x04host\x18\x01 \x01(\t\x12\x0f\n\x07project\x18\x02 \x01(\t\x12\n\n\x02id\x18\x03 \x01(\t\x12\x0b\n\x03ref\x18\x04 \x01(\t\x12\x10\n\x08position\x18\x05 \x01(\r\"\x17\n\x07UseFlag\x12\x0c\n\x04\x66lag\x18\x01 \x01(\t\"\xbb\x03\n\x0eReleaseBuilder\x12\x39\n\tmilestone\x18\x01 \x01(\x0b\x32$.chromiumos.ReleaseBuilder.MilestoneH\x00\x12\x16\n\x0e\x62uild_schedule\x18\x02 \x01(\t\x12\x38\n\x0f\x65xpiration_date\x18\x03 \x01(\x0b\x32\x1f.chromiumos.ReleaseBuilder.Date\x12I\n\x10\x61ndroid_branches\x18\x04 \x03(\x0b\x32/.chromiumos.ReleaseBuilder.AndroidBranchesEntry\x1a\x15\n\x04\x44\x61te\x12\r\n\x05value\x18\x01 \x01(\t\x1am\n\tMilestone\x12\x0e\n\x06number\x18\x01 \x01(\x05\x12;\n\x12target_branch_date\x18\x02 \x01(\x0b\x32\x1f.chromiumos.ReleaseBuilder.Date\x12\x13\n\x0b\x62ranch_name\x18\x03 \x01(\t\x1a\x36\n\x14\x41ndroidBranchesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42\x13\n\x11milestone_message\"?\n\x0fReleaseBuilders\x12,\n\x08\x62uilders\x18\x01 \x03(\x0b\x32\x1a.chromiumos.ReleaseBuilder\"\xf4\x01\n\x0fReleaseChannels\x12J\n\x10release_channels\x18\x01 \x03(\x0b\x32\x30.chromiumos.ReleaseChannels.ReleaseChannelsEntry\x1a\x34\n\x0b\x43hannelList\x12%\n\x08\x63hannels\x18\x01 \x03(\x0e\x32\x13.chromiumos.Channel\x1a_\n\x14ReleaseChannelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\x36\n\x05value\x18\x02 \x01(\x0b\x32\'.chromiumos.ReleaseChannels.ChannelList:\x02\x38\x01\"&\n\nProtoBytes\x12\x18\n\x10serialized_proto\x18\x01 \x01(\x0c\"q\n\x1dPrepareForBuildAdditionalArgs\x12\x1c\n\x12\x63hrome_cwp_profile\x18\x01 \x01(\tH\x00\x12\x18\n\x0ekernel_version\x18\x02 \x01(\tH\x00\x42\x18\n\x16prepare_for_build_args\"A\n\x0b\x41\x66\x64oRelease\x12\x1a\n\x12\x63hrome_cwp_profile\x18\x01 \x01(\t\x12\x16\n\x0eimage_build_id\x18\x02 \x01(\x03\"\xa5\x01\n\x13\x41rtifactProfileInfo\x12\x1c\n\x12\x63hrome_cwp_profile\x18\x01 \x01(\tH\x00\x12\x18\n\x0ekernel_version\x18\x02 \x01(\tH\x00\x12/\n\x0c\x61\x66\x64o_release\x18\x03 \x01(\x0b\x32\x17.chromiumos.AfdoReleaseH\x00\x12\x0c\n\x04\x61rch\x18\x04 \x01(\tB\x17\n\x15\x61rtifact_profile_info\"\xba.\n\x12\x41rtifactsByService\x12\x35\n\x06legacy\x18\x01 \x01(\x0b\x32%.chromiumos.ArtifactsByService.Legacy\x12;\n\ttoolchain\x18\x02 \x01(\x0b\x32(.chromiumos.ArtifactsByService.Toolchain\x12\x33\n\x05image\x18\x03 \x01(\x0b\x32$.chromiumos.ArtifactsByService.Image\x12\x37\n\x07package\x18\x04 \x01(\x0b\x32&.chromiumos.ArtifactsByService.Package\x12\x37\n\x07sysroot\x18\x05 \x01(\x0b\x32&.chromiumos.ArtifactsByService.Sysroot\x12\x31\n\x04test\x18\x06 \x01(\x0b\x32#.chromiumos.ArtifactsByService.Test\x12\x35\n\x0cprofile_info\x18\x07 \x01(\x0b\x32\x1f.chromiumos.ArtifactProfileInfo\x12\x39\n\x08\x66irmware\x18\x08 \x01(\x0b\x32\'.chromiumos.ArtifactsByService.Firmware\x12\x33\n\x05infra\x18\t \x01(\x0b\x32$.chromiumos.ArtifactsByService.Infra\x12/\n\x03sdk\x18\n \x01(\x0b\x32\".chromiumos.ArtifactsByService.Sdk\x1a\xb0\x01\n\x16\x43odeCoverageUploadInfo\x12]\n\rcoverage_type\x18\x01 \x01(\x0e\x32\x46.chromiumos.ArtifactsByService.CodeCoverageUploadInfo.CodeCoverageType\"7\n\x10\x43odeCoverageType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x08\n\x04LLVM\x10\x01\x12\x08\n\x04LCOV\x10\x02\x1a\xe2\x04\n\x06Legacy\x12K\n\x0finput_artifacts\x18\x01 \x03(\x0b\x32\x32.chromiumos.ArtifactsByService.Legacy.ArtifactInfo\x12L\n\x10output_artifacts\x18\x02 \x03(\x0b\x32\x32.chromiumos.ArtifactsByService.Legacy.ArtifactInfo\x1a\x9c\x01\n\x0c\x41rtifactInfo\x12J\n\x0e\x61rtifact_types\x18\x01 \x03(\x0e\x32\x32.chromiumos.ArtifactsByService.Legacy.ArtifactType\x12\x14\n\x0cgs_locations\x18\x02 \x03(\t\x12\x10\n\x08\x61\x63l_name\x18\x04 \x01(\tJ\x04\x08\x03\x10\x04J\x04\x08\x05\x10\x06R\x0cprofile_info\"\x9d\x02\n\x0c\x41rtifactType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\r\n\tIMAGE_ZIP\x10\x01\x12\x17\n\x13TEST_UPDATE_PAYLOAD\x10\x02\x12\x12\n\x0e\x41UTOTEST_FILES\x10\x03\x12\x0e\n\nTAST_FILES\x10\x04\x12\x17\n\x13PINNED_GUEST_IMAGES\x10\x05\x12\x0c\n\x08\x46IRMWARE\x10\x06\x12\x0f\n\x0b\x45\x42UILD_LOGS\x10\x07\x12\x13\n\x0f\x43HROMEOS_CONFIG\x10\x08\x12\x12\n\x0eIMAGE_ARCHIVES\x10\n\x12\x13\n\x0f\x46PMCU_UNITTESTS\x10\x1b\x12\x0f\n\x0bGCE_TARBALL\x10\x1c\x12\x11\n\rDEBUG_SYMBOLS\x10 \"\x04\x08\t\x10\t\"\x04\x08\x0b\x10\x1a\"\x04\x08\x1d\x10\x1f\"\x04\x08!\x10\x38\x1a\xda\x06\n\tToolchain\x12N\n\x0finput_artifacts\x18\x01 \x03(\x0b\x32\x35.chromiumos.ArtifactsByService.Toolchain.ArtifactInfo\x12O\n\x10output_artifacts\x18\x02 \x03(\x0b\x32\x35.chromiumos.ArtifactsByService.Toolchain.ArtifactInfo\x1a\x8b\x01\n\x0c\x41rtifactInfo\x12M\n\x0e\x61rtifact_types\x18\x01 \x03(\x0e\x32\x35.chromiumos.ArtifactsByService.Toolchain.ArtifactType\x12\x14\n\x0cgs_locations\x18\x02 \x03(\t\x12\x10\n\x08\x61\x63l_name\x18\x04 \x01(\tJ\x04\x08\x05\x10\x06\"\x9d\x04\n\x0c\x41rtifactType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12)\n%UNVERIFIED_CHROME_BENCHMARK_AFDO_FILE\x10\x0f\x12\'\n#VERIFIED_CHROME_BENCHMARK_AFDO_FILE\x10\x10\x12!\n\x1dVERIFIED_KERNEL_CWP_AFDO_FILE\x10\x11\x12#\n\x1fUNVERIFIED_KERNEL_CWP_AFDO_FILE\x10\x12\x12#\n\x1fUNVERIFIED_CHROME_CWP_AFDO_FILE\x10\x13\x12!\n\x1dVERIFIED_CHROME_CWP_AFDO_FILE\x10\x14\x12\x1e\n\x1aVERIFIED_RELEASE_AFDO_FILE\x10\x15\x12)\n%UNVERIFIED_CHROME_BENCHMARK_PERF_FILE\x10\x16\x12\x17\n\x13\x43HROME_DEBUG_BINARY\x10\x17\x12\x1a\n\x16TOOLCHAIN_WARNING_LOGS\x10\x18\x12)\n%CHROME_AFDO_PROFILE_FOR_ANDROID_LINUX\x10\x19\x12\x19\n\x15\x43LANG_CRASH_DIAGNOSES\x10\x1a\x12\x17\n\x13\x43OMPILER_RUSAGE_LOG\x10\x1d\x12\x1b\n\x17SDK_TOOLCHAIN_PREBUILTS\x10\x34\"\x04\x08\x01\x10\n\"\x04\x08\x0b\x10\x0e\"\x04\x08\x1b\x10\x1c\"\x04\x08\x1e\x10\x33\"\x04\x08\x35\x10\x38\x1a\xd1\x03\n\x05Image\x12J\n\x0finput_artifacts\x18\x01 \x03(\x0b\x32\x31.chromiumos.ArtifactsByService.Image.ArtifactInfo\x12K\n\x10output_artifacts\x18\x02 \x03(\x0b\x32\x31.chromiumos.ArtifactsByService.Image.ArtifactInfo\x1a\x87\x01\n\x0c\x41rtifactInfo\x12I\n\x0e\x61rtifact_types\x18\x01 \x03(\x0e\x32\x31.chromiumos.ArtifactsByService.Image.ArtifactType\x12\x14\n\x0cgs_locations\x18\x02 \x03(\t\x12\x10\n\x08\x61\x63l_name\x18\x04 \x01(\tJ\x04\x08\x05\x10\x06\"\xa4\x01\n\x0c\x41rtifactType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\r\n\tDLC_IMAGE\x10\"\x12\x13\n\x0fLICENSE_CREDITS\x10&\x12\x11\n\rFACTORY_IMAGE\x10+\x12\x15\n\x11STRIPPED_PACKAGES\x10-\x12\x11\n\rIMAGE_SCRIPTS\x10\x31\"\x04\x08\x01\x10!\"\x04\x08#\x10%\"\x04\x08\'\x10*\"\x04\x08,\x10,\"\x04\x08.\x10\x30\"\x04\x08\x32\x10\x38\x1a\xd9\x02\n\x07Package\x12L\n\x0finput_artifacts\x18\x01 \x03(\x0b\x32\x33.chromiumos.ArtifactsByService.Package.ArtifactInfo\x12M\n\x10output_artifacts\x18\x02 \x03(\x0b\x32\x33.chromiumos.ArtifactsByService.Package.ArtifactInfo\x1a\x89\x01\n\x0c\x41rtifactInfo\x12K\n\x0e\x61rtifact_types\x18\x01 \x03(\x0e\x32\x33.chromiumos.ArtifactsByService.Package.ArtifactType\x12\x14\n\x0cgs_locations\x18\x02 \x03(\t\x12\x10\n\x08\x61\x63l_name\x18\x04 \x01(\tJ\x04\x08\x05\x10\x06\"%\n\x0c\x41rtifactType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\"\x04\x08\x01\x10\x38\x1a\xb6\x07\n\x07Sysroot\x12L\n\x0finput_artifacts\x18\x01 \x03(\x0b\x32\x33.chromiumos.ArtifactsByService.Sysroot.ArtifactInfo\x12M\n\x10output_artifacts\x18\x02 \x03(\x0b\x32\x33.chromiumos.ArtifactsByService.Sysroot.ArtifactInfo\x12\x30\n(ignore_breakpad_symbol_generation_errors\x18\x03 \x01(\x08\x12\x85\x01\n0ignore_breakpad_symbol_generation_expected_files\x18\x04 \x03(\x0e\x32K.chromiumos.ArtifactsByService.Sysroot.BreakpadSymbolGenerationExpectedFile\x1a\x89\x01\n\x0c\x41rtifactInfo\x12K\n\x0e\x61rtifact_types\x18\x01 \x03(\x0e\x32\x33.chromiumos.ArtifactsByService.Sysroot.ArtifactType\x12\x14\n\x0cgs_locations\x18\x02 \x03(\t\x12\x10\n\x08\x61\x63l_name\x18\x04 \x01(\tJ\x04\x08\x05\x10\x06\"\x8f\x02\n\x0c\x41rtifactType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x11\n\rDEBUG_SYMBOLS\x10 \x12\x1a\n\x16\x42REAKPAD_DEBUG_SYMBOLS\x10#\x12\x19\n\x15SIMPLE_CHROME_SYSROOT\x10(\x12\x15\n\x11\x43HROME_EBUILD_ENV\x10)\x12\x12\n\x0e\x46UZZER_SYSROOT\x10/\x12\x13\n\x0fSYSROOT_ARCHIVE\x10\x32\x12\x1f\n\x1b\x42\x41ZEL_PERFORMANCE_ARTIFACTS\x10\x35\x12\x19\n\x15\x43OMPILE_COMMANDS_JSON\x10\x38\"\x04\x08\x01\x10\x1f\"\x04\x08!\x10\"\"\x04\x08$\x10\'\"\x04\x08*\x10.\"\x04\x08\x30\x10\x31\"\x04\x08\x34\x10\x34\"\x04\x08\x36\x10\x37\"\xb5\x01\n$BreakpadSymbolGenerationExpectedFile\x12\x17\n\x13\x45XPECTED_FILE_UNSET\x10\x00\x12\x1c\n\x18\x45XPECTED_FILE_ASH_CHROME\x10\x01\x12\x16\n\x12\x45XPECTED_FILE_LIBC\x10\x02\x12 \n\x1c\x45XPECTED_FILE_CRASH_REPORTER\x10\x03\x12\x1c\n\x18\x45XPECTED_FILE_LIBMETRICS\x10\x04\x1a\xd8\x04\n\x04Test\x12I\n\x0finput_artifacts\x18\x01 \x03(\x0b\x32\x30.chromiumos.ArtifactsByService.Test.ArtifactInfo\x12J\n\x10output_artifacts\x18\x02 \x03(\x0b\x32\x30.chromiumos.ArtifactsByService.Test.ArtifactInfo\x1a\xe0\x01\n\x0c\x41rtifactInfo\x12H\n\x0e\x61rtifact_types\x18\x01 \x03(\x0e\x32\x30.chromiumos.ArtifactsByService.Test.ArtifactType\x12\x14\n\x0cgs_locations\x18\x02 \x03(\t\x12\x10\n\x08\x61\x63l_name\x18\x04 \x01(\t\x12X\n\x19\x63ode_coverage_upload_info\x18\x06 \x01(\x0b\x32\x35.chromiumos.ArtifactsByService.CodeCoverageUploadInfoJ\x04\x08\x05\x10\x06\"\xd5\x01\n\x0c\x41rtifactType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0e\n\nUNIT_TESTS\x10%\x12\x1b\n\x17\x43ODE_COVERAGE_LLVM_JSON\x10\'\x12\n\n\x06HWQUAL\x10*\x12 \n\x1c\x43ODE_COVERAGE_RUST_LLVM_JSON\x10.\x12\x18\n\x14\x43ODE_COVERAGE_GOLANG\x10\x30\x12\x15\n\x11\x43ODE_COVERAGE_E2E\x10\x36\"\x04\x08\x01\x10$\"\x04\x08&\x10&\"\x04\x08(\x10)\"\x04\x08+\x10-\"\x04\x08/\x10/\"\x04\x08\x31\x10\x35\"\x04\x08\x37\x10\x38\x1a\xf3\x04\n\x08\x46irmware\x12M\n\x0finput_artifacts\x18\x01 \x03(\x0b\x32\x34.chromiumos.ArtifactsByService.Firmware.ArtifactInfo\x12N\n\x10output_artifacts\x18\x02 \x03(\x0b\x32\x34.chromiumos.ArtifactsByService.Firmware.ArtifactInfo\x1a\x8e\x02\n\x0c\x41rtifactInfo\x12L\n\x0e\x61rtifact_types\x18\x01 \x03(\x0e\x32\x34.chromiumos.ArtifactsByService.Firmware.ArtifactType\x12\x14\n\x0cgs_locations\x18\x02 \x03(\t\x12\x10\n\x08\x61\x63l_name\x18\x04 \x01(\t\x12(\n\x08location\x18\x06 \x01(\x0e\x32\x16.chromiumos.FwLocation\x12X\n\x19\x63ode_coverage_upload_info\x18\x07 \x01(\x0b\x32\x35.chromiumos.ArtifactsByService.CodeCoverageUploadInfoJ\x04\x08\x05\x10\x06\"\xb6\x01\n\x0c\x41rtifactType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x14\n\x10\x46IRMWARE_TARBALL\x10\x1e\x12\x19\n\x15\x46IRMWARE_TARBALL_INFO\x10\x1f\x12\x11\n\rFIRMWARE_LCOV\x10!\x12\x16\n\x12\x43ODE_COVERAGE_HTML\x10,\x12\x1b\n\x17\x46IRMWARE_TOKEN_DATABASE\x10\x37\"\x04\x08\x01\x10\x1d\"\x04\x08 \x10 \"\x04\x08\"\x10+\"\x04\x08-\x10\x36\"\x04\x08\x38\x10\x38\x1a\xeb\x02\n\x05Infra\x12J\n\x0finput_artifacts\x18\x01 \x03(\x0b\x32\x31.chromiumos.ArtifactsByService.Infra.ArtifactInfo\x12K\n\x10output_artifacts\x18\x02 \x03(\x0b\x32\x31.chromiumos.ArtifactsByService.Infra.ArtifactInfo\x1a\x87\x01\n\x0c\x41rtifactInfo\x12I\n\x0e\x61rtifact_types\x18\x01 \x03(\x0e\x32\x31.chromiumos.ArtifactsByService.Infra.ArtifactType\x12\x14\n\x0cgs_locations\x18\x02 \x03(\t\x12\x10\n\x08\x61\x63l_name\x18\x04 \x01(\tJ\x04\x08\x05\x10\x06\"?\n\x0c\x41rtifactType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x12\n\x0e\x42UILD_MANIFEST\x10$\"\x04\x08\x01\x10#\"\x04\x08%\x10\x38\x1a\xe0\x02\n\x03Sdk\x12H\n\x0finput_artifacts\x18\x01 \x03(\x0b\x32/.chromiumos.ArtifactsByService.Sdk.ArtifactInfo\x12I\n\x10output_artifacts\x18\x02 \x03(\x0b\x32/.chromiumos.ArtifactsByService.Sdk.ArtifactInfo\x1a\x85\x01\n\x0c\x41rtifactInfo\x12G\n\x0e\x61rtifact_types\x18\x01 \x03(\x0e\x32/.chromiumos.ArtifactsByService.Sdk.ArtifactType\x12\x14\n\x0cgs_locations\x18\x02 \x03(\t\x12\x10\n\x08\x61\x63l_name\x18\x04 \x01(\tJ\x04\x08\x05\x10\x06\"<\n\x0c\x41rtifactType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0f\n\x0bSDK_TARBALL\x10\x33\"\x04\x08\x01\x10\x32\"\x04\x08\x34\x10\x38\"\x86\x17\n\x1aUploadedArtifactsByService\x12=\n\x06legacy\x18\x01 \x01(\x0b\x32-.chromiumos.UploadedArtifactsByService.Legacy\x12\x43\n\ttoolchain\x18\x02 \x01(\x0b\x32\x30.chromiumos.UploadedArtifactsByService.Toolchain\x12;\n\x05image\x18\x03 \x01(\x0b\x32,.chromiumos.UploadedArtifactsByService.Image\x12?\n\x07package\x18\x04 \x01(\x0b\x32..chromiumos.UploadedArtifactsByService.Package\x12?\n\x07sysroot\x18\x05 \x01(\x0b\x32..chromiumos.UploadedArtifactsByService.Sysroot\x12\x39\n\x04test\x18\x06 \x01(\x0b\x32+.chromiumos.UploadedArtifactsByService.Test\x12\x41\n\x08\x66irmware\x18\x07 \x01(\x0b\x32/.chromiumos.UploadedArtifactsByService.Firmware\x12;\n\x05infra\x18\x08 \x01(\x0b\x32,.chromiumos.UploadedArtifactsByService.Infra\x12\x37\n\x03sdk\x18\t \x01(\x0b\x32*.chromiumos.UploadedArtifactsByService.Sdk\x1a\xfe\x01\n\x06Legacy\x12N\n\tartifacts\x18\x01 \x03(\x0b\x32;.chromiumos.UploadedArtifactsByService.Legacy.ArtifactPaths\x1a\xa3\x01\n\rArtifactPaths\x12I\n\rartifact_type\x18\x01 \x01(\x0e\x32\x32.chromiumos.ArtifactsByService.Legacy.ArtifactType\x12\x1f\n\x05paths\x18\x02 \x03(\x0b\x32\x10.chromiumos.Path\x12\x0e\n\x06\x66\x61iled\x18\x03 \x01(\x08\x12\x16\n\x0e\x66\x61ilure_reason\x18\x04 \x01(\t\x1a\x87\x02\n\tToolchain\x12Q\n\tartifacts\x18\x01 \x03(\x0b\x32>.chromiumos.UploadedArtifactsByService.Toolchain.ArtifactPaths\x1a\xa6\x01\n\rArtifactPaths\x12L\n\rartifact_type\x18\x01 \x01(\x0e\x32\x35.chromiumos.ArtifactsByService.Toolchain.ArtifactType\x12\x1f\n\x05paths\x18\x02 \x03(\x0b\x32\x10.chromiumos.Path\x12\x0e\n\x06\x66\x61iled\x18\x03 \x01(\x08\x12\x16\n\x0e\x66\x61ilure_reason\x18\x04 \x01(\t\x1a\xfb\x01\n\x05Image\x12M\n\tartifacts\x18\x01 \x03(\x0b\x32:.chromiumos.UploadedArtifactsByService.Image.ArtifactPaths\x1a\xa2\x01\n\rArtifactPaths\x12H\n\rartifact_type\x18\x01 \x01(\x0e\x32\x31.chromiumos.ArtifactsByService.Image.ArtifactType\x12\x1f\n\x05paths\x18\x02 \x03(\x0b\x32\x10.chromiumos.Path\x12\x0e\n\x06\x66\x61iled\x18\x03 \x01(\x08\x12\x16\n\x0e\x66\x61ilure_reason\x18\x04 \x01(\t\x1a\x81\x02\n\x07Package\x12O\n\tartifacts\x18\x01 \x03(\x0b\x32<.chromiumos.UploadedArtifactsByService.Package.ArtifactPaths\x1a\xa4\x01\n\rArtifactPaths\x12J\n\rartifact_type\x18\x01 \x01(\x0e\x32\x33.chromiumos.ArtifactsByService.Package.ArtifactType\x12\x1f\n\x05paths\x18\x02 \x03(\x0b\x32\x10.chromiumos.Path\x12\x0e\n\x06\x66\x61iled\x18\x03 \x01(\x08\x12\x16\n\x0e\x66\x61ilure_reason\x18\x04 \x01(\t\x1a\x81\x02\n\x07Sysroot\x12O\n\tartifacts\x18\x01 \x03(\x0b\x32<.chromiumos.UploadedArtifactsByService.Sysroot.ArtifactPaths\x1a\xa4\x01\n\rArtifactPaths\x12J\n\rartifact_type\x18\x01 \x01(\x0e\x32\x33.chromiumos.ArtifactsByService.Sysroot.ArtifactType\x12\x1f\n\x05paths\x18\x02 \x03(\x0b\x32\x10.chromiumos.Path\x12\x0e\n\x06\x66\x61iled\x18\x03 \x01(\x08\x12\x16\n\x0e\x66\x61ilure_reason\x18\x04 \x01(\t\x1a\xf8\x01\n\x04Test\x12L\n\tartifacts\x18\x01 \x03(\x0b\x32\x39.chromiumos.UploadedArtifactsByService.Test.ArtifactPaths\x1a\xa1\x01\n\rArtifactPaths\x12G\n\rartifact_type\x18\x01 \x01(\x0e\x32\x30.chromiumos.ArtifactsByService.Test.ArtifactType\x12\x1f\n\x05paths\x18\x02 \x03(\x0b\x32\x10.chromiumos.Path\x12\x0e\n\x06\x66\x61iled\x18\x03 \x01(\x08\x12\x16\n\x0e\x66\x61ilure_reason\x18\x04 \x01(\t\x1a\xae\x02\n\x08\x46irmware\x12P\n\tartifacts\x18\x01 \x03(\x0b\x32=.chromiumos.UploadedArtifactsByService.Firmware.ArtifactPaths\x1a\xcf\x01\n\rArtifactPaths\x12K\n\rartifact_type\x18\x01 \x01(\x0e\x32\x34.chromiumos.ArtifactsByService.Firmware.ArtifactType\x12\x1f\n\x05paths\x18\x02 \x03(\x0b\x32\x10.chromiumos.Path\x12(\n\x08location\x18\x03 \x01(\x0e\x32\x16.chromiumos.FwLocation\x12\x0e\n\x06\x66\x61iled\x18\x04 \x01(\x08\x12\x16\n\x0e\x66\x61ilure_reason\x18\x05 \x01(\t\x1a\xfb\x01\n\x05Infra\x12M\n\tartifacts\x18\x01 \x03(\x0b\x32:.chromiumos.UploadedArtifactsByService.Infra.ArtifactPaths\x1a\xa2\x01\n\rArtifactPaths\x12H\n\rartifact_type\x18\x01 \x01(\x0e\x32\x31.chromiumos.ArtifactsByService.Infra.ArtifactType\x12\x1f\n\x05paths\x18\x02 \x03(\x0b\x32\x10.chromiumos.Path\x12\x0e\n\x06\x66\x61iled\x18\x03 \x01(\x08\x12\x16\n\x0e\x66\x61ilure_reason\x18\x04 \x01(\t\x1a\xf5\x01\n\x03Sdk\x12K\n\tartifacts\x18\x01 \x03(\x0b\x32\x38.chromiumos.UploadedArtifactsByService.Sdk.ArtifactPaths\x1a\xa0\x01\n\rArtifactPaths\x12\x46\n\rartifact_type\x18\x01 \x01(\x0e\x32/.chromiumos.ArtifactsByService.Sdk.ArtifactType\x12\x1f\n\x05paths\x18\x02 \x03(\x0b\x32\x10.chromiumos.Path\x12\x0e\n\x06\x66\x61iled\x18\x03 \x01(\x08\x12\x16\n\x0e\x66\x61ilure_reason\x18\x04 \x01(\t*\x84\x06\n\tImageType\x12\x18\n\x14IMAGE_TYPE_UNDEFINED\x10\x00\x12\x13\n\x0fIMAGE_TYPE_BASE\x10\x01\x12\x12\n\x0eIMAGE_TYPE_DEV\x10\x02\x12\x13\n\x0fIMAGE_TYPE_TEST\x10\x03\x12\x16\n\x12IMAGE_TYPE_BASE_VM\x10\x04\x12\x16\n\x12IMAGE_TYPE_TEST_VM\x10\x05\x12\x17\n\x13IMAGE_TYPE_RECOVERY\x10\x06\x12\x16\n\x12IMAGE_TYPE_FACTORY\x10\x07\x12\x17\n\x13IMAGE_TYPE_FIRMWARE\x10\x08\x12\x1c\n\x18IMAGE_TYPE_CR50_FIRMWARE\x10\t\x12\x1c\n\x18IMAGE_TYPE_BASE_GUEST_VM\x10\n\x12\x1c\n\x18IMAGE_TYPE_TEST_GUEST_VM\x10\x0b\x12\x12\n\x0eIMAGE_TYPE_DLC\x10\x0c\x12\x1b\n\x17IMAGE_TYPE_GSC_FIRMWARE\x10\r\x12\x1e\n\x1aIMAGE_TYPE_ACCESSORY_USBPD\x10\x0e\x12\x1e\n\x1aIMAGE_TYPE_ACCESSORY_RWSIG\x10\x0f\x12\x1b\n\x17IMAGE_TYPE_HPS_FIRMWARE\x10\x10\x12\x16\n\x12IMAGE_TYPE_NETBOOT\x10\x11\x12\x1d\n\x19IMAGE_TYPE_UPDATE_PAYLOAD\x10\x12\x12\x1c\n\x18IMAGE_TYPE_FLEXOR_KERNEL\x10\x13\x12\x18\n\x14IMAGE_TYPE_SHELLBALL\x10\x14\x12\x1e\n\x1aIMAGE_TYPE_RECOVERY_KERNEL\x10\x15*\x04\x42\x41SE*\x04TEST*\x03\x44\x45V*\x07\x42\x41SE_VM*\x07TEST_VM*\x08RECOVERY*\x07\x46\x41\x43TORY*\x08\x46IRMWARE*\rCR50_FIRMWARE*\rBASE_GUEST_VM*\rTEST_GUEST_VM*\x03\x44LC*\x0cGSC_FIRMWARE*\x0f\x41\x43\x43\x45SSORY_USBPD*\x0f\x41\x43\x43\x45SSORY_RWSIG*\x0cHPS_FIRMWARE*\x8f\x01\n\x07\x43hannel\x12\x17\n\x13\x43HANNEL_UNSPECIFIED\x10\x00\x12\x12\n\x0e\x43HANNEL_STABLE\x10\x01\x12\x10\n\x0c\x43HANNEL_BETA\x10\x02\x12\x0f\n\x0b\x43HANNEL_DEV\x10\x03\x12\x12\n\x0e\x43HANNEL_CANARY\x10\x04\x12\x0f\n\x0b\x43HANNEL_LTS\x10\x05\x12\x0f\n\x0b\x43HANNEL_LTC\x10\x06*l\n\tDeltaType\x12\x11\n\rDELTA_UNKNOWN\x10\x00\x12\x0c\n\x08NO_DELTA\x10\x01\x12\x07\n\x03\x46SI\x10\x02\x12\r\n\tMILESTONE\x10\x03\x12\t\n\x05OMAHA\x10\x04\x12\x12\n\x0eSTEPPING_STONE\x10\x05\x12\x07\n\x03N2N\x10\x06*\xc7\x01\n\nFwLocation\x12\x17\n\x13\x46W_LOCATION_UNKNOWN\x10\x00\x12\x0f\n\x0bPLATFORM_EC\x10\x01\x12\x13\n\x0fPLATFORM_ZEPHYR\x10\x02\x12\x11\n\rPLATFORM_TI50\x10\x03\x12\x11\n\rPLATFORM_CR50\x10\x04\x12\x16\n\x12PLATFORM_CHAMELEON\x10\x05\x12\x16\n\x12PLATFORM_GSC_UTILS\x10\x06\x12\x0f\n\x0bPLATFORM_AP\x10\x07\x12\x13\n\x0fPLATFORM_RENODE\x10\x08:<\n\x10logging_optional\x12\x1d.google.protobuf.FieldOptions\x18\xac\xa9\x03 \x01(\x08\x88\x01\x01\x42Y\n!com.google.chrome.crosinfra.protoZ4go.chromium.org/chromiumos/infra/proto/go/chromiumosb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chromiumos.common_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  google_dot_protobuf_dot_descriptor__pb2.FieldOptions.RegisterExtension(logging_optional)

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n!com.google.chrome.crosinfra.protoZ4go.chromium.org/chromiumos/infra/proto/go/chromiumos'
  _RELEASEBUILDER_ANDROIDBRANCHESENTRY._options = None
  _RELEASEBUILDER_ANDROIDBRANCHESENTRY._serialized_options = b'8\001'
  _RELEASECHANNELS_RELEASECHANNELSENTRY._options = None
  _RELEASECHANNELS_RELEASECHANNELSENTRY._serialized_options = b'8\001'
  _globals['_IMAGETYPE']._serialized_start=11845
  _globals['_IMAGETYPE']._serialized_end=12617
  _globals['_CHANNEL']._serialized_start=12620
  _globals['_CHANNEL']._serialized_end=12763
  _globals['_DELTATYPE']._serialized_start=12765
  _globals['_DELTATYPE']._serialized_end=12873
  _globals['_FWLOCATION']._serialized_start=12876
  _globals['_FWLOCATION']._serialized_end=13075
  _globals['_BUILDTARGET']._serialized_start=73
  _globals['_BUILDTARGET']._serialized_end=138
  _globals['_GCSPATH']._serialized_start=140
  _globals['_GCSPATH']._serialized_end=179
  _globals['_CHROOT']._serialized_start=182
  _globals['_CHROOT']._serialized_end=408
  _globals['_CHROOT_CHROOTENV']._serialized_start=306
  _globals['_CHROOT_CHROOTENV']._serialized_end=396
  _globals['_FEATURE']._serialized_start=410
  _globals['_FEATURE']._serialized_end=436
  _globals['_REMOTEEXECCONFIG']._serialized_start=438
  _globals['_REMOTEEXECCONFIG']._serialized_end=544
  _globals['_REMOTEEXECARTIFACTS']._serialized_start=546
  _globals['_REMOTEEXECARTIFACTS']._serialized_end=586
  _globals['_GOMACONFIG']._serialized_start=589
  _globals['_GOMACONFIG']._serialized_end=922
  _globals['_GOMACONFIG_GOMAAPPROACH']._serialized_start=791
  _globals['_GOMACONFIG_GOMAAPPROACH']._serialized_end=898
  _globals['_GOMAARTIFACTS']._serialized_start=924
  _globals['_GOMAARTIFACTS']._serialized_end=1001
  _globals['_PACKAGEINFO']._serialized_start=1003
  _globals['_PACKAGEINFO']._serialized_end=1073
  _globals['_PROFILE']._serialized_start=1075
  _globals['_PROFILE']._serialized_end=1098
  _globals['_PACKAGEINDEXINFO']._serialized_start=1101
  _globals['_PACKAGEINDEXINFO']._serialized_end=1269
  _globals['_PATH']._serialized_start=1271
  _globals['_PATH']._serialized_end=1390
  _globals['_PATH_LOCATION']._serialized_start=1338
  _globals['_PATH_LOCATION']._serialized_end=1390
  _globals['_RESULTPATH']._serialized_start=1393
  _globals['_RESULTPATH']._serialized_end=1569
  _globals['_RESULTPATH_TRANSFER']._serialized_start=1490
  _globals['_RESULTPATH_TRANSFER']._serialized_end=1569
  _globals['_SYNCEDDIR']._serialized_start=1571
  _globals['_SYNCEDDIR']._serialized_end=1595
  _globals['_GERRITCHANGE']._serialized_start=1597
  _globals['_GERRITCHANGE']._serialized_end=1676
  _globals['_GITILESCOMMIT']._serialized_start=1678
  _globals['_GITILESCOMMIT']._serialized_end=1767
  _globals['_USEFLAG']._serialized_start=1769
  _globals['_USEFLAG']._serialized_end=1792
  _globals['_RELEASEBUILDER']._serialized_start=1795
  _globals['_RELEASEBUILDER']._serialized_end=2238
  _globals['_RELEASEBUILDER_DATE']._serialized_start=2029
  _globals['_RELEASEBUILDER_DATE']._serialized_end=2050
  _globals['_RELEASEBUILDER_MILESTONE']._serialized_start=2052
  _globals['_RELEASEBUILDER_MILESTONE']._serialized_end=2161
  _globals['_RELEASEBUILDER_ANDROIDBRANCHESENTRY']._serialized_start=2163
  _globals['_RELEASEBUILDER_ANDROIDBRANCHESENTRY']._serialized_end=2217
  _globals['_RELEASEBUILDERS']._serialized_start=2240
  _globals['_RELEASEBUILDERS']._serialized_end=2303
  _globals['_RELEASECHANNELS']._serialized_start=2306
  _globals['_RELEASECHANNELS']._serialized_end=2550
  _globals['_RELEASECHANNELS_CHANNELLIST']._serialized_start=2401
  _globals['_RELEASECHANNELS_CHANNELLIST']._serialized_end=2453
  _globals['_RELEASECHANNELS_RELEASECHANNELSENTRY']._serialized_start=2455
  _globals['_RELEASECHANNELS_RELEASECHANNELSENTRY']._serialized_end=2550
  _globals['_PROTOBYTES']._serialized_start=2552
  _globals['_PROTOBYTES']._serialized_end=2590
  _globals['_PREPAREFORBUILDADDITIONALARGS']._serialized_start=2592
  _globals['_PREPAREFORBUILDADDITIONALARGS']._serialized_end=2705
  _globals['_AFDORELEASE']._serialized_start=2707
  _globals['_AFDORELEASE']._serialized_end=2772
  _globals['_ARTIFACTPROFILEINFO']._serialized_start=2775
  _globals['_ARTIFACTPROFILEINFO']._serialized_end=2940
  _globals['_ARTIFACTSBYSERVICE']._serialized_start=2943
  _globals['_ARTIFACTSBYSERVICE']._serialized_end=8889
  _globals['_ARTIFACTSBYSERVICE_CODECOVERAGEUPLOADINFO']._serialized_start=3516
  _globals['_ARTIFACTSBYSERVICE_CODECOVERAGEUPLOADINFO']._serialized_end=3692
  _globals['_ARTIFACTSBYSERVICE_CODECOVERAGEUPLOADINFO_CODECOVERAGETYPE']._serialized_start=3637
  _globals['_ARTIFACTSBYSERVICE_CODECOVERAGEUPLOADINFO_CODECOVERAGETYPE']._serialized_end=3692
  _globals['_ARTIFACTSBYSERVICE_LEGACY']._serialized_start=3695
  _globals['_ARTIFACTSBYSERVICE_LEGACY']._serialized_end=4305
  _globals['_ARTIFACTSBYSERVICE_LEGACY_ARTIFACTINFO']._serialized_start=3861
  _globals['_ARTIFACTSBYSERVICE_LEGACY_ARTIFACTINFO']._serialized_end=4017
  _globals['_ARTIFACTSBYSERVICE_LEGACY_ARTIFACTTYPE']._serialized_start=4020
  _globals['_ARTIFACTSBYSERVICE_LEGACY_ARTIFACTTYPE']._serialized_end=4305
  _globals['_ARTIFACTSBYSERVICE_TOOLCHAIN']._serialized_start=4308
  _globals['_ARTIFACTSBYSERVICE_TOOLCHAIN']._serialized_end=5166
  _globals['_ARTIFACTSBYSERVICE_TOOLCHAIN_ARTIFACTINFO']._serialized_start=4483
  _globals['_ARTIFACTSBYSERVICE_TOOLCHAIN_ARTIFACTINFO']._serialized_end=4622
  _globals['_ARTIFACTSBYSERVICE_TOOLCHAIN_ARTIFACTTYPE']._serialized_start=4625
  _globals['_ARTIFACTSBYSERVICE_TOOLCHAIN_ARTIFACTTYPE']._serialized_end=5166
  _globals['_ARTIFACTSBYSERVICE_IMAGE']._serialized_start=5169
  _globals['_ARTIFACTSBYSERVICE_IMAGE']._serialized_end=5634
  _globals['_ARTIFACTSBYSERVICE_IMAGE_ARTIFACTINFO']._serialized_start=5332
  _globals['_ARTIFACTSBYSERVICE_IMAGE_ARTIFACTINFO']._serialized_end=5467
  _globals['_ARTIFACTSBYSERVICE_IMAGE_ARTIFACTTYPE']._serialized_start=5470
  _globals['_ARTIFACTSBYSERVICE_IMAGE_ARTIFACTTYPE']._serialized_end=5634
  _globals['_ARTIFACTSBYSERVICE_PACKAGE']._serialized_start=5637
  _globals['_ARTIFACTSBYSERVICE_PACKAGE']._serialized_end=5982
  _globals['_ARTIFACTSBYSERVICE_PACKAGE_ARTIFACTINFO']._serialized_start=5806
  _globals['_ARTIFACTSBYSERVICE_PACKAGE_ARTIFACTINFO']._serialized_end=5943
  _globals['_ARTIFACTSBYSERVICE_PACKAGE_ARTIFACTTYPE']._serialized_start=5945
  _globals['_ARTIFACTSBYSERVICE_PACKAGE_ARTIFACTTYPE']._serialized_end=5982
  _globals['_ARTIFACTSBYSERVICE_SYSROOT']._serialized_start=5985
  _globals['_ARTIFACTSBYSERVICE_SYSROOT']._serialized_end=6935
  _globals['_ARTIFACTSBYSERVICE_SYSROOT_ARTIFACTINFO']._serialized_start=6340
  _globals['_ARTIFACTSBYSERVICE_SYSROOT_ARTIFACTINFO']._serialized_end=6477
  _globals['_ARTIFACTSBYSERVICE_SYSROOT_ARTIFACTTYPE']._serialized_start=6480
  _globals['_ARTIFACTSBYSERVICE_SYSROOT_ARTIFACTTYPE']._serialized_end=6751
  _globals['_ARTIFACTSBYSERVICE_SYSROOT_BREAKPADSYMBOLGENERATIONEXPECTEDFILE']._serialized_start=6754
  _globals['_ARTIFACTSBYSERVICE_SYSROOT_BREAKPADSYMBOLGENERATIONEXPECTEDFILE']._serialized_end=6935
  _globals['_ARTIFACTSBYSERVICE_TEST']._serialized_start=6938
  _globals['_ARTIFACTSBYSERVICE_TEST']._serialized_end=7538
  _globals['_ARTIFACTSBYSERVICE_TEST_ARTIFACTINFO']._serialized_start=7098
  _globals['_ARTIFACTSBYSERVICE_TEST_ARTIFACTINFO']._serialized_end=7322
  _globals['_ARTIFACTSBYSERVICE_TEST_ARTIFACTTYPE']._serialized_start=7325
  _globals['_ARTIFACTSBYSERVICE_TEST_ARTIFACTTYPE']._serialized_end=7538
  _globals['_ARTIFACTSBYSERVICE_FIRMWARE']._serialized_start=7541
  _globals['_ARTIFACTSBYSERVICE_FIRMWARE']._serialized_end=8168
  _globals['_ARTIFACTSBYSERVICE_FIRMWARE_ARTIFACTINFO']._serialized_start=7713
  _globals['_ARTIFACTSBYSERVICE_FIRMWARE_ARTIFACTINFO']._serialized_end=7983
  _globals['_ARTIFACTSBYSERVICE_FIRMWARE_ARTIFACTTYPE']._serialized_start=7986
  _globals['_ARTIFACTSBYSERVICE_FIRMWARE_ARTIFACTTYPE']._serialized_end=8168
  _globals['_ARTIFACTSBYSERVICE_INFRA']._serialized_start=8171
  _globals['_ARTIFACTSBYSERVICE_INFRA']._serialized_end=8534
  _globals['_ARTIFACTSBYSERVICE_INFRA_ARTIFACTINFO']._serialized_start=8334
  _globals['_ARTIFACTSBYSERVICE_INFRA_ARTIFACTINFO']._serialized_end=8469
  _globals['_ARTIFACTSBYSERVICE_INFRA_ARTIFACTTYPE']._serialized_start=8471
  _globals['_ARTIFACTSBYSERVICE_INFRA_ARTIFACTTYPE']._serialized_end=8534
  _globals['_ARTIFACTSBYSERVICE_SDK']._serialized_start=8537
  _globals['_ARTIFACTSBYSERVICE_SDK']._serialized_end=8889
  _globals['_ARTIFACTSBYSERVICE_SDK_ARTIFACTINFO']._serialized_start=8694
  _globals['_ARTIFACTSBYSERVICE_SDK_ARTIFACTINFO']._serialized_end=8827
  _globals['_ARTIFACTSBYSERVICE_SDK_ARTIFACTTYPE']._serialized_start=8829
  _globals['_ARTIFACTSBYSERVICE_SDK_ARTIFACTTYPE']._serialized_end=8889
  _globals['_UPLOADEDARTIFACTSBYSERVICE']._serialized_start=8892
  _globals['_UPLOADEDARTIFACTSBYSERVICE']._serialized_end=11842
  _globals['_UPLOADEDARTIFACTSBYSERVICE_LEGACY']._serialized_start=9490
  _globals['_UPLOADEDARTIFACTSBYSERVICE_LEGACY']._serialized_end=9744
  _globals['_UPLOADEDARTIFACTSBYSERVICE_LEGACY_ARTIFACTPATHS']._serialized_start=9581
  _globals['_UPLOADEDARTIFACTSBYSERVICE_LEGACY_ARTIFACTPATHS']._serialized_end=9744
  _globals['_UPLOADEDARTIFACTSBYSERVICE_TOOLCHAIN']._serialized_start=9747
  _globals['_UPLOADEDARTIFACTSBYSERVICE_TOOLCHAIN']._serialized_end=10010
  _globals['_UPLOADEDARTIFACTSBYSERVICE_TOOLCHAIN_ARTIFACTPATHS']._serialized_start=9844
  _globals['_UPLOADEDARTIFACTSBYSERVICE_TOOLCHAIN_ARTIFACTPATHS']._serialized_end=10010
  _globals['_UPLOADEDARTIFACTSBYSERVICE_IMAGE']._serialized_start=10013
  _globals['_UPLOADEDARTIFACTSBYSERVICE_IMAGE']._serialized_end=10264
  _globals['_UPLOADEDARTIFACTSBYSERVICE_IMAGE_ARTIFACTPATHS']._serialized_start=10102
  _globals['_UPLOADEDARTIFACTSBYSERVICE_IMAGE_ARTIFACTPATHS']._serialized_end=10264
  _globals['_UPLOADEDARTIFACTSBYSERVICE_PACKAGE']._serialized_start=10267
  _globals['_UPLOADEDARTIFACTSBYSERVICE_PACKAGE']._serialized_end=10524
  _globals['_UPLOADEDARTIFACTSBYSERVICE_PACKAGE_ARTIFACTPATHS']._serialized_start=10360
  _globals['_UPLOADEDARTIFACTSBYSERVICE_PACKAGE_ARTIFACTPATHS']._serialized_end=10524
  _globals['_UPLOADEDARTIFACTSBYSERVICE_SYSROOT']._serialized_start=10527
  _globals['_UPLOADEDARTIFACTSBYSERVICE_SYSROOT']._serialized_end=10784
  _globals['_UPLOADEDARTIFACTSBYSERVICE_SYSROOT_ARTIFACTPATHS']._serialized_start=10620
  _globals['_UPLOADEDARTIFACTSBYSERVICE_SYSROOT_ARTIFACTPATHS']._serialized_end=10784
  _globals['_UPLOADEDARTIFACTSBYSERVICE_TEST']._serialized_start=10787
  _globals['_UPLOADEDARTIFACTSBYSERVICE_TEST']._serialized_end=11035
  _globals['_UPLOADEDARTIFACTSBYSERVICE_TEST_ARTIFACTPATHS']._serialized_start=10874
  _globals['_UPLOADEDARTIFACTSBYSERVICE_TEST_ARTIFACTPATHS']._serialized_end=11035
  _globals['_UPLOADEDARTIFACTSBYSERVICE_FIRMWARE']._serialized_start=11038
  _globals['_UPLOADEDARTIFACTSBYSERVICE_FIRMWARE']._serialized_end=11340
  _globals['_UPLOADEDARTIFACTSBYSERVICE_FIRMWARE_ARTIFACTPATHS']._serialized_start=11133
  _globals['_UPLOADEDARTIFACTSBYSERVICE_FIRMWARE_ARTIFACTPATHS']._serialized_end=11340
  _globals['_UPLOADEDARTIFACTSBYSERVICE_INFRA']._serialized_start=11343
  _globals['_UPLOADEDARTIFACTSBYSERVICE_INFRA']._serialized_end=11594
  _globals['_UPLOADEDARTIFACTSBYSERVICE_INFRA_ARTIFACTPATHS']._serialized_start=11432
  _globals['_UPLOADEDARTIFACTSBYSERVICE_INFRA_ARTIFACTPATHS']._serialized_end=11594
  _globals['_UPLOADEDARTIFACTSBYSERVICE_SDK']._serialized_start=11597
  _globals['_UPLOADEDARTIFACTSBYSERVICE_SDK']._serialized_end=11842
  _globals['_UPLOADEDARTIFACTSBYSERVICE_SDK_ARTIFACTPATHS']._serialized_start=11682
  _globals['_UPLOADEDARTIFACTSBYSERVICE_SDK_ARTIFACTPATHS']._serialized_end=11842
# @@protoc_insertion_point(module_scope)