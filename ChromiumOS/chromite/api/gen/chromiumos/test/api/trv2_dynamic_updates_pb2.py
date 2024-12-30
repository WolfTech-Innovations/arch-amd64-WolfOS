# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/test/api/trv2_dynamic_updates.proto
"""Generated protocol buffer code."""
from chromite.third_party.google.protobuf.internal import builder as _builder
from chromite.third_party.google.protobuf import descriptor as _descriptor
from chromite.third_party.google.protobuf import descriptor_pool as _descriptor_pool
from chromite.third_party.google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.third_party.google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from chromite.api.gen.chromiumos.test.api import trv2_dynamic_pb2 as chromiumos_dot_test_dot_api_dot_trv2__dynamic__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.chromiumos/test/api/trv2_dynamic_updates.proto\x12\x13\x63hromiumos.test.api\x1a\x19google/protobuf/any.proto\x1a&chromiumos/test/api/trv2_dynamic.proto\"\x95\x01\n\x18UserDefinedDynamicUpdate\x12?\n\x11\x66ocal_task_finder\x18\x01 \x01(\x0b\x32$.chromiumos.test.api.FocalTaskFinder\x12\x38\n\rupdate_action\x18\x02 \x01(\x0b\x32!.chromiumos.test.api.UpdateAction\"\xa2\x05\n\x0f\x46ocalTaskFinder\x12;\n\x05\x66irst\x18\x01 \x01(\x0b\x32*.chromiumos.test.api.FocalTaskFinder.FirstH\x00\x12\x39\n\x04last\x18\x02 \x01(\x0b\x32).chromiumos.test.api.FocalTaskFinder.LastH\x00\x12\x43\n\tbeginning\x18\x03 \x01(\x0b\x32..chromiumos.test.api.FocalTaskFinder.BeginningH\x00\x12\x37\n\x03\x65nd\x18\x04 \x01(\x0b\x32(.chromiumos.test.api.FocalTaskFinder.EndH\x00\x12Y\n\x15\x62y_dynamic_identifier\x18\x05 \x01(\x0b\x32\x38.chromiumos.test.api.FocalTaskFinder.ByDynamicIdentifierH\x00\x1aI\n\x05\x46irst\x12@\n\ttask_type\x18\x01 \x01(\x0e\x32-.chromiumos.test.api.FocalTaskFinder.TaskType\x1aH\n\x04Last\x12@\n\ttask_type\x18\x01 \x01(\x0e\x32-.chromiumos.test.api.FocalTaskFinder.TaskType\x1a\x0b\n\tBeginning\x1a\x05\n\x03\x45nd\x1a\x31\n\x13\x42yDynamicIdentifier\x12\x1a\n\x12\x64ynamic_identifier\x18\x01 \x01(\t\"X\n\x08TaskType\x12\r\n\tPROVISION\x10\x00\x12\x0b\n\x07PRETEST\x10\x01\x12\x08\n\x04TEST\x10\x02\x12\x0c\n\x08POSTTEST\x10\x03\x12\x0b\n\x07PUBLISH\x10\x04\x12\x0b\n\x07GENERIC\x10\x05\x42\x08\n\x06\x66inder\"\xca\x05\n\x0cUpdateAction\x12:\n\x06insert\x18\x01 \x01(\x0b\x32(.chromiumos.test.api.UpdateAction.InsertH\x00\x12:\n\x06remove\x18\x02 \x01(\x0b\x32(.chromiumos.test.api.UpdateAction.RemoveH\x00\x12:\n\x06modify\x18\x03 \x01(\x0b\x32(.chromiumos.test.api.UpdateAction.ModifyH\x00\x1a\xcc\x01\n\x06Insert\x12H\n\x0binsert_type\x18\x01 \x01(\x0e\x32\x33.chromiumos.test.api.UpdateAction.Insert.InsertType\x12\x44\n\x04task\x18\x02 \x01(\x0b\x32\x36.chromiumos.test.api.CrosTestRunnerDynamicRequest.Task\"2\n\nInsertType\x12\n\n\x06\x41PPEND\x10\x00\x12\x0b\n\x07PREPEND\x10\x01\x12\x0b\n\x07REPLACE\x10\x02\x1a\x08\n\x06Remove\x1a\xa2\x02\n\x06Modify\x12L\n\rmodifications\x18\x01 \x03(\x0b\x32\x35.chromiumos.test.api.UpdateAction.Modify.Modification\x1a\xc9\x01\n\x0cModification\x12%\n\x07payload\x18\x01 \x01(\x0b\x32\x14.google.protobuf.Any\x12]\n\x0cinstructions\x18\x02 \x03(\x0b\x32G.chromiumos.test.api.UpdateAction.Modify.Modification.InstructionsEntry\x1a\x33\n\x11InstructionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42\x08\n\x06\x61\x63tionB/Z-go.chromium.org/chromiumos/config/go/test/apib\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chromiumos.test.api.trv2_dynamic_updates_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z-go.chromium.org/chromiumos/config/go/test/api'
  _UPDATEACTION_MODIFY_MODIFICATION_INSTRUCTIONSENTRY._options = None
  _UPDATEACTION_MODIFY_MODIFICATION_INSTRUCTIONSENTRY._serialized_options = b'8\001'
  _USERDEFINEDDYNAMICUPDATE._serialized_start=139
  _USERDEFINEDDYNAMICUPDATE._serialized_end=288
  _FOCALTASKFINDER._serialized_start=291
  _FOCALTASKFINDER._serialized_end=965
  _FOCALTASKFINDER_FIRST._serialized_start=647
  _FOCALTASKFINDER_FIRST._serialized_end=720
  _FOCALTASKFINDER_LAST._serialized_start=722
  _FOCALTASKFINDER_LAST._serialized_end=794
  _FOCALTASKFINDER_BEGINNING._serialized_start=796
  _FOCALTASKFINDER_BEGINNING._serialized_end=807
  _FOCALTASKFINDER_END._serialized_start=809
  _FOCALTASKFINDER_END._serialized_end=814
  _FOCALTASKFINDER_BYDYNAMICIDENTIFIER._serialized_start=816
  _FOCALTASKFINDER_BYDYNAMICIDENTIFIER._serialized_end=865
  _FOCALTASKFINDER_TASKTYPE._serialized_start=867
  _FOCALTASKFINDER_TASKTYPE._serialized_end=955
  _UPDATEACTION._serialized_start=968
  _UPDATEACTION._serialized_end=1682
  _UPDATEACTION_INSERT._serialized_start=1165
  _UPDATEACTION_INSERT._serialized_end=1369
  _UPDATEACTION_INSERT_INSERTTYPE._serialized_start=1319
  _UPDATEACTION_INSERT_INSERTTYPE._serialized_end=1369
  _UPDATEACTION_REMOVE._serialized_start=1371
  _UPDATEACTION_REMOVE._serialized_end=1379
  _UPDATEACTION_MODIFY._serialized_start=1382
  _UPDATEACTION_MODIFY._serialized_end=1672
  _UPDATEACTION_MODIFY_MODIFICATION._serialized_start=1471
  _UPDATEACTION_MODIFY_MODIFICATION._serialized_end=1672
  _UPDATEACTION_MODIFY_MODIFICATION_INSTRUCTIONSENTRY._serialized_start=1621
  _UPDATEACTION_MODIFY_MODIFICATION_INSTRUCTIONSENTRY._serialized_end=1672
# @@protoc_insertion_point(module_scope)
