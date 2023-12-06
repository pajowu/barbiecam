# Barbiecam

Bringing new life to Mattels Barbie Photo Designer / Nick Click digital camera.

## Installation

[Install poetry](https://python-poetry.org/docs/#installation)

Now run the following command in the barbiecam folder to install all needed dependencies

```shell
poetry install
```

## Usage

Connect the camera using a rs232 adapter. Figure our the port name (linux: /dev/ttyUSB???; on mac /dev/tty.usbserial-???, on window COM??) and then run

```shell
poetry run python dev.py PORT OUTPUT_FILENAME BINARY_FILENAME
```

This will capture an image with the camera connected via `PORT` and then decode it and save it to `OUTPUT_FILENAME`

## Credit

This was hacked together very quickly on a long evening based on the [incredible documentation for picoweb](https://www.picoweb.net/download/c0800blpdf.pdf) and the command protocol the [cipa webcam for linux project got](https://webcam.sourceforge.net/news.html)
