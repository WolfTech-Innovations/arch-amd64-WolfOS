# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/test/api/publish_gcs_metadata.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen_sdk.chromiumos import storage_path_pb2 as chromiumos_dot_storage__path__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.chromiumos/test/api/publish_gcs_metadata.proto\x12\x13\x63hromiumos.test.api\x1a\x1d\x63hromiumos/storage_path.proto\"\x9b\x01\n\x13XtsArchiverMetadata\x12\x0e\n\x06\x61l_run\x18\x01 \x01(\x08\x12\x0f\n\x07product\x18\x02 \x01(\t\x12\r\n\x05\x62uild\x18\x03 \x01(\t\x12\x1f\n\x17parent_swarming_task_id\x18\x04 \x01(\t\x12\x1a\n\x12results_gcs_prefix\x18\x05 \x01(\t\x12\x17\n\x0f\x61pfe_gcs_prefix\x18\x06 \x01(\t\"\xe7\x01\n\x12PublishGcsMetadata\x12)\n\x08gcs_path\x18\x01 \x01(\x0b\x32\x17.chromiumos.StoragePath\x12@\n\x1fservice_account_creds_file_path\x18\x02 \x01(\x0b\x32\x17.chromiumos.StoragePath\x12G\n\x15xts_archiver_metadata\x18\x03 \x01(\x0b\x32(.chromiumos.test.api.XtsArchiverMetadata\x12\x1b\n\x13\x65nable_xts_archiver\x18\x04 \x01(\x08\x42/Z-go.chromium.org/chromiumos/config/go/test/apib\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chromiumos.test.api.publish_gcs_metadata_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z-go.chromium.org/chromiumos/config/go/test/api'
  _globals['_XTSARCHIVERMETADATA']._serialized_start=103
  _globals['_XTSARCHIVERMETADATA']._serialized_end=258
  _globals['_PUBLISHGCSMETADATA']._serialized_start=261
  _globals['_PUBLISHGCSMETADATA']._serialized_end=492
# @@protoc_insertion_point(module_scope)