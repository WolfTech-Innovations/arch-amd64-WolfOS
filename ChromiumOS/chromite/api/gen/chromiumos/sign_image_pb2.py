# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/sign_image.proto
"""Generated protocol buffer code."""
from chromite.third_party.google.protobuf.internal import builder as _builder
from chromite.third_party.google.protobuf import descriptor as _descriptor
from chromite.third_party.google.protobuf import descriptor_pool as _descriptor_pool
from chromite.third_party.google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1b\x63hromiumos/sign_image.proto\x12\nchromiumos\"\xbe\x01\n\x10\x43r50Instructions\x12\x33\n\x06target\x18\x01 \x01(\x0e\x32#.chromiumos.Cr50Instructions.Target\x12\x11\n\tdevice_id\x18\x02 \x01(\t\"b\n\x06Target\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\n\n\x06PREPVT\x10\x01\x12\x15\n\x11RELEASE_CANDIDATE\x10\x02\x12\x0f\n\x0bNODE_LOCKED\x10\x03\x12\x13\n\x0fGENERAL_RELEASE\x10\x04\"\xc9\x01\n\x0fGscInstructions\x12\x32\n\x06target\x18\x01 \x01(\x0e\x32\".chromiumos.GscInstructions.Target\x12\x11\n\tdevice_id\x18\x02 \x01(\t\"o\n\x06Target\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\n\n\x06PREPVT\x10\x01\x12\x15\n\x11RELEASE_CANDIDATE\x10\x02\x12\x0f\n\x0bNODE_LOCKED\x10\x03\x12\x13\n\x0fGENERAL_RELEASE\x10\x04\x12\x0b\n\x07NIGHTLY\x10\x05*_\n\nSignerType\x12\x16\n\x12SIGNER_UNSPECIFIED\x10\x00\x12\x15\n\x11SIGNER_PRODUCTION\x10\x01\x12\x12\n\x0eSIGNER_STAGING\x10\x02\x12\x0e\n\nSIGNER_DEV\x10\x03\x42Y\n!com.google.chrome.crosinfra.protoZ4go.chromium.org/chromiumos/infra/proto/go/chromiumosb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chromiumos.sign_image_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n!com.google.chrome.crosinfra.protoZ4go.chromium.org/chromiumos/infra/proto/go/chromiumos'
  _SIGNERTYPE._serialized_start=440
  _SIGNERTYPE._serialized_end=535
  _CR50INSTRUCTIONS._serialized_start=44
  _CR50INSTRUCTIONS._serialized_end=234
  _CR50INSTRUCTIONS_TARGET._serialized_start=136
  _CR50INSTRUCTIONS_TARGET._serialized_end=234
  _GSCINSTRUCTIONS._serialized_start=237
  _GSCINSTRUCTIONS._serialized_end=438
  _GSCINSTRUCTIONS_TARGET._serialized_start=327
  _GSCINSTRUCTIONS_TARGET._serialized_end=438
# @@protoc_insertion_point(module_scope)
