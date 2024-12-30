# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromite/api/copybot.proto
"""Generated protocol buffer code."""
from chromite.third_party.google.protobuf.internal import builder as _builder
from chromite.third_party.google.protobuf import descriptor as _descriptor
from chromite.third_party.google.protobuf import descriptor_pool as _descriptor_pool
from chromite.third_party.google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen.chromite.api import build_api_pb2 as chromite_dot_api_dot_build__api__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1a\x63hromite/api/copybot.proto\x12\x0c\x63hromite.api\x1a\x1c\x63hromite/api/build_api.proto\"\xd4\x0e\n\x11RunCopybotRequest\x12\x36\n\x08upstream\x18\x01 \x01(\x0b\x32$.chromite.api.RunCopybotRequest.Repo\x12\x38\n\ndownstream\x18\x02 \x01(\x0b\x32$.chromite.api.RunCopybotRequest.Repo\x12\r\n\x05topic\x18\x03 \x01(\t\x12;\n\x06labels\x18\x04 \x03(\x0b\x32+.chromite.api.RunCopybotRequest.GerritLabel\x12=\n\treviewers\x18\x05 \x03(\x0b\x32*.chromite.api.RunCopybotRequest.GerritUser\x12\x37\n\x03\x63\x63s\x18\x06 \x03(\x0b\x32*.chromite.api.RunCopybotRequest.GerritUser\x12\x17\n\x0fprepend_subject\x18\x07 \x01(\t\x12V\n\x17merge_conflict_behavior\x18\x08 \x01(\x0e\x32\x35.chromite.api.RunCopybotRequest.MergeConflictBehavior\x12\x46\n\x15\x65xclude_file_patterns\x18\t \x03(\x0b\x32\'.chromite.api.RunCopybotRequest.Pattern\x12H\n\x12keep_pseudoheaders\x18\n \x03(\x0b\x32,.chromite.api.RunCopybotRequest.Pseudoheader\x12\x19\n\x11\x61\x64\x64_signed_off_by\x18\x0b \x01(\x08\x12\x0f\n\x07\x64ry_run\x18\x0c \x01(\x08\x12@\n\x0cpush_options\x18\r \x03(\x0b\x32*.chromite.api.RunCopybotRequest.PushOption\x12\x39\n\x08hashtags\x18\x0e \x03(\x0b\x32\'.chromite.api.RunCopybotRequest.Hashtag\x12\x16\n\x0eupstream_limit\x18\x0f \x01(\r\x12\x18\n\x10\x64ownstream_limit\x18\x10 \x01(\r\x12\x42\n\rinclude_paths\x18\x11 \x03(\x0b\x32+.chromite.api.RunCopybotRequest.IncludePath\x12\x11\n\tbuild_url\x18\x12 \x01(\t\x12\x10\n\x08\x62uild_id\x18\x13 \x01(\t\x12\x39\n\x08job_name\x18\x14 \x01(\x0b\x32\'.chromite.api.RunCopybotRequest.JobName\x12?\n\x0eskip_job_names\x18\x15 \x03(\x0b\x32\'.chromite.api.RunCopybotRequest.JobName\x12H\n\x10pantheon_secrets\x18\x16 \x03(\x0b\x32..chromite.api.RunCopybotRequest.PantheonSecret\x12\x15\n\rupstream_hash\x18\x17 \x01(\t\x12\x17\n\x0f\x64ownstream_hash\x18\x18 \x01(\t\x12@\n\x0cskip_authors\x18\x19 \x03(\x0b\x32*.chromite.api.RunCopybotRequest.GerritUser\x12=\n\ninsert_msg\x18\x1a \x03(\x0b\x32).chromite.api.RunCopybotRequest.CommitMsg\x1a\x34\n\x04Repo\x12\x0b\n\x03url\x18\x01 \x01(\t\x12\x0e\n\x06\x62ranch\x18\x02 \x01(\t\x12\x0f\n\x07subtree\x18\x03 \x01(\t\x1a\x1a\n\nGerritUser\x12\x0c\n\x04user\x18\x01 \x01(\t\x1a\x1c\n\x0bGerritLabel\x12\r\n\x05label\x18\x01 \x01(\t\x1a\x1a\n\x07Pattern\x12\x0f\n\x07pattern\x18\x01 \x01(\t\x1a\x1c\n\x0cPseudoheader\x12\x0c\n\x04name\x18\x01 \x01(\t\x1a\x19\n\nPushOption\x12\x0b\n\x03opt\x18\x01 \x01(\t\x1a\x1a\n\x07Hashtag\x12\x0f\n\x07hashtag\x18\x01 \x01(\t\x1a\x1b\n\x0bIncludePath\x12\x0c\n\x04path\x18\x01 \x01(\t\x1a\x1b\n\x07JobName\x12\x10\n\x08job_name\x18\x01 \x01(\t\x1a%\n\x0ePantheonSecret\x12\x13\n\x0bsecret_name\x18\x01 \x01(\t\x1a\x34\n\tCommitMsg\x12\x13\n\x0bline_number\x18\x01 \x01(\r\x12\x12\n\ninsert_txt\x18\x02 \x01(\t\"\xd2\x01\n\x15MergeConflictBehavior\x12\'\n#MERGE_CONFLICT_BEHAVIOR_UNSPECIFIED\x10\x00\x12 \n\x1cMERGE_CONFLICT_BEHAVIOR_SKIP\x10\x01\x12 \n\x1cMERGE_CONFLICT_BEHAVIOR_FAIL\x10\x02\x12 \n\x1cMERGE_CONFLICT_BEHAVIOR_STOP\x10\x03\x12*\n&MERGE_CONFLICT_BEHAVIOR_ALLOW_CONFLICT\x10\x04\"\xfd\x02\n\x12RunCopybotResponse\x12\x46\n\x0e\x66\x61ilure_reason\x18\x01 \x01(\x0e\x32..chromite.api.RunCopybotResponse.FailureReason\x12M\n\x0fmerge_conflicts\x18\x02 \x03(\x0b\x32\x34.chromite.api.RunCopybotResponse.MergeConflictCommit\x1a#\n\x13MergeConflictCommit\x12\x0c\n\x04hash\x18\x01 \x01(\t\"\xaa\x01\n\rFailureReason\x12\x13\n\x0f\x46\x41ILURE_UNKNOWN\x10\x00\x12 \n\x1c\x46\x41ILURE_UPSTREAM_FETCH_ERROR\x10\x01\x12\"\n\x1e\x46\x41ILURE_DOWNSTREAM_FETCH_ERROR\x10\x02\x12!\n\x1d\x46\x41ILURE_DOWNSTREAM_PUSH_ERROR\x10\x03\x12\x1b\n\x17\x46\x41ILURE_MERGE_CONFLICTS\x10\x04\x32p\n\x0e\x43opybotService\x12O\n\nRunCopybot\x12\x1f.chromite.api.RunCopybotRequest\x1a .chromite.api.RunCopybotResponse\x1a\r\xc2\xed\x1a\t\n\x07\x63opybotB8Z6go.chromium.org/chromiumos/infra/proto/go/chromite/apib\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chromite.api.copybot_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z6go.chromium.org/chromiumos/infra/proto/go/chromite/api'
  _COPYBOTSERVICE._options = None
  _COPYBOTSERVICE._serialized_options = b'\302\355\032\t\n\007copybot'
  _RUNCOPYBOTREQUEST._serialized_start=75
  _RUNCOPYBOTREQUEST._serialized_end=1951
  _RUNCOPYBOTREQUEST_REPO._serialized_start=1364
  _RUNCOPYBOTREQUEST_REPO._serialized_end=1416
  _RUNCOPYBOTREQUEST_GERRITUSER._serialized_start=1418
  _RUNCOPYBOTREQUEST_GERRITUSER._serialized_end=1444
  _RUNCOPYBOTREQUEST_GERRITLABEL._serialized_start=1446
  _RUNCOPYBOTREQUEST_GERRITLABEL._serialized_end=1474
  _RUNCOPYBOTREQUEST_PATTERN._serialized_start=1476
  _RUNCOPYBOTREQUEST_PATTERN._serialized_end=1502
  _RUNCOPYBOTREQUEST_PSEUDOHEADER._serialized_start=1504
  _RUNCOPYBOTREQUEST_PSEUDOHEADER._serialized_end=1532
  _RUNCOPYBOTREQUEST_PUSHOPTION._serialized_start=1534
  _RUNCOPYBOTREQUEST_PUSHOPTION._serialized_end=1559
  _RUNCOPYBOTREQUEST_HASHTAG._serialized_start=1561
  _RUNCOPYBOTREQUEST_HASHTAG._serialized_end=1587
  _RUNCOPYBOTREQUEST_INCLUDEPATH._serialized_start=1589
  _RUNCOPYBOTREQUEST_INCLUDEPATH._serialized_end=1616
  _RUNCOPYBOTREQUEST_JOBNAME._serialized_start=1618
  _RUNCOPYBOTREQUEST_JOBNAME._serialized_end=1645
  _RUNCOPYBOTREQUEST_PANTHEONSECRET._serialized_start=1647
  _RUNCOPYBOTREQUEST_PANTHEONSECRET._serialized_end=1684
  _RUNCOPYBOTREQUEST_COMMITMSG._serialized_start=1686
  _RUNCOPYBOTREQUEST_COMMITMSG._serialized_end=1738
  _RUNCOPYBOTREQUEST_MERGECONFLICTBEHAVIOR._serialized_start=1741
  _RUNCOPYBOTREQUEST_MERGECONFLICTBEHAVIOR._serialized_end=1951
  _RUNCOPYBOTRESPONSE._serialized_start=1954
  _RUNCOPYBOTRESPONSE._serialized_end=2335
  _RUNCOPYBOTRESPONSE_MERGECONFLICTCOMMIT._serialized_start=2127
  _RUNCOPYBOTRESPONSE_MERGECONFLICTCOMMIT._serialized_end=2162
  _RUNCOPYBOTRESPONSE_FAILUREREASON._serialized_start=2165
  _RUNCOPYBOTRESPONSE_FAILUREREASON._serialized_end=2335
  _COPYBOTSERVICE._serialized_start=2337
  _COPYBOTSERVICE._serialized_end=2449
# @@protoc_insertion_point(module_scope)
