# High Level Analyzer
# For more information and documentation, please go to https://support.saleae.com/extensions/high-level-analyzer-extensions

from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting, NumberSetting, ChoicesSetting

import struct

DATA_COMMANDS = {

}

CHARGER_I2C_ADDRESS = 0x6B

REGISTERS = {
  0x00 : "Charger Status 0",
  0x01 : "Charger Status 1",
  0x02 : "ADC Status",
  0x03 : "Charger Flags 0",
  0x04 : "Charger Flags 1",
  0x05 : "ADC Flags",
  0x06 : "Timer Flags",
  0x07 : "Interrupt Mask 0",
  0x08 : "Interrupt Mask 1",
  0x09 : "Interrupt Mast 2",
  0x0a : "Interrupt Mask 3",
  0x12 : "Battery Voltage Control",
  0x13 : "Fast Charge Current Control",
  0x14 : "Pre-Charge Current Control",
  0x15 : "Termination Current Control",
  0x16 : "Battery UVLO and Current Limit Control",
  0x17 : "Charger Control 0",
  0x18 : "Charger Control 1",
  0x19 : "Input Current Limit Control",
  0x1d : "LDO Control",
  0x30 : "MR Control",
  0x35 : "IC Control 0",
  0x36 : "IC Control 1",
  0x37 : "IC Control 2",
  0x40 : "ADC Control 0",
  0x41 : "ADC Control 1",
  0x42 : "VBatt MSB",
  0x43 : "VBatt LSB",
  0x44 : "TS MSB",
  0x45 : "TS LSB",
  0x46 : "Fast Charge Current MSB",
  0x47 : "Fast Charge Current LSB",
  0x48 : "ADC In MSB",
  0x49 : "ADC In LSB",
  0x4a : "Vin MSB",
  0x4b : "Vin LSB",
  0x4c : "VpMid MSB",
  0x4d : "VpMid LSB",
  0x4e : "Iin MSB",
  0x4f : "Iin LSB",
  0x52 : "Comparator 1 Threshold MSB",
  0x53 : "Comparator 1 Threshold LSB",
  0x54 : "Comparator 2 Threshold MSB",
  0x55 : "Comparator 2 Threshold LSB",
  0x56 : "Comparator 3 Threshold MSB",
  0x57 : "Comparator 3 Threshold LSB",
  0x58 : "ADC Channel Enable",
  0x61 : "Fast Charge Control",
  0x62 : "Cold Threshold",
  0x63 : "Cool Threshold",
  0x64 : "Warm Threshold",
  0x65 : "Hot Threshold",
  0x6f : "Device ID"
}

# High level analyzers must subclass the HighLevelAnalyzer class.
class LinearBatteryCharger(HighLevelAnalyzer):
    # List of settings that a user can set for this High Level Analyzer.
    # my_string_setting = StringSetting()
    # my_number_setting = NumberSetting(min_value=0, max_value=100)
    # my_choices_setting = ChoicesSetting(choices=('A', 'B'))

    # An optional list of types this analyzer produces, providing a way to customize the way frames are displayed in Logic 2.
    result_types = {
        'error': {
            'format': 'Error!'
        },
        'generic_data': {
          'format' : '{{data.address}} [ {{data.data}} ]'
        },
        'generic_read': {
          'format' : 'Read [ {{data.data}} ] from the {{data.address}} register'
        },
        'generic_write': {
          'format' : 'Wrote [ {{data.data}} ] to the {{data.data}} register'
        },
        'register': {
          'format' : 'Using the {{data.data}} register'
        }
    }

    temp_frame = None

    def __init__(self):
        '''
        Initialize HLA.
        Settings can be accessed using the same name used above.
        '''
        self._continue_analysis = False
        self._is_reg_next = True

    def decode(self, frame: AnalyzerFrame):
        '''
        Process a frame from the input analyzer, and optionally return a single `AnalyzerFrame` or a list of `AnalyzerFrame`s.
        The type and data values in `frame` will depend on the input analyzer.
        '''
        # set our frame to an error frame, which will eventually get over-written as we get data.
        if self.temp_frame is None:
            self.temp_frame = AnalyzerFrame("error", frame.start_time, frame.end_time, {
                    "address": "error",
                    "data": "",
                    "count": 0
                }
            )

        if (frame.type == "start" or frame.type == "address") and self.temp_frame.type == "error":
            self.temp_frame = AnalyzerFrame("generic_data", frame.start_time, frame.end_time, {
                    "data": "",
                    "count": 0
                }
            )

            self._is_reg_next = True

        if frame.type == "address":
            address_byte = frame.data["address"][0]

            # Make sure this is a linear battery charger address
            if int(address_byte) == CHARGER_I2C_ADDRESS:
              self._continue_analysis = True

              if(not self._is_reg_next and frame.data["read"] is not None):
                if frame.data["read"]:
                  self.temp_frame.type = "generic_read"
                else:
                  self.temp_frame.type = "generic_write"
            else:
              self._continue_analysis = False

        if frame.type == "data":
          if self._continue_analysis:
            data_byte = frame.data["data"][0]

            # I2C is telling device which register to start at
            if self._is_reg_next:

              self._is_reg_next = False

              if int(data_byte) in REGISTERS:
                self.temp_frame.data["address"] = REGISTERS[data_byte]
              else:
                self.temp_frame.data["address"] = hex(data_byte)

            # I2C read or write register data
            else:
              self.temp_frame.data["count"] += 1
              if len(self.temp_frame.data["data"]) > 0:
                  self.temp_frame.data["data"] += ", "
              self.temp_frame.data["data"] += hex(data_byte)

        if frame.type == "stop":
            self.temp_frame.end_time = frame.end_time
            new_frame = self.temp_frame
            self.temp_frame = None

            if self._continue_analysis:
              self._continue_analysis = False
              return new_frame
