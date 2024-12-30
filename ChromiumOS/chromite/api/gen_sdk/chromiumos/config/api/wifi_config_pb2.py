# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/config/api/wifi_config.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'chromiumos/config/api/wifi_config.proto\x12\x15\x63hromiumos.config.api\"\xc9<\n\nWifiConfig\x12G\n\rath10k_config\x18\x01 \x01(\x0b\x32..chromiumos.config.api.WifiConfig.Ath10kConfigH\x00\x12\x45\n\x0crtw88_config\x18\x02 \x01(\x0b\x32-.chromiumos.config.api.WifiConfig.Rtw88ConfigH\x00\x12\x45\n\x0cintel_config\x18\x03 \x01(\x0b\x32-.chromiumos.config.api.WifiConfig.IntelConfigH\x00\x12\x41\n\nmtk_config\x18\x04 \x01(\x0b\x32+.chromiumos.config.api.WifiConfig.MtkConfigH\x00\x12\x45\n\x0crtw89_config\x18\x05 \x01(\x0b\x32-.chromiumos.config.api.WifiConfig.Rtw89ConfigH\x00\x12R\n\x13legacy_intel_config\x18\x06 \x01(\x0b\x32\x33.chromiumos.config.api.WifiConfig.LegacyIntelConfigH\x00\x1a\x94\x02\n\x0c\x41th10kConfig\x12\x62\n\x17tablet_mode_power_table\x18\x01 \x01(\x0b\x32\x41.chromiumos.config.api.WifiConfig.Ath10kConfig.TransmitPowerChain\x12\x66\n\x1bnon_tablet_mode_power_table\x18\x02 \x01(\x0b\x32\x41.chromiumos.config.api.WifiConfig.Ath10kConfig.TransmitPowerChain\x1a\x38\n\x12TransmitPowerChain\x12\x10\n\x08limit_2g\x18\x01 \x01(\r\x12\x10\n\x08limit_5g\x18\x02 \x01(\r\x1a\xda\x04\n\x0bRtw88Config\x12\x61\n\x17tablet_mode_power_table\x18\x01 \x01(\x0b\x32@.chromiumos.config.api.WifiConfig.Rtw88Config.TransmitPowerChain\x12\x65\n\x1bnon_tablet_mode_power_table\x18\x02 \x01(\x0b\x32@.chromiumos.config.api.WifiConfig.Rtw88Config.TransmitPowerChain\x12L\n\noffset_fcc\x18\x03 \x01(\x0b\x32\x38.chromiumos.config.api.WifiConfig.Rtw88Config.GeoOffsets\x12K\n\toffset_eu\x18\x04 \x01(\x0b\x32\x38.chromiumos.config.api.WifiConfig.Rtw88Config.GeoOffsets\x12N\n\x0coffset_other\x18\x05 \x01(\x0b\x32\x38.chromiumos.config.api.WifiConfig.Rtw88Config.GeoOffsets\x1a\x62\n\x12TransmitPowerChain\x12\x10\n\x08limit_2g\x18\x01 \x01(\r\x12\x12\n\nlimit_5g_1\x18\x02 \x01(\r\x12\x12\n\nlimit_5g_3\x18\x03 \x01(\r\x12\x12\n\nlimit_5g_4\x18\x04 \x01(\r\x1a\x32\n\nGeoOffsets\x12\x11\n\toffset_2g\x18\x01 \x01(\r\x12\x11\n\toffset_5g\x18\x02 \x01(\r\x1a\xda#\n\x0bIntelConfig\x12I\n\tsar_table\x18\x01 \x01(\x0b\x32\x36.chromiumos.config.api.WifiConfig.IntelConfig.SarTable\x12I\n\nwgds_table\x18\x02 \x01(\x0b\x32\x35.chromiumos.config.api.WifiConfig.IntelConfig.Offsets\x12\x46\n\tant_table\x18\x03 \x01(\x0b\x32\x33.chromiumos.config.api.WifiConfig.IntelConfig.Gains\x12I\n\nwtas_table\x18\x04 \x01(\x0b\x32\x35.chromiumos.config.api.WifiConfig.IntelConfig.Average\x12>\n\x03\x64sm\x18\x05 \x01(\x0b\x32\x31.chromiumos.config.api.WifiConfig.IntelConfig.DSM\x12J\n\x06\x62t_sar\x18\x06 \x01(\x0b\x32:.chromiumos.config.api.WifiConfig.IntelConfig.BluetoothSAR\x12@\n\x04wbem\x18\x07 \x01(\x0b\x32\x32.chromiumos.config.api.WifiConfig.IntelConfig.WBEM\x1a\xa6\t\n\x08SarTable\x12\x19\n\x11sar_table_version\x18\x01 \x01(\r\x12l\n\x19tablet_mode_power_table_a\x18\x03 \x01(\x0b\x32I.chromiumos.config.api.WifiConfig.IntelConfig.SarTable.TransmitPowerChain\x12l\n\x19tablet_mode_power_table_b\x18\x04 \x01(\x0b\x32I.chromiumos.config.api.WifiConfig.IntelConfig.SarTable.TransmitPowerChain\x12p\n\x1dnon_tablet_mode_power_table_a\x18\x05 \x01(\x0b\x32I.chromiumos.config.api.WifiConfig.IntelConfig.SarTable.TransmitPowerChain\x12p\n\x1dnon_tablet_mode_power_table_b\x18\x06 \x01(\x0b\x32I.chromiumos.config.api.WifiConfig.IntelConfig.SarTable.TransmitPowerChain\x12p\n\x1d\x63\x64\x62_tablet_mode_power_table_a\x18\x07 \x01(\x0b\x32I.chromiumos.config.api.WifiConfig.IntelConfig.SarTable.TransmitPowerChain\x12p\n\x1d\x63\x64\x62_tablet_mode_power_table_b\x18\x08 \x01(\x0b\x32I.chromiumos.config.api.WifiConfig.IntelConfig.SarTable.TransmitPowerChain\x12t\n!cdb_non_tablet_mode_power_table_a\x18\t \x01(\x0b\x32I.chromiumos.config.api.WifiConfig.IntelConfig.SarTable.TransmitPowerChain\x12t\n!cdb_non_tablet_mode_power_table_b\x18\n \x01(\x0b\x32I.chromiumos.config.api.WifiConfig.IntelConfig.SarTable.TransmitPowerChain\x1a\xee\x01\n\x12TransmitPowerChain\x12\x10\n\x08limit_2g\x18\x01 \x01(\r\x12\x12\n\nlimit_5g_1\x18\x02 \x01(\r\x12\x12\n\nlimit_5g_2\x18\x03 \x01(\r\x12\x12\n\nlimit_5g_3\x18\x04 \x01(\r\x12\x12\n\nlimit_5g_4\x18\x05 \x01(\r\x12\x12\n\nlimit_5g_5\x18\x06 \x01(\r\x12\x12\n\nlimit_6g_1\x18\x07 \x01(\r\x12\x12\n\nlimit_6g_2\x18\x08 \x01(\r\x12\x12\n\nlimit_6g_3\x18\t \x01(\r\x12\x12\n\nlimit_6g_4\x18\n \x01(\r\x12\x12\n\nlimit_6g_5\x18\x0b \x01(\r\x1a\xdf\x03\n\x07Offsets\x12\x14\n\x0cwgds_version\x18\x01 \x01(\r\x12T\n\noffset_fcc\x18\x02 \x01(\x0b\x32@.chromiumos.config.api.WifiConfig.IntelConfig.Offsets.GeoOffsets\x12S\n\toffset_eu\x18\x03 \x01(\x0b\x32@.chromiumos.config.api.WifiConfig.IntelConfig.Offsets.GeoOffsets\x12V\n\x0coffset_other\x18\x04 \x01(\x0b\x32@.chromiumos.config.api.WifiConfig.IntelConfig.Offsets.GeoOffsets\x1a\xba\x01\n\nGeoOffsets\x12\x0e\n\x06max_2g\x18\x01 \x01(\r\x12\x13\n\x0boffset_2g_a\x18\x02 \x01(\r\x12\x13\n\x0boffset_2g_b\x18\x03 \x01(\r\x12\x0e\n\x06max_5g\x18\x04 \x01(\r\x12\x13\n\x0boffset_5g_a\x18\x05 \x01(\r\x12\x13\n\x0boffset_5g_b\x18\x06 \x01(\r\x12\x0e\n\x06max_6g\x18\x07 \x01(\r\x12\x13\n\x0boffset_6g_a\x18\x08 \x01(\r\x12\x13\n\x0boffset_6g_b\x18\t \x01(\r\x1a\xfa\x03\n\x05Gains\x12\x19\n\x11\x61nt_table_version\x18\x01 \x01(\r\x12\x15\n\rant_mode_ppag\x18\x02 \x01(\r\x12Y\n\x10\x61nt_gain_table_a\x18\x03 \x01(\x0b\x32?.chromiumos.config.api.WifiConfig.IntelConfig.Gains.AntennaGain\x12Y\n\x10\x61nt_gain_table_b\x18\x04 \x01(\x0b\x32?.chromiumos.config.api.WifiConfig.IntelConfig.Gains.AntennaGain\x1a\x88\x02\n\x0b\x41ntennaGain\x12\x13\n\x0b\x61nt_gain_2g\x18\x01 \x01(\r\x12\x15\n\rant_gain_5g_1\x18\x02 \x01(\r\x12\x15\n\rant_gain_5g_2\x18\x03 \x01(\r\x12\x15\n\rant_gain_5g_3\x18\x04 \x01(\r\x12\x15\n\rant_gain_5g_4\x18\x05 \x01(\r\x12\x15\n\rant_gain_5g_5\x18\x06 \x01(\r\x12\x15\n\rant_gain_6g_1\x18\x07 \x01(\r\x12\x15\n\rant_gain_6g_2\x18\x08 \x01(\r\x12\x15\n\rant_gain_6g_3\x18\t \x01(\r\x12\x15\n\rant_gain_6g_4\x18\n \x01(\r\x12\x15\n\rant_gain_6g_5\x18\x0b \x01(\r\x1a\x87\x04\n\x07\x41verage\x12\x17\n\x0fsar_avg_version\x18\x01 \x01(\r\x12\x15\n\rtas_selection\x18\x02 \x01(\r\x12\x15\n\rtas_list_size\x18\x03 \x01(\r\x12\x19\n\x11\x64\x65ny_list_entry_1\x18\x04 \x01(\r\x12\x19\n\x11\x64\x65ny_list_entry_2\x18\x05 \x01(\r\x12\x19\n\x11\x64\x65ny_list_entry_3\x18\x06 \x01(\r\x12\x19\n\x11\x64\x65ny_list_entry_4\x18\x07 \x01(\r\x12\x19\n\x11\x64\x65ny_list_entry_5\x18\x08 \x01(\r\x12\x19\n\x11\x64\x65ny_list_entry_6\x18\t \x01(\r\x12\x19\n\x11\x64\x65ny_list_entry_7\x18\n \x01(\r\x12\x19\n\x11\x64\x65ny_list_entry_8\x18\x0b \x01(\r\x12\x19\n\x11\x64\x65ny_list_entry_9\x18\x0c \x01(\r\x12\x1a\n\x12\x64\x65ny_list_entry_10\x18\r \x01(\r\x12\x1a\n\x12\x64\x65ny_list_entry_11\x18\x0e \x01(\r\x12\x1a\n\x12\x64\x65ny_list_entry_12\x18\x0f \x01(\r\x12\x1a\n\x12\x64\x65ny_list_entry_13\x18\x10 \x01(\r\x12\x1a\n\x12\x64\x65ny_list_entry_14\x18\x11 \x01(\r\x12\x1a\n\x12\x64\x65ny_list_entry_15\x18\x12 \x01(\r\x12\x1a\n\x12\x64\x65ny_list_entry_16\x18\x13 \x01(\r\x1a\xf4\x06\n\x03\x44SM\x12#\n\x1b\x64isable_active_sdr_channels\x18\x02 \x01(\x03\x12!\n\x19support_indonesia_5g_band\x18\x03 \x01(\x03\x12\x1f\n\x17support_ultra_high_band\x18\x04 \x01(\x03\x12!\n\x19regulatory_configurations\x18\x05 \x01(\x03\x12\x1b\n\x13uart_configurations\x18\x06 \x01(\x03\x12\x17\n\x0f\x65nablement_11ax\x18\x07 \x01(\x03\x12\x0e\n\x06unii_4\x18\x08 \x01(\x03\x12l\n\x19\x65nablement_11be_countries\x18\t \x01(\x0b\x32I.chromiumos.config.api.WifiConfig.IntelConfig.DSM.Enablement11beCountries\x12n\n\x1a\x65nergy_detection_threshold\x18\n \x01(\x0b\x32J.chromiumos.config.api.WifiConfig.IntelConfig.DSM.EnergyDetectionThreshold\x12W\n\x0erfi_mitigation\x18\x0b \x01(\x0b\x32?.chromiumos.config.api.WifiConfig.IntelConfig.DSM.RFIMitigation\x1a=\n\x17\x45nablement11beCountries\x12\r\n\x05\x63hina\x18\x01 \x01(\x08\x12\x13\n\x0bsouth_korea\x18\x02 \x01(\x08\x1a\xf8\x01\n\x18\x45nergyDetectionThreshold\x12\x10\n\x08revision\x18\x01 \x01(\r\x12\x0f\n\x07\x65tsi_hb\x18\x02 \x01(\x08\x12\x0f\n\x07\x66\x63\x63_uhb\x18\x03 \x01(\x08\x12\x10\n\x08hb_5g2_3\x18\x04 \x01(\x08\x12\x0e\n\x06hb_5g4\x18\x05 \x01(\x08\x12\x0e\n\x06hb_5g6\x18\x06 \x01(\x08\x12\x10\n\x08hb_5g8_9\x18\x07 \x01(\x08\x12\x0f\n\x07uhb_6g1\x18\x08 \x01(\x08\x12\x0f\n\x07uhb_6g3\x18\t \x01(\x08\x12\x0f\n\x07uhb_6g5\x18\n \x01(\x08\x12\x0f\n\x07uhb_6g6\x18\x0b \x01(\x08\x12\x0f\n\x07uhb_6g8\x18\x0c \x01(\x08\x12\x0f\n\x07uhb_7g0\x18\r \x01(\x08\x1a*\n\rRFIMitigation\x12\x0c\n\x04\x64lvr\x18\x01 \x01(\x08\x12\x0b\n\x03\x64\x64r\x18\x02 \x01(\x08\x1a\x81\x02\n\x0c\x42luetoothSAR\x12\x10\n\x08revision\x18\x01 \x01(\r\x12\'\n\x1fincreased_power_mode_limitation\x18\x02 \x01(\r\x12 \n\x18sar_lb_power_restriction\x18\x03 \x01(\r\x12\x15\n\rbr_modulation\x18\x04 \x01(\r\x12\x17\n\x0f\x65\x64r2_modulation\x18\x05 \x01(\r\x12\x17\n\x0f\x65\x64r3_modulation\x18\x06 \x01(\r\x12\x15\n\rle_modulation\x18\x07 \x01(\r\x12\x1a\n\x12le2_mhz_modulation\x18\x08 \x01(\r\x12\x18\n\x10le_lr_modulation\x18\t \x01(\r\x1a\xc6\x01\n\x04WBEM\x12\x10\n\x08revision\x18\x01 \x01(\r\x12m\n\x19\x65nablement_wbem_countries\x18\x02 \x01(\x0b\x32J.chromiumos.config.api.WifiConfig.IntelConfig.WBEM.EnablementWbemCountries\x1a=\n\x17\x45nablementWbemCountries\x12\r\n\x05japan\x18\x01 \x01(\x08\x12\x13\n\x0bsouth_korea\x18\x02 \x01(\x08\x1a\x13\n\x11LegacyIntelConfig\x1a\xa7\x08\n\tMtkConfig\x12_\n\x17tablet_mode_power_table\x18\x01 \x01(\x0b\x32>.chromiumos.config.api.WifiConfig.MtkConfig.TransmitPowerChain\x12\x63\n\x1bnon_tablet_mode_power_table\x18\x02 \x01(\x0b\x32>.chromiumos.config.api.WifiConfig.MtkConfig.TransmitPowerChain\x12Z\n\x0f\x66\x63\x63_power_table\x18\x03 \x01(\x0b\x32\x41.chromiumos.config.api.WifiConfig.MtkConfig.GeoTransmitPowerChain\x12Y\n\x0e\x65u_power_table\x18\x04 \x01(\x0b\x32\x41.chromiumos.config.api.WifiConfig.MtkConfig.GeoTransmitPowerChain\x12\\\n\x11other_power_table\x18\x05 \x01(\x0b\x32\x41.chromiumos.config.api.WifiConfig.MtkConfig.GeoTransmitPowerChain\x12K\n\x0c\x63ountry_list\x18\x06 \x01(\x0b\x32\x35.chromiumos.config.api.WifiConfig.MtkConfig.MtclTable\x1a\xee\x01\n\x12TransmitPowerChain\x12\x10\n\x08limit_2g\x18\x01 \x01(\r\x12\x12\n\nlimit_5g_1\x18\x02 \x01(\r\x12\x12\n\nlimit_5g_2\x18\x03 \x01(\r\x12\x12\n\nlimit_5g_3\x18\x04 \x01(\r\x12\x12\n\nlimit_5g_4\x18\x05 \x01(\r\x12\x12\n\nlimit_6g_1\x18\x06 \x01(\r\x12\x12\n\nlimit_6g_2\x18\x07 \x01(\r\x12\x12\n\nlimit_6g_3\x18\x08 \x01(\r\x12\x12\n\nlimit_6g_4\x18\t \x01(\r\x12\x12\n\nlimit_6g_5\x18\n \x01(\r\x12\x12\n\nlimit_6g_6\x18\x0b \x01(\r\x1a\x86\x01\n\x15GeoTransmitPowerChain\x12\x10\n\x08limit_2g\x18\x01 \x01(\r\x12\x10\n\x08limit_5g\x18\x02 \x01(\r\x12\x11\n\toffset_2g\x18\x03 \x01(\r\x12\x11\n\toffset_5g\x18\x04 \x01(\r\x12\x10\n\x08limit_6g\x18\x05 \x01(\r\x12\x11\n\toffset_6g\x18\x06 \x01(\r\x1ax\n\tMtclTable\x12\x0f\n\x07version\x18\x01 \x01(\r\x12\x14\n\x0csupport_6ghz\x18\x02 \x01(\r\x12\x14\n\x0c\x62itmask_6ghz\x18\x03 \x01(\x04\x12\x16\n\x0esupport_5p9ghz\x18\x04 \x01(\r\x12\x16\n\x0e\x62itmask_5p9ghz\x18\x05 \x01(\x04\x1a\xe6\x05\n\x0bRtw89Config\x12\x61\n\x17tablet_mode_power_table\x18\x01 \x01(\x0b\x32@.chromiumos.config.api.WifiConfig.Rtw89Config.TransmitPowerChain\x12\x65\n\x1bnon_tablet_mode_power_table\x18\x02 \x01(\x0b\x32@.chromiumos.config.api.WifiConfig.Rtw89Config.TransmitPowerChain\x12L\n\noffset_fcc\x18\x03 \x01(\x0b\x32\x38.chromiumos.config.api.WifiConfig.Rtw89Config.GeoOffsets\x12K\n\toffset_eu\x18\x04 \x01(\x0b\x32\x38.chromiumos.config.api.WifiConfig.Rtw89Config.GeoOffsets\x12N\n\x0coffset_other\x18\x05 \x01(\x0b\x32\x38.chromiumos.config.api.WifiConfig.Rtw89Config.GeoOffsets\x1a\xda\x01\n\x12TransmitPowerChain\x12\x10\n\x08limit_2g\x18\x01 \x01(\r\x12\x12\n\nlimit_5g_1\x18\x02 \x01(\r\x12\x12\n\nlimit_5g_3\x18\x03 \x01(\r\x12\x12\n\nlimit_5g_4\x18\x04 \x01(\r\x12\x12\n\nlimit_6g_1\x18\x05 \x01(\r\x12\x12\n\nlimit_6g_2\x18\x06 \x01(\r\x12\x12\n\nlimit_6g_3\x18\x07 \x01(\r\x12\x12\n\nlimit_6g_4\x18\x08 \x01(\r\x12\x12\n\nlimit_6g_5\x18\t \x01(\r\x12\x12\n\nlimit_6g_6\x18\n \x01(\r\x1a\x45\n\nGeoOffsets\x12\x11\n\toffset_2g\x18\x01 \x01(\r\x12\x11\n\toffset_5g\x18\x02 \x01(\r\x12\x11\n\toffset_6g\x18\x03 \x01(\rB\r\n\x0bwifi_configB*Z(go.chromium.org/chromiumos/config/go/apib\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chromiumos.config.api.wifi_config_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z(go.chromium.org/chromiumos/config/go/api'
  _globals['_WIFICONFIG']._serialized_start=67
  _globals['_WIFICONFIG']._serialized_end=7820
  _globals['_WIFICONFIG_ATH10KCONFIG']._serialized_start=519
  _globals['_WIFICONFIG_ATH10KCONFIG']._serialized_end=795
  _globals['_WIFICONFIG_ATH10KCONFIG_TRANSMITPOWERCHAIN']._serialized_start=739
  _globals['_WIFICONFIG_ATH10KCONFIG_TRANSMITPOWERCHAIN']._serialized_end=795
  _globals['_WIFICONFIG_RTW88CONFIG']._serialized_start=798
  _globals['_WIFICONFIG_RTW88CONFIG']._serialized_end=1400
  _globals['_WIFICONFIG_RTW88CONFIG_TRANSMITPOWERCHAIN']._serialized_start=1250
  _globals['_WIFICONFIG_RTW88CONFIG_TRANSMITPOWERCHAIN']._serialized_end=1348
  _globals['_WIFICONFIG_RTW88CONFIG_GEOOFFSETS']._serialized_start=1350
  _globals['_WIFICONFIG_RTW88CONFIG_GEOOFFSETS']._serialized_end=1400
  _globals['_WIFICONFIG_INTELCONFIG']._serialized_start=1403
  _globals['_WIFICONFIG_INTELCONFIG']._serialized_end=5973
  _globals['_WIFICONFIG_INTELCONFIG_SARTABLE']._serialized_start=1922
  _globals['_WIFICONFIG_INTELCONFIG_SARTABLE']._serialized_end=3112
  _globals['_WIFICONFIG_INTELCONFIG_SARTABLE_TRANSMITPOWERCHAIN']._serialized_start=2874
  _globals['_WIFICONFIG_INTELCONFIG_SARTABLE_TRANSMITPOWERCHAIN']._serialized_end=3112
  _globals['_WIFICONFIG_INTELCONFIG_OFFSETS']._serialized_start=3115
  _globals['_WIFICONFIG_INTELCONFIG_OFFSETS']._serialized_end=3594
  _globals['_WIFICONFIG_INTELCONFIG_OFFSETS_GEOOFFSETS']._serialized_start=3408
  _globals['_WIFICONFIG_INTELCONFIG_OFFSETS_GEOOFFSETS']._serialized_end=3594
  _globals['_WIFICONFIG_INTELCONFIG_GAINS']._serialized_start=3597
  _globals['_WIFICONFIG_INTELCONFIG_GAINS']._serialized_end=4103
  _globals['_WIFICONFIG_INTELCONFIG_GAINS_ANTENNAGAIN']._serialized_start=3839
  _globals['_WIFICONFIG_INTELCONFIG_GAINS_ANTENNAGAIN']._serialized_end=4103
  _globals['_WIFICONFIG_INTELCONFIG_AVERAGE']._serialized_start=4106
  _globals['_WIFICONFIG_INTELCONFIG_AVERAGE']._serialized_end=4625
  _globals['_WIFICONFIG_INTELCONFIG_DSM']._serialized_start=4628
  _globals['_WIFICONFIG_INTELCONFIG_DSM']._serialized_end=5512
  _globals['_WIFICONFIG_INTELCONFIG_DSM_ENABLEMENT11BECOUNTRIES']._serialized_start=5156
  _globals['_WIFICONFIG_INTELCONFIG_DSM_ENABLEMENT11BECOUNTRIES']._serialized_end=5217
  _globals['_WIFICONFIG_INTELCONFIG_DSM_ENERGYDETECTIONTHRESHOLD']._serialized_start=5220
  _globals['_WIFICONFIG_INTELCONFIG_DSM_ENERGYDETECTIONTHRESHOLD']._serialized_end=5468
  _globals['_WIFICONFIG_INTELCONFIG_DSM_RFIMITIGATION']._serialized_start=5470
  _globals['_WIFICONFIG_INTELCONFIG_DSM_RFIMITIGATION']._serialized_end=5512
  _globals['_WIFICONFIG_INTELCONFIG_BLUETOOTHSAR']._serialized_start=5515
  _globals['_WIFICONFIG_INTELCONFIG_BLUETOOTHSAR']._serialized_end=5772
  _globals['_WIFICONFIG_INTELCONFIG_WBEM']._serialized_start=5775
  _globals['_WIFICONFIG_INTELCONFIG_WBEM']._serialized_end=5973
  _globals['_WIFICONFIG_INTELCONFIG_WBEM_ENABLEMENTWBEMCOUNTRIES']._serialized_start=5912
  _globals['_WIFICONFIG_INTELCONFIG_WBEM_ENABLEMENTWBEMCOUNTRIES']._serialized_end=5973
  _globals['_WIFICONFIG_LEGACYINTELCONFIG']._serialized_start=5975
  _globals['_WIFICONFIG_LEGACYINTELCONFIG']._serialized_end=5994
  _globals['_WIFICONFIG_MTKCONFIG']._serialized_start=5997
  _globals['_WIFICONFIG_MTKCONFIG']._serialized_end=7060
  _globals['_WIFICONFIG_MTKCONFIG_TRANSMITPOWERCHAIN']._serialized_start=6563
  _globals['_WIFICONFIG_MTKCONFIG_TRANSMITPOWERCHAIN']._serialized_end=6801
  _globals['_WIFICONFIG_MTKCONFIG_GEOTRANSMITPOWERCHAIN']._serialized_start=6804
  _globals['_WIFICONFIG_MTKCONFIG_GEOTRANSMITPOWERCHAIN']._serialized_end=6938
  _globals['_WIFICONFIG_MTKCONFIG_MTCLTABLE']._serialized_start=6940
  _globals['_WIFICONFIG_MTKCONFIG_MTCLTABLE']._serialized_end=7060
  _globals['_WIFICONFIG_RTW89CONFIG']._serialized_start=7063
  _globals['_WIFICONFIG_RTW89CONFIG']._serialized_end=7805
  _globals['_WIFICONFIG_RTW89CONFIG_TRANSMITPOWERCHAIN']._serialized_start=7516
  _globals['_WIFICONFIG_RTW89CONFIG_TRANSMITPOWERCHAIN']._serialized_end=7734
  _globals['_WIFICONFIG_RTW89CONFIG_GEOOFFSETS']._serialized_start=7736
  _globals['_WIFICONFIG_RTW89CONFIG_GEOOFFSETS']._serialized_end=7805
# @@protoc_insertion_point(module_scope)
