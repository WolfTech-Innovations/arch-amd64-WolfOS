# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/config/api/test/xmlrpc/xmlrpc.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.chromiumos/config/api/test/xmlrpc/xmlrpc.proto\x12!chromiumos.config.api.test.xmlrpc\"\xfb\x01\n\x05Value\x12\r\n\x03int\x18\x02 \x01(\x11H\x00\x12\x11\n\x07\x62oolean\x18\x03 \x01(\x08H\x00\x12\x10\n\x06string\x18\x04 \x01(\tH\x00\x12\x10\n\x06\x64ouble\x18\x05 \x01(\x01H\x00\x12\x12\n\x08\x64\x61tetime\x18\x06 \x01(\tH\x00\x12\x10\n\x06\x62\x61se64\x18\x07 \x01(\x0cH\x00\x12;\n\x06struct\x18\x08 \x01(\x0b\x32).chromiumos.config.api.test.xmlrpc.StructH\x00\x12\x39\n\x05\x61rray\x18\t \x01(\x0b\x32(.chromiumos.config.api.test.xmlrpc.ArrayH\x00\x42\x0e\n\x0cscalar_oneof\"\xab\x01\n\x06Struct\x12G\n\x07members\x18\x01 \x03(\x0b\x32\x36.chromiumos.config.api.test.xmlrpc.Struct.MembersEntry\x1aX\n\x0cMembersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x37\n\x05value\x18\x02 \x01(\x0b\x32(.chromiumos.config.api.test.xmlrpc.Value:\x02\x38\x01\"A\n\x05\x41rray\x12\x38\n\x06values\x18\x01 \x03(\x0b\x32(.chromiumos.config.api.test.xmlrpc.ValueB6Z4go.chromium.org/chromiumos/config/go/api/test/xmlrpcb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chromiumos.config.api.test.xmlrpc.xmlrpc_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z4go.chromium.org/chromiumos/config/go/api/test/xmlrpc'
  _STRUCT_MEMBERSENTRY._options = None
  _STRUCT_MEMBERSENTRY._serialized_options = b'8\001'
  _globals['_VALUE']._serialized_start=86
  _globals['_VALUE']._serialized_end=337
  _globals['_STRUCT']._serialized_start=340
  _globals['_STRUCT']._serialized_end=511
  _globals['_STRUCT_MEMBERSENTRY']._serialized_start=423
  _globals['_STRUCT_MEMBERSENTRY']._serialized_end=511
  _globals['_ARRAY']._serialized_start=513
  _globals['_ARRAY']._serialized_end=578
# @@protoc_insertion_point(module_scope)
