import serial
import serial.tools.list_ports
from time import sleep
from tkinter import messagebox

# cmd = bytes.fromhex("AA 55 12 05 02 00 00 00 00 00 00 00 00 01 00 00 00 00 00 1A")  # AA 55 12 05 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 19
cmd = bytes.fromhex("AA 55 12 05 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 19")
# cmd = bytearray([0xAA,0x55,0x12,0x05,0x02,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x00,0x00,0x1A])
packet = bytearray([0xAA,0xE2,0x00,0x03,0x0C,0x00])

ser = serial

commands = {
    "OPERATION" : 0x0000,
    "VOUT_SET" : 0x0020,
    "IOUT_SET" : 0x0030,
    "FAULT_STATUS" : 0x0040,
    "READ_VIN" : 0x0050,
    "READ_VOUT" : 0x0060,
    "READ_IOUT" : 0x0061,
    "READ_TEMPERATURE_1" : 0x0062,
    "MFR_ID_B085" : 0x0080,
    "MFR_ID_B6B11" : 0x0081,
    "MFR_MODEL_B085" : 0x0082,
    "MFR_MODEL_B6B11" : 0x0083,
    "MFR_REVISION_B085" : 0x0084,
    "MFR_LOCATION_B082" : 0x0085,
    "MFR_DATE_B085" : 0x0086,
    "MFR_SERIAL_B085" : 0x0087,
    "MFR_SERIAL_B6B11" : 0x0088,
    "SCALING_FACTOR" : 0x00C0,
    "SYSTEM_STATUS" : 0x00C1,
    "SYSTEM_CONFIG" : 0x00C2,
    "DIRECTION_CTRL" : 0x0100,
    "REVERSE_VOUT_SET" : 0x0120,
    "REVERSE_IOUT_SET" : 0x0130,
    "BIDIRECTIONAL_CONFIG" : 0x0140

}

def list_ports():
    port_list = []
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        # print("{}: {}".format(port, desc))
        port_list.append(port)
    return port_list

def send_data(command,data,twice=True):
    global ser
    sdata = packet.copy()
    data = data.to_bytes(2,"little")
    if(twice):
        sdata[1] = sdata[1]+data.__len__()
    else:
        sdata[1] = sdata[1]+data.__len__()-1
    sdata.append(commands.get(command) & 0x00FF)
    sdata.append((commands.get(command) & 0xFF00)>>8)
    sdata.append(data[0])
    if(twice):
        sdata.append(data[1])
    sdata.append(0x55)
    try:
        len = ser.write(sdata)
        if len != 0 :
            return True
    except:
        raise ValueError("Unable to send or read data to the COM PORT\n Please check the serial connection and try again!")

def read_data(command,size):
    global ser
    rdata = packet.copy()
    rdata.append(commands.get(command) & 0x00FF)
    rdata.append((commands.get(command) & 0xFF00)>>8)
    rdata.append(0x55)
    try :
        ser.write(rdata)
        received_data = ser.read(size=(size+9))[6:-1]
    except:
        raise ValueError("Unable to send or read data to the COM PORT\n Please check the serial connection and try again!")
    # print(received_data.hex(" "))
    try :
        if (received_data[1]<<8|received_data[0]) == commands.get(command):
            return received_data[2:]
    except:
        raise ValueError("Unable to read data from CAN\nPlease check the CAN connection and try again!")

def serial_initialize(com_port):
    global ser
    try :
        ser = serial.Serial(com_port,timeout=0.05,baudrate=115200)  # open serial port
        if(ser.is_open):
            # print(ser.name)
            ser.write(cmd)
            sleep(0.25)
            send_data("SYSTEM_CONFIG",0x0403)
            return True
    except:
        messagebox.showerror(title="Error",message="Unable to open the COM PORT\n Please check the serial connection and try again!")
        return False

def serial_deinitialize():
    global ser
    try :
        ser.close()
        if(not ser.is_open):
            return True
    except:
        messagebox.showerror(title="Error",message="Unable to close the COM PORT\n Please check the serial connection and try again!")
        return False

# serial_initialize('COM8')
# val = read_data("MFR_ID_B085") + read_data("MFR_ID_B6B11")
# print(val.decode())

# val = bytes.fromhex("FF00")
# if (val[0] & 0x01) == 0:
#     print("yes")
# else:
#     print("no")

# str_1 = "20"
# for i in range(val.__len__()):
#     str_1 = str_1 + str(val[i])
#     if(i%2==0 and i != 0):
#         str_1 = str_1 + "/"

# print(str(23))
# serial_deinitialize()

