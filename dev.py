import serial
import time

STX = b"\x02"
ETX = b"\x03"
ACK = b"\x06"
NACK = b"\x15"


class BarbieCamera:
    ser: serial.Serial

    def __init__(self, port: str):
        self.ser = serial.Serial(
            port=port,
            baudrate=57600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
        )

    def _send_command(
        self, cmd: bytes, data: bytes, response_length: int, read_etx: bool = True
    ) -> bytes:
        print(f"Sending {cmd=} {data=}")
        self.ser.write(STX + cmd + data + ETX)
        ack = self.ser.read(1)
        print(f"{ack=}")
        assert ack == ACK, "Command not acked"
        stx = self.ser.read(1)
        assert stx == STX
        resp = self.ser.read(response_length)
        if read_etx:
            assert self.ser.read(1) == ETX
        return resp

    def echo_byte(self, byte: bytes):
        assert len(byte) == 1, "Echo Byte supports 1 byte only"
        return self._send_command(b"E", byte, 2)

    def reset_image_count(self, val: int):
        return self._send_command(b"A", bytes([val]), 2)

    def get_image_index(self) -> int:
        return self._send_command(b"I", b"\0", 2)[1]

    def upload_image(self) -> bytes:
        _, n_cols, n_black_lines, n_visible_lines, n_status_bytes = self._send_command(
            b"U", b"\0", 5, read_etx=False
        )
        print(n_cols, n_black_lines, n_visible_lines, n_status_bytes)
        n_total = n_cols * (n_black_lines + n_visible_lines) + n_status_bytes
        img = self.ser.read(n_total)
        assert self.ser.read(1) == ETX
        return img

    def grab_image(self):
        print(self._send_command(b"G", b"\0", 2))

    def grab_result(self):
        return self._send_command(b"Y", b"\0", 2)


if __name__ == "__main__":
    cam = BarbieCamera(port="/dev/tty.usbserial-A9BI3S58")
    print(cam.reset_image_count(0))
    print(cam.grab_image())
    res = cam.grab_result()
    print(f"{res=}")
    while res[:1] == b"!":
        time.sleep(0.1)
        res = cam.grab_result()
        print(f"{res=}")
    print(cam.reset_image_count(0))
    img = cam.upload_image()
    print(f"{cam.get_image_index()=}")
    with open("test.bin", "wb") as f:
        f.write(img)
