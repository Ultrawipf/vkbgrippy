import struct

from adafruit_hid import find_device
class VKBGrip:
    def __init__(self,uart,devices,hidlen,setuppacket,replylen):
        self.setuppacket = bytes(setuppacket)
        self.setuplen = len(setuppacket)
        self.replylen = replylen
        self.uart = uart
        self.buttons = 0
        self.analog = []

        self._gamepad_device = find_device(devices, usage_page=0x1, usage=0x05)
        self._report = bytearray(hidlen)
        self._last_report = bytearray(hidlen)

        self.buttons_state = 0 # 32 buttons
        self.joy_x = 0
        self.joy_y = 0
        self.joy_z = 0
        # self.joy_r_z = 0

    def send_report(self, always=False):

        struct.pack_into(
            "<IHHH",
            self._report,
            0,
            self.buttons_state,
            self.joy_x,
            self.joy_y,
            self.joy_z,

        )

        if always or self._last_report != self._report:
            self._gamepad_device.send_report(self._report)
            self._last_report[:] = self._report
       

    def process_reply(self,packet):
        return True

    def request(self):
        self.uart.write(self.setuppacket)
        reply = self.uart.read(self.setuplen+self.replylen)
        if not reply or len(reply) < self.setuplen+self.replylen:
            return False
        else:
            reply = reply[self.setuplen::]
            return self.process_reply(reply)



class Kosmosima(VKBGrip):
    def __init__(self,uart,devices,hidlen):
        VKBGrip.__init__(self,uart=uart,devices=devices,hidlen=hidlen,setuppacket=[0xA5,0x0B,0x11,0x98,0x00,0x00,0x00,0xE5,0x20], replylen= 29)
        self.xormask = bytes([0x5a, 0xb, 0x11, 0xc8, 0x14, 0xd5, 0xde, 0x1c, 0xa, 0x69, 0xf7, 0xc2, 121, 113, 243, 201, 231, 241, 0xff, 0xff, 00, 0x87, 0xa6, 0xf4, 0xbf, 0x29, 0xd9, 0x93, 0x2d])
                                                                                               # 11    113          ?   241
        self.lastanalog = 0
        # The lower bits in the lower byte of the analog values may still be incorrect in xor mask
        # Byte 15 either 54 or 201 xor
    def process_reply(self,packet):
        # print([hex(d) for d in packet])
        # print(bin(packet[12]))

        # analog = packet[14]
        # # print(bin(analog))
        # xor = self.lastanalog ^ analog
        # if xor == 0xff: # or 7f
        #     print(self.lastanalog , analog)
        # self.lastanalog = analog

        packet = bytes([d ^ i for d,i in zip(packet,self.xormask)])
       
        # buttons
        buttons = packet[25:29]
        self.buttons_state = 0
        for i,b in enumerate(buttons):
            self.buttons_state |= (b) << i*8
        self.buttons_state = self.buttons_state >> 1 # shift 1 down
        
        
        # analog axes are in the bytes 12/13, 14/15 and 16/17. 12b resolution. maybe offset of 123
        self.joy_z = (packet[16] | ((packet[17]+124)&0xf) << 8) << 4
        self.joy_x = (packet[12] | ((packet[13]-1)&0xf) << 8) << 4
        self.joy_y = (packet[14] | ((packet[15])&0xf) << 8) << 4



        return True