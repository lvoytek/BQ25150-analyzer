REGISTERS = {
    0x00: "Charger Status 0",
    0x01: "Charger Status 1",
    0x02: "ADC Status",
    0x03: "Charger Flags 0",
    0x04: "Charger Flags 1",
    0x05: "ADC Flags",
    0x06: "Timer Flags",
    0x07: "Interrupt Mask 0",
    0x08: "Interrupt Mask 1",
    0x09: "Interrupt Mast 2",
    0x0a: "Interrupt Mask 3",
    0x12: "Battery Voltage Control",
    0x13: "Fast Charge Current Control",
    0x14: "Pre-Charge Current Control",
    0x15: "Termination Current Control",
    0x16: "Battery UVLO and Current Limit Control",
    0x17: "Charger Control 0",
    0x18: "Charger Control 1",
    0x19: "Input Current Limit Control",
    0x1d: "LDO Control",
    0x30: "MR Control",
    0x35: "IC Control 0",
    0x36: "IC Control 1",
    0x37: "IC Control 2",
    0x40: "ADC Control 0",
    0x41: "ADC Control 1",
    0x42: "VBatt MSB",
    0x43: "VBatt LSB",
    0x44: "TS MSB",
    0x45: "TS LSB",
    0x46: "Fast Charge Current MSB",
    0x47: "Fast Charge Current LSB",
    0x48: "ADC In MSB",
    0x49: "ADC In LSB",
    0x4a: "Vin MSB",
    0x4b: "Vin LSB",
    0x4c: "VpMid MSB",
    0x4d: "VpMid LSB",
    0x4e: "Iin MSB",
    0x4f: "Iin LSB",
    0x52: "Comparator 1 Threshold MSB",
    0x53: "Comparator 1 Threshold LSB",
    0x54: "Comparator 2 Threshold MSB",
    0x55: "Comparator 2 Threshold LSB",
    0x56: "Comparator 3 Threshold MSB",
    0x57: "Comparator 3 Threshold LSB",
    0x58: "ADC Channel Enable",
    0x61: "Fast Charge Control",
    0x62: "Cold Threshold",
    0x63: "Cool Threshold",
    0x64: "Warm Threshold",
    0x65: "Hot Threshold",
    0x6f: "Device ID"
}


def set_bit(bit_num):
    return 1 << bit_num


DERIVED_STATUS = {
    # Status Register 0
    0x00: {
        set_bit(0): "Good",
        set_bit(1): "Thermal Regulation Active",
        set_bit(2): "VINDPM Active",
        set_bit(3): "DPPM Active",
        set_bit(4): "Input Current Limit Active",
        set_bit(5): "Charging Done",
        set_bit(6): "Constant Voltage Charge Mode Active"
    },
    # Status Register 1
    0x01: {
        set_bit(0): "Hot",
        set_bit(1): "Warm",
        set_bit(2): "Cool",
        set_bit(3): "Cold",
        set_bit(4): "Battery Voltage Below Vbatuvlo",
        set_bit(5): "Battery Over-Current Protection Active",
        set_bit(7): "Vin Overvolted"
    },
    # ADC Status
    0x02: {
        set_bit(0): "TS open",
        set_bit(4): "ADC Voltage Above Level 3",
        set_bit(5): "ADC Voltage Above Level 2",
        set_bit(6): "ADC Voltage Above Level 1"
    },
    # Flags 0
    0x03: {
        set_bit(0): "Vin Power Good",
        set_bit(1): "Thermal Regulation Detected",
        set_bit(2): "VINDPM Detected",
        set_bit(3): "DPPM Detected",
        set_bit(4): "Input Current Limit Detected",
        set_bit(5): "Charging Done",
        set_bit(6): "Constant Voltage Charge Mode Detected"
    },
    # Flags 1
    0x04: {
        set_bit(0): "Hot Region Entry Detected",
        set_bit(1): "Warm Region Entry Detected",
        set_bit(2): "Cool Region Entry Detected",
        set_bit(3): "Cold Region Entry Detected",
        set_bit(4): "Battery Undervoltage Detected",
        set_bit(5): "Battery Over-Current Detected",
        set_bit(7): "Vin Overvoltage Detected"
    }
}

# List of MSB regs for multi-byte data entries
MULTI_BYTE_DATA = {
    0x42: {
        "name": "Battery Voltage",
        "units": "mV",
        "convert": 6000 / 65535
    },
    0x44: {
        "name": "Thermistor Input",
        "units": "mV",
        "convert": 1200 / 65535
    },
    0x46: {
        "name": "Charge Current",
        "units": ""
    },
    0x48: {
        "name": "ADC Input",
        "units": ""
    },
    0x4a: {
        "name": "Vin",
        "units": ""
    },
    0x4c: {
        "name": "Vpmid",
        "units": ""
    },
    0x4e: {
        "name": "Iin",
        "units": ""
    }
}
