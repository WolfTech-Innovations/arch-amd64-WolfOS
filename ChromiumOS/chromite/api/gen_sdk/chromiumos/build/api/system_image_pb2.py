# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/build/api/system_image.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen_sdk.chromiumos.build.api import portage_pb2 as chromiumos_dot_build_dot_api_dot_portage__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'chromiumos/build/api/system_image.proto\x12\x14\x63hromiumos.build.api\x1a\"chromiumos/build/api/portage.proto\"\xd3\x08\n\x0bSystemImage\x12\x35\n\x02id\x18\x01 \x01(\x0b\x32).chromiumos.build.api.SystemImage.ImageId\x12\x41\n\x08metadata\x18\x02 \x01(\x0b\x32/.chromiumos.build.api.SystemImage.BuildMetadata\x1a\x18\n\x07ImageId\x12\r\n\x05value\x18\x01 \x01(\t\x1aV\n\x0b\x42uildTarget\x12G\n\x14portage_build_target\x18\x01 \x01(\x0b\x32).chromiumos.build.api.Portage.BuildTarget\x1a\x81\x06\n\rBuildMetadata\x12\x43\n\x0c\x62uild_target\x18\x01 \x01(\x0b\x32-.chromiumos.build.api.SystemImage.BuildTarget\x12W\n\x0fpackage_summary\x18\x02 \x01(\x0b\x32>.chromiumos.build.api.SystemImage.BuildMetadata.PackageSummary\x12\x37\n\x08packages\x18\x03 \x03(\x0b\x32%.chromiumos.build.api.Portage.Package\x1a\xfd\x02\n\x0ePackageSummary\x12@\n\x03\x61rc\x18\x01 \x01(\x0b\x32\x33.chromiumos.build.api.SystemImage.BuildMetadata.Arc\x12I\n\x06\x63hrome\x18\x02 \x01(\x0b\x32\x39.chromiumos.build.api.SystemImage.BuildMetadata.AshChrome\x12H\n\x07\x63hipset\x18\x03 \x01(\x0b\x32\x37.chromiumos.build.api.SystemImage.BuildMetadata.Chipset\x12\x46\n\x06kernel\x18\x04 \x01(\x0b\x32\x36.chromiumos.build.api.SystemImage.BuildMetadata.Kernel\x12L\n\ttoolchain\x18\x05 \x01(\x0b\x32\x39.chromiumos.build.api.SystemImage.BuildMetadata.Toolchain\x1a&\n\x03\x41rc\x12\x0f\n\x07version\x18\x01 \x01(\t\x12\x0e\n\x06\x62ranch\x18\x02 \x01(\t\x1a\x1c\n\tAshChrome\x12\x0f\n\x07version\x18\x01 \x01(\t\x1a\x1a\n\x07\x43hipset\x12\x0f\n\x07overlay\x18\x01 \x01(\t\x1a\x19\n\x06Kernel\x12\x0f\n\x07version\x18\x01 \x01(\t\x1a\x1c\n\tToolchain\x12\x0f\n\x07version\x18\x01 \x01(\t\x1aT\n\x11\x42uildMetadataList\x12?\n\x06values\x18\x01 \x03(\x0b\x32/.chromiumos.build.api.SystemImage.BuildMetadataB0Z.go.chromium.org/chromiumos/config/go/build/apib\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chromiumos.build.api.system_image_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z.go.chromium.org/chromiumos/config/go/build/api'
  _globals['_SYSTEMIMAGE']._serialized_start=102
  _globals['_SYSTEMIMAGE']._serialized_end=1209
  _globals['_SYSTEMIMAGE_IMAGEID']._serialized_start=239
  _globals['_SYSTEMIMAGE_IMAGEID']._serialized_end=263
  _globals['_SYSTEMIMAGE_BUILDTARGET']._serialized_start=265
  _globals['_SYSTEMIMAGE_BUILDTARGET']._serialized_end=351
  _globals['_SYSTEMIMAGE_BUILDMETADATA']._serialized_start=354
  _globals['_SYSTEMIMAGE_BUILDMETADATA']._serialized_end=1123
  _globals['_SYSTEMIMAGE_BUILDMETADATA_PACKAGESUMMARY']._serialized_start=587
  _globals['_SYSTEMIMAGE_BUILDMETADATA_PACKAGESUMMARY']._serialized_end=968
  _globals['_SYSTEMIMAGE_BUILDMETADATA_ARC']._serialized_start=970
  _globals['_SYSTEMIMAGE_BUILDMETADATA_ARC']._serialized_end=1008
  _globals['_SYSTEMIMAGE_BUILDMETADATA_ASHCHROME']._serialized_start=1010
  _globals['_SYSTEMIMAGE_BUILDMETADATA_ASHCHROME']._serialized_end=1038
  _globals['_SYSTEMIMAGE_BUILDMETADATA_CHIPSET']._serialized_start=1040
  _globals['_SYSTEMIMAGE_BUILDMETADATA_CHIPSET']._serialized_end=1066
  _globals['_SYSTEMIMAGE_BUILDMETADATA_KERNEL']._serialized_start=1068
  _globals['_SYSTEMIMAGE_BUILDMETADATA_KERNEL']._serialized_end=1093
  _globals['_SYSTEMIMAGE_BUILDMETADATA_TOOLCHAIN']._serialized_start=1095
  _globals['_SYSTEMIMAGE_BUILDMETADATA_TOOLCHAIN']._serialized_end=1123
  _globals['_SYSTEMIMAGE_BUILDMETADATALIST']._serialized_start=1125
  _globals['_SYSTEMIMAGE_BUILDMETADATALIST']._serialized_end=1209
# @@protoc_insertion_point(module_scope)
