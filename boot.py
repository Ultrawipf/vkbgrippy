import usb_hid
import usb_cdc
# This is only one example of a gamepad descriptor, and may not suit your needs.
GAMEPAD_REPORT_DESCRIPTOR = bytes((
    0x05, 0x01,  # Usage Page (Generic Desktop Ctrls)
    0x09, 0x05,  # Usage (Game Pad)
    0xA1, 0x01,  # Collection (Application)
    0x85, 0x01,  #   Report ID (1)
    0x05, 0x09,  #   Usage Page (Button)
    0x19, 0x01,  #   Usage Minimum (Button 1)
    0x29, 0x20,  #   Usage Maximum (Button 32)
    0x15, 0x00,  #   Logical Minimum (0)
    0x25, 0x01,  #   Logical Maximum (1)
    0x75, 0x01,  #   Report Size (1)
    0x95, 0x20,  #   Report Count (32)
    0x81, 0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x05, 0x01,  #   Usage Page (Generic Desktop Ctrls)
    0x16, 0x01, 0x80,              #     LOGICAL_MINIMUM (-32767)
    0x26, 0xff, 0x7f,              #     LOGICAL_MAXIMUM (32767)
    0x09, 0x30,  #   Usage (X)
    0x09, 0x31,  #   Usage (Y)
    0x09, 0x32,  #   Usage (Z)
    # 0x09, 0x35,  #   Usage (Rz)
    0x75, 0x10,                    #    REPORT_SIZE (16)
    0x95, 0x03,  #   Report Count (3)
    0x81, 0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0xC0,        # End Collection
))
usb_cdc.enable(console=True, data=False)    # Enable console and data
gamepad = usb_hid.Device(
    report_descriptor=GAMEPAD_REPORT_DESCRIPTOR,
    usage_page=0x01,           # Generic Desktop Control
    usage=0x05,                # Gamepad
    report_ids=(1,),           # Descriptor uses report ID 4.
    in_report_lengths=(10,),    # This gamepad sends 8 bytes in its report.
    out_report_lengths=(0,),   # It does not receive any reports.
)

usb_hid.enable(
    (gamepad,)
)