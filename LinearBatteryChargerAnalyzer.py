# High Level Analyzer
# For more information and documentation, please go to https://support.saleae.com/extensions/high-level-analyzer-extensions

from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting, NumberSetting, ChoicesSetting

import struct
import BQ25150

DATA_COMMANDS = {

}

CHARGER_I2C_ADDRESS = 0x6B

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
          'format' : '{{data.address}} {{data.data}}'
        },
        'generic_read': {
          'format' : 'Read {{data.data}} from the {{data.address}} register'
        },
        'generic_write': {
          'format' : 'Wrote {{data.data}} to the {{data.data}} register'
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
        self._current_register = -1

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
                }
            )

        if (frame.type == "start" or frame.type == "address") and self.temp_frame.type == "error":
            self.temp_frame = AnalyzerFrame("generic_data", frame.start_time, frame.end_time, {
                    "data": "",
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
            data_byte = int(frame.data["data"][0])

            # I2C is telling device which register to start at
            if self._is_reg_next:

              self._is_reg_next = False

              self._current_register = data_byte

              if data_byte in BQ25150.REGISTERS:
                self.temp_frame.data["address"] = BQ25150.REGISTERS[data_byte]
              else:
                self.temp_frame.data["address"] = hex(data_byte)

            # I2C read or write register data
            else:
              # This is a status register, view each bit value
              if(self._current_register in BQ25150.DERIVED_STATUS):
                for status_bit in BQ25150.DERIVED_STATUS[self._current_register].keys():
                  if(status_bit & data_byte):
                    if len(self.temp_frame.data["data"]) > 0:
                      self.temp_frame.data["data"] += ", "
                    self.temp_frame.data["data"] += BQ25150.DERIVED_STATUS[self._current_register][status_bit]

              # This is a generic register, just show a hex value
              else:
                self.temp_frame.data["data"] = hex(data_byte)

        if frame.type == "stop":
            self.temp_frame.end_time = frame.end_time
            new_frame = self.temp_frame
            self.temp_frame = None

            if self._continue_analysis:
              self._continue_analysis = False
              self._current_register = -1
              return new_frame
