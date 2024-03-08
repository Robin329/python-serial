# -*- coding: utf-8 -*-
import sys
import os
import asyncio
import serial_asyncio
import time
import serial
from serial.tools import list_ports

__doc__ = "This is the documentation for the pyserial module."


def __init__(port, baud,  bytes,  parity, stopbits):
    print("Serial open test")
    try:
        ser = serial.Serial(port, baud, bytes, parity, stopbits, timeout=None)
    except Exception as e:
        print("-- Exception --", e)
    # print(ser)
    return ser

async def serial_write_test(serial):
    serial.write('\n'.encode('utf-8'))
    while True:
        # data_to_send = await queue.get()
        # if data_to_send:
        serial.write("\n".encode('utf-8'))
        await serial.drain()
        await asyncio.sleep(1)


async def serial_read_test(serial):
    count = 0
    while True:
        data = await serial.readline()
        p = time.strftime("%X", time.localtime())
        print(f'received at:{count} {p} data:{data.decode()}')
        count += 1


def serial_exit(serial):
    if serial.is_open:
        serial.close()

async def async_main(port, baud):
    loop = asyncio.get_event_loop()
    reader, writer = await serial_asyncio.open_serial_connection(url=port, baudrate=baud)
    task_read = loop.create_task(serial_read_test(reader))
    task_write = loop.create_task(serial_write_test(writer))
    await task_read
    await task_write

def serial_lists():
    port_list = list(list_ports.comports())
    num = len(port_list)
    if num <= 0:
        print("No found ports")
    else:
        print("\nAvailable ports:")
        for i in range(num):
            port = list(port_list[i])
            print(f'[{i}]:'+str(port))
        return port_list

def main():
    port_input = input("Enter the port num(e.g., 0 or 1 ..):")
    port = int(port_input) if port_input.strip().isdigit() else 1
    # 50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
    baud_input = input("Enter the baud rate(e.g., 9600/115200):")
    baud = int(baud_input) if baud_input.strip().isdigit() and int(baud_input) in [
        50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600, 19200, 38400, 57600, 115200] else 115200
    bytes_input = input("Enter the number of bytes(default:8):")
    bytes = int(bytes_input) if bytes_input.strip().isdigit() else 8
    parity_input = input("Enter the parity(default:N):")
    parity = parity_input.strip().upper() if parity_input.strip().upper() in [
        'N', 'E', 'O'] else 'N'
    stopbits_input = input("Enter the stop bits(default:1):")
    stopbits = int(
        stopbits_input) if stopbits_input.strip().isdigit() else 1
    return port, baud, bytes, parity, stopbits
if __name__ == '__main__':
    sys.stdout.write(__doc__)
    ports_list = serial_lists()
    port, baud_rate, bytes, parity, stopbits = main()
    select_port = ports_list[port][0]
    # print(select_port)
    # ser = serial_open_test(select_port, baud_rate, bytes,  parity, stopbits)
    asyncio.run(async_main(select_port, baud_rate))
