# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/test/lab/api/dut.proto
"""Generated protocol buffer code."""
from chromite.third_party.google.protobuf.internal import builder as _builder
from chromite.third_party.google.protobuf import descriptor as _descriptor
from chromite.third_party.google.protobuf import descriptor_pool as _descriptor_pool
from chromite.third_party.google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen.chromiumos.config.api import device_config_id_pb2 as chromiumos_dot_config_dot_api_dot_device__config__id__pb2
from chromite.api.gen.chromiumos.test.lab.api import ip_endpoint_pb2 as chromiumos_dot_test_dot_lab_dot_api_dot_ip__endpoint__pb2
from chromite.api.gen.chromiumos.test.lab.api import pasit_host_pb2 as chromiumos_dot_test_dot_lab_dot_api_dot_pasit__host__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!chromiumos/test/lab/api/dut.proto\x12\x17\x63hromiumos.test.lab.api\x1a,chromiumos/config/api/device_config_id.proto\x1a)chromiumos/test/lab/api/ip_endpoint.proto\x1a(chromiumos/test/lab/api/pasit_host.proto\"\xfc\r\n\x03\x44ut\x12+\n\x02id\x18\x01 \x01(\x0b\x32\x1f.chromiumos.test.lab.api.Dut.Id\x12\x39\n\x08\x63hromeos\x18\x02 \x01(\x0b\x32%.chromiumos.test.lab.api.Dut.ChromeOSH\x00\x12\x37\n\x07\x61ndroid\x18\x03 \x01(\x0b\x32$.chromiumos.test.lab.api.Dut.AndroidH\x00\x12\x39\n\x08\x64\x65vboard\x18\x05 \x01(\x0b\x32%.chromiumos.test.lab.api.Dut.DevboardH\x00\x12:\n\x0c\x63\x61\x63he_server\x18\x04 \x01(\x0b\x32$.chromiumos.test.lab.api.CacheServer\x12\x38\n\x0bwifi_secret\x18\x06 \x01(\x0b\x32#.chromiumos.test.lab.api.WifiSecret\x1a\x13\n\x02Id\x12\r\n\x05value\x18\x01 \x01(\t\x1a\x8a\x08\n\x08\x43hromeOS\x12?\n\x10\x64\x65vice_config_id\x18\x03 \x01(\x0b\x32%.chromiumos.config.api.DeviceConfigId\x12\x30\n\x03ssh\x18\x02 \x01(\x0b\x32#.chromiumos.test.lab.api.IpEndpoint\x12\x0c\n\x04name\x18\x0f \x01(\t\x12\x34\n\tdut_model\x18\x0e \x01(\x0b\x32!.chromiumos.test.lab.api.DutModel\x12-\n\x05servo\x18\x04 \x01(\x0b\x32\x1e.chromiumos.test.lab.api.Servo\x12\x35\n\tchameleon\x18\x05 \x01(\x0b\x32\".chromiumos.test.lab.api.Chameleon\x12)\n\x03rpm\x18\x06 \x01(\x0b\x32\x1c.chromiumos.test.lab.api.RPM\x12\x41\n\x10\x65xternal_cameras\x18\x07 \x03(\x0b\x32\'.chromiumos.test.lab.api.ExternalCamera\x12-\n\x05\x61udio\x18\x08 \x01(\x0b\x32\x1e.chromiumos.test.lab.api.Audio\x12+\n\x04wifi\x18\t \x01(\x0b\x32\x1d.chromiumos.test.lab.api.Wifi\x12-\n\x05touch\x18\n \x01(\x0b\x32\x1e.chromiumos.test.lab.api.Touch\x12\x35\n\tcamerabox\x18\x0b \x01(\x0b\x32\".chromiumos.test.lab.api.Camerabox\x12.\n\x06\x63\x61\x62les\x18\x0c \x03(\x0b\x32\x1e.chromiumos.test.lab.api.Cable\x12\x33\n\x08\x63\x65llular\x18\r \x01(\x0b\x32!.chromiumos.test.lab.api.Cellular\x12\x16\n\x0ehwid_component\x18\x10 \x03(\t\x12?\n\x0f\x62luetooth_peers\x18\x11 \x03(\x0b\x32&.chromiumos.test.lab.api.BluetoothPeer\x12\x0b\n\x03sku\x18\x12 \x01(\t\x12\x0c\n\x04hwid\x18\x13 \x01(\t\x12-\n\x05phase\x18\x14 \x01(\x0e\x32\x1e.chromiumos.test.lab.api.Phase\x12\x33\n\tsim_infos\x18\x15 \x03(\x0b\x32 .chromiumos.test.lab.api.SIMInfo\x12\x36\n\nmodem_info\x18\x16 \x01(\x0b\x32\".chromiumos.test.lab.api.ModemInfo\x12\x36\n\npasit_host\x18\x17 \x01(\x0b\x32\".chromiumos.test.lab.api.PasitHostJ\x04\x08\x01\x10\x02\x1a\xa6\x01\n\x07\x41ndroid\x12@\n\x13\x61ssociated_hostname\x18\x01 \x01(\x0b\x32#.chromiumos.test.lab.api.IpEndpoint\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x15\n\rserial_number\x18\x03 \x01(\t\x12\x34\n\tdut_model\x18\x04 \x01(\x0b\x32!.chromiumos.test.lab.api.DutModel\x1a\xcb\x01\n\x08\x44\x65vboard\x12\x12\n\nboard_type\x18\x01 \x01(\t\x12\x19\n\x11ultradebug_serial\x18\x02 \x01(\t\x12-\n\x05servo\x18\x03 \x01(\x0b\x32\x1e.chromiumos.test.lab.api.Servo\x12\x1d\n\x15\x66ingerprint_module_id\x18\x04 \x01(\t\x12\x0c\n\x04name\x18\x05 \x01(\t\x12\x34\n\tdut_model\x18\x06 \x01(\x0b\x32!.chromiumos.test.lab.api.DutModelB\n\n\x08\x64ut_type\"4\n\x08\x44utModel\x12\x14\n\x0c\x62uild_target\x18\x01 \x01(\t\x12\x12\n\nmodel_name\x18\x02 \x01(\t\"\x8f\x01\n\x0b\x44utTopology\x12\x33\n\x02id\x18\x03 \x01(\x0b\x32\'.chromiumos.test.lab.api.DutTopology.Id\x12*\n\x04\x64uts\x18\x04 \x03(\x0b\x32\x1c.chromiumos.test.lab.api.Dut\x1a\x13\n\x02Id\x12\r\n\x05value\x18\x01 \x01(\tJ\x04\x08\x01\x10\x02J\x04\x08\x02\x10\x03\")\n\x05\x41udio\x12\x11\n\taudio_box\x18\x01 \x01(\x08\x12\r\n\x05\x61trus\x18\x02 \x01(\x08\"\x95\x01\n\x05\x43\x61\x62le\x12\x31\n\x04type\x18\x01 \x01(\x0e\x32#.chromiumos.test.lab.api.Cable.Type\"Y\n\x04Type\x12\x14\n\x10TYPE_UNSPECIFIED\x10\x00\x12\r\n\tAUDIOJACK\x10\x01\x12\x0c\n\x08USBAUDIO\x10\x02\x12\x0f\n\x0bUSBPRINTING\x10\x03\x12\r\n\tHDMIAUDIO\x10\x04\"C\n\x0b\x43\x61\x63heServer\x12\x34\n\x07\x61\x64\x64ress\x18\x01 \x01(\x0b\x32#.chromiumos.test.lab.api.IpEndpoint\"}\n\tCamerabox\x12\x39\n\x06\x66\x61\x63ing\x18\x01 \x01(\x0e\x32).chromiumos.test.lab.api.Camerabox.Facing\"5\n\x06\x46\x61\x63ing\x12\x16\n\x12\x46\x41\x43ING_UNSPECIFIED\x10\x00\x12\x08\n\x04\x42\x41\x43K\x10\x01\x12\t\n\x05\x46RONT\x10\x02\"\xa3\x01\n\x08\x43\x65llular\x12=\n\toperators\x18\x01 \x03(\x0e\x32*.chromiumos.test.lab.api.Cellular.Operator\x12\x0f\n\x07\x63\x61rrier\x18\x02 \x01(\t\"G\n\x08Operator\x12\x18\n\x14OPERATOR_UNSPECIFIED\x10\x00\x12\x07\n\x03\x41TT\x10\x01\x12\x0b\n\x07VERIZON\x10\x02\x12\x0b\n\x07TMOBILE\x10\x03\"\x8e\x01\n\tModemInfo\x12\x30\n\x04type\x18\x01 \x01(\x0e\x32\".chromiumos.test.lab.api.ModemType\x12\x0c\n\x04imei\x18\x02 \x01(\t\x12\x17\n\x0fsupported_bands\x18\x03 \x01(\t\x12\x11\n\tsim_count\x18\x04 \x01(\x05\x12\x15\n\rmodel_variant\x18\x05 \x01(\t\"\xa9\x01\n\x07SIMInfo\x12\x0f\n\x07slot_id\x18\x01 \x01(\x05\x12.\n\x04type\x18\x02 \x01(\x0e\x32 .chromiumos.test.lab.api.SIMType\x12\x0b\n\x03\x65id\x18\x03 \x01(\t\x12\x11\n\ttest_esim\x18\x04 \x01(\x08\x12=\n\x0cprofile_info\x18\x05 \x03(\x0b\x32\'.chromiumos.test.lab.api.SIMProfileInfo\"\xc6\x03\n\x0eSIMProfileInfo\x12\r\n\x05iccid\x18\x01 \x01(\t\x12\x0f\n\x07sim_pin\x18\x02 \x01(\t\x12\x0f\n\x07sim_puk\x18\x03 \x01(\t\x12>\n\x0c\x63\x61rrier_name\x18\x04 \x01(\x0e\x32(.chromiumos.test.lab.api.NetworkProvider\x12\x12\n\nown_number\x18\x05 \x01(\t\x12<\n\x05state\x18\x06 \x01(\x0e\x32-.chromiumos.test.lab.api.SIMProfileInfo.State\x12\x41\n\x08\x66\x65\x61tures\x18\x07 \x03(\x0e\x32/.chromiumos.test.lab.api.SIMProfileInfo.Feature\"_\n\x05State\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\n\n\x06\x42ROKEN\x10\x01\x12\n\n\x06LOCKED\x10\x02\x12\x0e\n\nNO_NETWORK\x10\x03\x12\x0b\n\x07WORKING\x10\x04\x12\x10\n\x0cWRONG_CONFIG\x10\x05\"M\n\x07\x46\x65\x61ture\x12\x17\n\x13\x46\x45\x41TURE_UNSPECIFIED\x10\x00\x12\x18\n\x14\x46\x45\x41TURE_LIVE_NETWORK\x10\x01\x12\x0f\n\x0b\x46\x45\x41TURE_SMS\x10\x02\"\xac\x03\n\tChameleon\x12\x42\n\x0bperipherals\x18\x01 \x03(\x0e\x32-.chromiumos.test.lab.api.Chameleon.Peripheral\x12\x13\n\x0b\x61udio_board\x18\x02 \x01(\x08\x12\x37\n\x05state\x18\x03 \x01(\x0e\x32(.chromiumos.test.lab.api.PeripheralState\x12\x10\n\x08hostname\x18\x04 \x01(\t\x12\x36\n\x05types\x18\x05 \x03(\x0e\x32\'.chromiumos.test.lab.api.Chameleon.Type\"\x94\x01\n\nPeripheral\x12\x1a\n\x16PERIPHERAL_UNSPECIFIED\x10\x00\x12\n\n\x06\x42T_HID\x10\x01\x12\x06\n\x02\x44P\x10\x02\x12\x0b\n\x07\x44P_HDMI\x10\x03\x12\x07\n\x03VGA\x10\x04\x12\x08\n\x04HDMI\x10\x05\x12\x0e\n\nBT_BLE_HID\x10\x06\x12\x10\n\x0c\x42T_A2DP_SINK\x10\x07\x12\x0b\n\x07\x42T_PEER\x10\x08\x12\x07\n\x03RPI\x10\t\",\n\x04Type\x12\x14\n\x10TYPE_UNSPECIFIED\x10\x00\x12\x06\n\x02V2\x10\x01\x12\x06\n\x02V3\x10\x02\"\x83\x01\n\x0e\x45xternalCamera\x12:\n\x04type\x18\x01 \x01(\x0e\x32,.chromiumos.test.lab.api.ExternalCamera.Type\"5\n\x04Type\x12\x14\n\x10TYPE_UNSPECIFIED\x10\x00\x12\n\n\x06HUDDLY\x10\x01\x12\x0b\n\x07PTZPRO2\x10\x02\"\x9f\x02\n\x03RPM\x12\x0f\n\x07present\x18\x01 \x01(\x08\x12=\n\x10\x66rontend_address\x18\x02 \x01(\x0b\x32#.chromiumos.test.lab.api.IpEndpoint\x12@\n\x13power_unit_hostname\x18\x03 \x01(\x0b\x32#.chromiumos.test.lab.api.IpEndpoint\x12\x19\n\x11power_unit_outlet\x18\x04 \x01(\t\x12;\n\x0ehydra_hostname\x18\x05 \x01(\x0b\x32#.chromiumos.test.lab.api.IpEndpoint\x12.\n\x04type\x18\x06 \x01(\x0e\x32 .chromiumos.test.lab.api.RPMType\"\x9e\x01\n\x05Servo\x12\x0f\n\x07present\x18\x01 \x01(\x08\x12;\n\x0eservod_address\x18\x02 \x01(\x0b\x32#.chromiumos.test.lab.api.IpEndpoint\x12\x0e\n\x06serial\x18\x03 \x01(\t\x12\x37\n\x05state\x18\x04 \x01(\x0e\x32(.chromiumos.test.lab.api.PeripheralState\"\x15\n\x05Touch\x12\x0c\n\x04mimo\x18\x01 \x01(\x08\"\xe6\x01\n\x04Wifi\x12>\n\x0b\x65nvironment\x18\x01 \x01(\x0e\x32).chromiumos.test.lab.api.Wifi.Environment\x12\x35\n\x07\x61ntenna\x18\x02 \x01(\x0b\x32$.chromiumos.test.lab.api.WifiAntenna\"g\n\x0b\x45nvironment\x12\x1b\n\x17\x45NVIRONMENT_UNSPECIFIED\x10\x00\x12\x0c\n\x08STANDARD\x10\x01\x12\r\n\tWIFI_CELL\x10\x02\x12\t\n\x05\x43HAOS\x10\x03\x12\x13\n\x0fROUTER_802_11AX\x10\x04\"\x95\x01\n\x0bWifiAntenna\x12\x43\n\nconnection\x18\x01 \x01(\x0e\x32/.chromiumos.test.lab.api.WifiAntenna.Connection\"A\n\nConnection\x12\x1a\n\x16\x43ONNECTION_UNSPECIFIED\x10\x00\x12\x0e\n\nCONDUCTIVE\x10\x01\x12\x07\n\x03OTA\x10\x02\"Z\n\rBluetoothPeer\x12\x10\n\x08hostname\x18\x01 \x01(\t\x12\x37\n\x05state\x18\x02 \x01(\x0e\x32(.chromiumos.test.lab.api.PeripheralState\">\n\nWifiSecret\x12\x0c\n\x04ssid\x18\x01 \x01(\t\x12\x10\n\x08security\x18\x02 \x01(\t\x12\x10\n\x08password\x18\x03 \x01(\t*\xbe\x02\n\tModemType\x12\x1a\n\x16MODEM_TYPE_UNSPECIFIED\x10\x00\x12\x1a\n\x16MODEM_TYPE_UNSUPPORTED\x10\x08\x12\x1e\n\x1aMODEM_TYPE_QUALCOMM_SC7180\x10\x01\x12\x1e\n\x1aMODEM_TYPE_FIBOCOMM_L850GL\x10\x02\x12\x14\n\x10MODEM_TYPE_NL668\x10\x03\x12\x14\n\x10MODEM_TYPE_FM350\x10\x04\x12\x14\n\x10MODEM_TYPE_FM101\x10\x05\x12\x1e\n\x1aMODEM_TYPE_QUALCOMM_SC7280\x10\x06\x12\x14\n\x10MODEM_TYPE_EM060\x10\x07\x12\x14\n\x10MODEM_TYPE_RW101\x10\t\x12\x14\n\x10MODEM_TYPE_RW135\x10\n\x12\x15\n\x11MODEM_TYPE_LCUK54\x10\x0b*\xc1\x03\n\x0fNetworkProvider\x12\x11\n\rNETWORK_OTHER\x10\x00\x12\x17\n\x13NETWORK_UNSUPPORTED\x10\x05\x12\x10\n\x0cNETWORK_TEST\x10\x01\x12\x0f\n\x0bNETWORK_ATT\x10\x02\x12\x13\n\x0fNETWORK_TMOBILE\x10\x03\x12\x13\n\x0fNETWORK_VERIZON\x10\x04\x12\x12\n\x0eNETWORK_SPRINT\x10\x06\x12\x12\n\x0eNETWORK_DOCOMO\x10\x07\x12\x14\n\x10NETWORK_SOFTBANK\x10\x08\x12\x10\n\x0cNETWORK_KDDI\x10\t\x12\x13\n\x0fNETWORK_RAKUTEN\x10\n\x12\x14\n\x10NETWORK_VODAFONE\x10\x0b\x12\x0e\n\nNETWORK_EE\x10\x0c\x12\x15\n\x11NETWORK_AMARISOFT\x10\r\x12\x11\n\rNETWORK_ROGER\x10\x0e\x12\x10\n\x0cNETWORK_BELL\x10\x0f\x12\x11\n\rNETWORK_TELUS\x10\x10\x12\x0e\n\nNETWORK_FI\x10\x11\x12\x10\n\x0cNETWORK_CBRS\x10\x12\x12\x12\n\x0eNETWORK_LINEMO\x10\x13\x12\x10\n\x0cNETWORK_POVO\x10\x14\x12\x13\n\x0fNETWORK_HANSHIN\x10\x15*=\n\x07SIMType\x12\x0f\n\x0bSIM_UNKNOWN\x10\x00\x12\x10\n\x0cSIM_PHYSICAL\x10\x01\x12\x0f\n\x0bSIM_DIGITAL\x10\x02*I\n\x07RPMType\x12\x14\n\x10RPM_TYPE_UNKNOWN\x10\x00\x12\x13\n\x0fRPM_TYPE_SENTRY\x10\x01\x12\x13\n\x0fRPM_TYPE_IP9850\x10\x02*`\n\x0fPeripheralState\x12 \n\x1cPERIPHERAL_STATE_UNSPECIFIED\x10\x00\x12\x0b\n\x07WORKING\x10\x01\x12\n\n\x06\x42ROKEN\x10\x02\x12\x12\n\x0eNOT_APPLICABLE\x10\x03*\xfb\x03\n\x05Phase\x12\x15\n\x11PHASE_UNSPECIFIED\x10\x00\x12\x07\n\x03\x44VT\x10\x01\x12\t\n\x05\x44VT_2\x10\x02\x12\x11\n\rDVT_2_MPS_LTE\x10\x03\x12\x0f\n\x0b\x44VT_BIPSHIP\x10\x04\x12\x0e\n\nDVT_BOOKEM\x10\x05\x12\x0f\n\x0b\x44VT_ELECTRO\x10\x06\x12\r\n\tDVT_LOCKE\x10\x07\x12\x0e\n\nDVT_OSCINO\x10\x08\x12\x0e\n\nDVT_REKS14\x10\t\x12\x14\n\x10\x44VT_REKS14_TOUCH\x10\n\x12\r\n\tDVT_TOUCH\x10\x0b\x12\x07\n\x03\x45VT\x10\x0c\x12\x11\n\rEVT_FLEEX_LTE\x10\r\x12\n\n\x06\x45VT_HQ\x10\x0e\x12\x0b\n\x07\x45VT_LTE\x10\x0f\x12\r\n\tEVT_MAPLE\x10\x10\x12\r\n\tEVT_PUJJO\x10\x11\x12\t\n\x05PROTO\x10\x12\x12\n\n\x06PROTO1\x10\x13\x12\x07\n\x03PVT\x10\x14\x12\x0e\n\nPVT_TERRA3\x10\x15\x12\n\n\x06PVT_US\x10\x16\x12\t\n\x05PVT_2\x10\x17\x12\x0e\n\nPVT_BOOKEM\x10\x18\x12\x0f\n\x0bPVT_ELECTRO\x10\x19\x12\x0e\n\nPVT_GIK360\x10\x1a\x12\x0c\n\x08PVT_LILI\x10\x1b\x12\x0b\n\x07PVT_LTE\x10\x1c\x12\x0f\n\x0bPVT_NEW_CPU\x10\x1d\x12\x0c\n\x08PVT_SAND\x10\x1e\x12\x11\n\rPVT_TUNE_BITS\x10\x1f\x12\x0e\n\nPVT_TELESU\x10 \x12\x06\n\x02SR\x10!B3Z1go.chromium.org/chromiumos/config/go/test/lab/apib\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chromiumos.test.lab.api.dut_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z1go.chromium.org/chromiumos/config/go/test/lab/api'
  _MODEMTYPE._serialized_start=5096
  _MODEMTYPE._serialized_end=5414
  _NETWORKPROVIDER._serialized_start=5417
  _NETWORKPROVIDER._serialized_end=5866
  _SIMTYPE._serialized_start=5868
  _SIMTYPE._serialized_end=5929
  _RPMTYPE._serialized_start=5931
  _RPMTYPE._serialized_end=6004
  _PERIPHERALSTATE._serialized_start=6006
  _PERIPHERALSTATE._serialized_end=6102
  _PHASE._serialized_start=6105
  _PHASE._serialized_end=6612
  _DUT._serialized_start=194
  _DUT._serialized_end=1982
  _DUT_ID._serialized_start=539
  _DUT_ID._serialized_end=558
  _DUT_CHROMEOS._serialized_start=561
  _DUT_CHROMEOS._serialized_end=1595
  _DUT_ANDROID._serialized_start=1598
  _DUT_ANDROID._serialized_end=1764
  _DUT_DEVBOARD._serialized_start=1767
  _DUT_DEVBOARD._serialized_end=1970
  _DUTMODEL._serialized_start=1984
  _DUTMODEL._serialized_end=2036
  _DUTTOPOLOGY._serialized_start=2039
  _DUTTOPOLOGY._serialized_end=2182
  _DUTTOPOLOGY_ID._serialized_start=539
  _DUTTOPOLOGY_ID._serialized_end=558
  _AUDIO._serialized_start=2184
  _AUDIO._serialized_end=2225
  _CABLE._serialized_start=2228
  _CABLE._serialized_end=2377
  _CABLE_TYPE._serialized_start=2288
  _CABLE_TYPE._serialized_end=2377
  _CACHESERVER._serialized_start=2379
  _CACHESERVER._serialized_end=2446
  _CAMERABOX._serialized_start=2448
  _CAMERABOX._serialized_end=2573
  _CAMERABOX_FACING._serialized_start=2520
  _CAMERABOX_FACING._serialized_end=2573
  _CELLULAR._serialized_start=2576
  _CELLULAR._serialized_end=2739
  _CELLULAR_OPERATOR._serialized_start=2668
  _CELLULAR_OPERATOR._serialized_end=2739
  _MODEMINFO._serialized_start=2742
  _MODEMINFO._serialized_end=2884
  _SIMINFO._serialized_start=2887
  _SIMINFO._serialized_end=3056
  _SIMPROFILEINFO._serialized_start=3059
  _SIMPROFILEINFO._serialized_end=3513
  _SIMPROFILEINFO_STATE._serialized_start=3339
  _SIMPROFILEINFO_STATE._serialized_end=3434
  _SIMPROFILEINFO_FEATURE._serialized_start=3436
  _SIMPROFILEINFO_FEATURE._serialized_end=3513
  _CHAMELEON._serialized_start=3516
  _CHAMELEON._serialized_end=3944
  _CHAMELEON_PERIPHERAL._serialized_start=3750
  _CHAMELEON_PERIPHERAL._serialized_end=3898
  _CHAMELEON_TYPE._serialized_start=3900
  _CHAMELEON_TYPE._serialized_end=3944
  _EXTERNALCAMERA._serialized_start=3947
  _EXTERNALCAMERA._serialized_end=4078
  _EXTERNALCAMERA_TYPE._serialized_start=4025
  _EXTERNALCAMERA_TYPE._serialized_end=4078
  _RPM._serialized_start=4081
  _RPM._serialized_end=4368
  _SERVO._serialized_start=4371
  _SERVO._serialized_end=4529
  _TOUCH._serialized_start=4531
  _TOUCH._serialized_end=4552
  _WIFI._serialized_start=4555
  _WIFI._serialized_end=4785
  _WIFI_ENVIRONMENT._serialized_start=4682
  _WIFI_ENVIRONMENT._serialized_end=4785
  _WIFIANTENNA._serialized_start=4788
  _WIFIANTENNA._serialized_end=4937
  _WIFIANTENNA_CONNECTION._serialized_start=4872
  _WIFIANTENNA_CONNECTION._serialized_end=4937
  _BLUETOOTHPEER._serialized_start=4939
  _BLUETOOTHPEER._serialized_end=5029
  _WIFISECRET._serialized_start=5031
  _WIFISECRET._serialized_end=5093
# @@protoc_insertion_point(module_scope)
