import serial
import time
from typing import Tuple
import logging

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
        logging.debug(f"Sending {cmd=} {data=}")
        self.ser.write(STX + cmd + data + ETX)
        ack = self.ser.read(1)
        logging.debug(f"{ack=}")
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

    def upload_image(self) -> Tuple[bytes, int, int, int]:
        _, n_cols, n_black_lines, n_visible_lines, n_status_bytes = self._send_command(
            b"U", b"\0", 5, read_etx=False
        )
        n_total = n_cols * (n_black_lines + n_visible_lines) + n_status_bytes
        img = self.ser.read(n_total)
        assert self.ser.read(1) == ETX
        return img, n_cols, n_black_lines, n_visible_lines

    def grab_image(self):
        self._send_command(b"G", b"\0", 2)

    def grab_result(self):
        return self._send_command(b"Y", b"\0", 2)


if __name__ == "__main__":
    import argparse
    from decode_image import decode_image
    import cv2

    parser = argparse.ArgumentParser()
    parser.add_argument("port")
    parser.add_argument("output_file")
    parser.add_argument("binary_file", default=None)
    args = parser.parse_args()

    cam = BarbieCamera(port=args.port)
    print("Taking picture")
    cam.reset_image_count(0)
    print(cam.grab_image())
    res = cam.grab_result()
    print("Waiting for camera to finish taking picture")
    while res[:1] == b"!":
        time.sleep(0.1)
        res = cam.grab_result()
    print("Downloading picture from camera")
    cam.reset_image_count(0)
    img, n_cols, n_black_lines, n_visible_lines = cam.upload_image()
    if args.binary_file is not None:
        with open(args.binary_file, "wb") as f:
            f.write(img)

    output_image = decode_image(img, n_cols=164, n_black_lines=2, n_visible_lines=124)
    cv2.imwrite(args.output_file, output_image)
