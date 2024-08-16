# imports
from tkinter import *
from tkinter import ttk
from tk_tools import *
from tkinter import messagebox
from can_control import *

#global variables
id = int()
paused = bool()

# Old values of inputation which are stored to verify if new data is available or not
old_values = {
    "OPERATION" : "1",
    "VOUT_SET" : "",
    "IOUT_SET" : "",
    "REVERSE_VOUT_SET" : "",
    "REVERSE_IOUT_SET" : "",
    "BIDIRECTIONAL_CONFIG" : "",
    "DIRECTION_CTRL" : "0"
}

# The scaling factors required for the conversion of voltage and current
scaling_factors = {
    "VOUT" : 0.01,
    "IOUT" : 0.01,
    "VIN" : 0.1,
    "FAN_SPEED" : 0,
    "TEMPERATURE_1" : 0.1,
    "IIN" : 0
}

# The scaling factors presets required mapping of scaling factors
scaling_factors_presets = {
    0x0 : 0,
    0x4 : 0.001,
    0x5 : 0.01,
    0x6 : 0.1,
    0x7 : 1,
    0x8 : 10,
    0x9 : 100
}

# Font Settings
myfont = ("Arial",10,"bold")

# Function to refresh the com port combo box with new availablity of com ports
def refresh_ports():
    com_port_combo_box.config(values=list_ports())

# Function to intialize the GUI i.e enabling all the components as well staring the serial and CAN communication
def initialize():
    if(com_port_combo_box.get()):
        if(serial_initialize(com_port_combo_box.get())):
            start_button.config(state=DISABLED)
            refresh_button.config(state=DISABLED)
            stop_button.config(state=ACTIVE)
            pause_display_button.config(state=ACTIVE)
            operation_write_0_radio_button.config(state=ACTIVE)
            operation_write_1_radio_button.config(state=ACTIVE)
            output_voltage_write_entry.config(state=NORMAL)
            output_current_write_entry.config(state=NORMAL)
            discharge_voltage_write_entry.config(state=NORMAL)
            discharge_current_write_entry.config(state=NORMAL)
            set_submit_button.config(state=ACTIVE)
            bidirection_mode_write_0_radio_button.config(state=ACTIVE)
            bidirection_mode_write_1_radio_button.config(state=ACTIVE)
            mode_submit_button.config(state=ACTIVE)

            input_voltage_val_label.config(state=ACTIVE)
            output_voltage_val_label.config(state=ACTIVE)
            output_current_val_label.config(state=ACTIVE)
            temperature_val_label.config(state=ACTIVE)
            set_output_voltage_val_label.config(state=ACTIVE)
            set_output_current_val_label.config(state=ACTIVE)
            set_discharge_voltage_val_label.config(state=ACTIVE)
            set_discharge_current_val_label.config(state=ACTIVE)

            manufacturer_name_val_label.config(state=ACTIVE)
            manufacturer_model_name_val_label.config(state=ACTIVE)
            firmware_revision_val_label.config(state=ACTIVE)
            # manufacturer_factory_location_val_label.config(state=ACTIVE)
            manufacturer_date_val_label.config(state=ACTIVE)
            product_serial_number_val_label.config(state=ACTIVE)

            read_scaling_factor()
            read_manufacturer_details()
            readings_update()

# Function to deintialize the GUI i.e disabling all the components as well staring the serial and CAN communication
def deinitialize():
    global id
    window.after_cancel(id) if not paused else ''''''
    if(serial_deinitialize()):
        start_button.config(state=ACTIVE)
        refresh_button.config(state=ACTIVE)
        stop_button.config(state=DISABLED)
        resume_display_button.config(state=DISABLED)
        pause_display_button.config(state=DISABLED)
        operation_write_0_radio_button.config(state=DISABLED)
        operation_write_1_radio_button.config(state=DISABLED)
        output_voltage_write_entry.config(state=DISABLED)
        output_current_write_entry.config(state=DISABLED)
        discharge_voltage_write_entry.config(state=DISABLED)
        discharge_current_write_entry.config(state=DISABLED)
        set_submit_button.config(state=DISABLED)
        direction_control_write_0_radio_button.config(state=DISABLED)
        direction_control_write_1_radio_button.config(state=DISABLED)
        bidirection_mode_write_0_radio_button.config(state=DISABLED)
        bidirection_mode_write_1_radio_button.config(state=DISABLED)
        mode_submit_button.config(state=DISABLED)

        input_voltage_val_label.config(state=DISABLED)
        output_voltage_val_label.config(state=DISABLED)
        output_current_val_label.config(state=DISABLED)
        temperature_val_label.config(state=DISABLED)
        set_output_voltage_val_label.config(state=DISABLED)
        set_output_current_val_label.config(state=DISABLED)
        set_discharge_voltage_val_label.config(state=DISABLED)
        set_discharge_current_val_label.config(state=DISABLED)

        operation_label_led.to_grey()
        fan_fail_label_led.to_grey()
        over_temperature_label_led.to_grey()
        dc_over_voltage_label_led.to_grey()
        dc_over_current_label_led.to_grey()
        short_circuit_label_led.to_grey()
        ac_fail_label_led.to_grey()
        dc_status_label_led.to_grey()
        high_temperature_label_led.to_grey()
        hv_over_voltage_label_led.to_grey()
        device_slave_label_led.to_grey()
        device_master_label_led.to_grey()
        secondary_dd_output_voltage_label_led.to_grey()
        primary_pfc_label_led.to_grey()
        active_dummy_load_label_led.to_grey()
        device_initialized_label_led.to_grey()
        eeprom_data_access_label_led.to_grey()
        direction_ad_label_led.to_grey()
        direction_da_label_led.to_grey()
        bidirection_auto_detect_label_led.to_grey()
        bidirection_battery_label_led.to_grey()

        manufacturer_name_val_label.config(state=DISABLED)
        manufacturer_model_name_val_label.config(state=DISABLED)
        firmware_revision_val_label.config(state=DISABLED)
        # manufacturer_factory_location_val_label.config(state=DISABLED)
        manufacturer_date_val_label.config(state=DISABLED)
        product_serial_number_val_label.config(state=DISABLED)

# Function to resume the updates of readings and flags
def resume_display():
    global id,paused
    paused = False
    id = window.after(1000,readings_update)
    resume_display_button.config(state=DISABLED)
    pause_display_button.config(state=ACTIVE)

# Function to pause the updates of readings and flags
def pause_display():
    global id,paused
    paused = True
    window.after_cancel(id)
    resume_display_button.config(state=ACTIVE)
    pause_display_button.config(state=DISABLED)

# Function to be called when the "Set Reference" button is clicked
# Sends updated values of voltage and current to the power supply
def set_submit():
    global id
    ov =False
    oi = False
    rov = False
    roi = False
    input_error = False
    error = False
    str_1 = 'Please Input the values between the ranges!'

    #Stop the readings update if not paused
    window.after_cancel(id) if not paused else ''''''
    
    # Check for Range Errors as well as new values and whether the values are purely numerical
    try :
        if old_values.get("VOUT_SET") != output_voltage_write_entry.get() and output_voltage_write_entry.get() != "":
            if (float(output_voltage_write_entry.get()) < 38 or float(output_voltage_write_entry.get()) > 65):
                error = True
                str_1 = str_1 + "\nOutput Voltage out of range"
            else:
                ov = True
        
        if old_values.get("IOUT_SET") != output_current_write_entry.get() and output_current_write_entry.get() != "":
            if (float(output_current_write_entry.get())< 0 or float(output_current_write_entry.get()) > 40):
                error = True
                str_1 = str_1 + "\nOutput Current out of range"
            else:
                oi = True

        if old_values.get("REVERSE_VOUT_SET") != discharge_voltage_write_entry.get() and discharge_voltage_write_entry.get() != "":
            if (float(discharge_voltage_write_entry.get()) < 38 or float(discharge_voltage_write_entry.get()) > 65):
                error = True
                str_1 = str_1 + "\nDischarge Voltage out of range"
            else:
                rov = True

        if old_values.get("REVERSE_IOUT_SET") != discharge_current_write_entry.get() and discharge_current_write_entry.get() != "":
            if (float(discharge_current_write_entry.get())< 0 or float(discharge_current_write_entry.get()) > 40):
                error = True
                str_1 = str_1 + "\nDischarge Current out of range"
            else:
                roi = True
    except:
        messagebox.showwarning(title="Warning",message="Only input numbers in the input field!")
        error = True
        input_error = True

    # Send the values of updated fields
    try:
        if not error:
            (send_data("OPERATION",int(operation_write_val.get()),False),old_values.__setitem__("OPERATION",operation_write_val.get())) if old_values.get("OPERATION") != operation_write_val.get() else ''''''
            if(ov):
                send_data("VOUT_SET",int(float(output_voltage_write_entry.get())/scaling_factors.get("VOUT")))
                old_values.__setitem__("VOUT_SET",output_voltage_write_entry.get())
            if(oi):
                send_data("IOUT_SET",int(float(output_current_write_entry.get())/scaling_factors.get("IOUT")))
                old_values.__setitem__("IOUT_SET",output_current_write_entry.get())
            if(rov):
                send_data("REVERSE_VOUT_SET",int(float(discharge_voltage_write_entry.get())/scaling_factors.get("VOUT")))
                old_values.__setitem__("REVERSE_VOUT_SET",discharge_voltage_write_entry.get())
            if(roi):
                send_data("REVERSE_IOUT_SET",int(float(discharge_current_write_entry.get())/scaling_factors.get("IOUT")))
                old_values.__setitem__("REVERSE_IOUT_SET",discharge_current_write_entry.get())
        elif not input_error:
            messagebox.showwarning(title='Warning',message=str_1)
    except Exception as e:
       messagebox.showerror(title="Error",message=e)

    #Resume the readings update if not paused
    id = window.after(1000,readings_update) if not paused else ''''''

# Function to be called when the "Set Mode" button is clicked
# Sends updated values of direction and bidirection registers to the power supply  
def mode_submit():
    global id,paused
    check = False

    #Stop the readings update if not paused
    window.after_cancel(id) if not paused else ''''''

    # Check for new values and confirmation
    try:
        if(old_values.get("BIDIRECTIONAL_CONFIG") != bidirection_mode_write_val.get()):
            if(bidirection_mode_write_val.get() == "0"):
                str_1 = 'The System will have to be rebooted and direction control will be auto\nContinue?'
            elif(bidirection_mode_write_val.get() == "1"):
                str_1 = 'The System will have to be rebooted and direction control will be manual\nContinue?'
            if messagebox.askyesno(title='System',message=str_1):

                #if true send the command to change the mode and stop the serial communication
                send_data("BIDIRECTIONAL_CONFIG",int(bidirection_mode_write_val.get()))
                paused = True
                check = True
                deinitialize()
        if not check:
            (send_data("DIRECTION_CTRL",int(direction_control_write_val.get()),False),old_values.__setitem__("DIRECTION_CTRL",direction_control_write_val.get())) if old_values.get("DIRECTION_CTRL") != direction_control_write_val.get() else ''''''
            id = window.after(1000,readings_update) if not paused else ''''''
    except Exception as e:
       messagebox.showerror(title="Error",message=e)

# Function to read the scaling factor register and update the scaling_factor dictonary
def read_scaling_factor():
    try:
        val = read_data("SCALING_FACTOR",6)
        if(val):
            scaling_factors.__setitem__("VOUT",scaling_factors_presets.get((val[0]&0x0F)))
            scaling_factors.__setitem__("IOUT",scaling_factors_presets.get((val[0]&0xF0)>>4))
            scaling_factors.__setitem__("VIN",scaling_factors_presets.get((val[1]&0x0F)))
            scaling_factors.__setitem__("FAN_SPEED",scaling_factors_presets.get((val[1]&0xF0)>>4))
            scaling_factors.__setitem__("TEMPERATURE_1",scaling_factors_presets.get((val[2]&0x0F)))
            scaling_factors.__setitem__("IIN",scaling_factors_presets.get((val[3]&0x0F)))
    except Exception as e:
        messagebox.showerror(title="Error",message=e)

# Function to read the manfacturing details registers and update the the neccessary variabels so that it can be reflected on the GUI
def read_manufacturer_details():
    try:
        val = read_data("MFR_ID_B085",6) + read_data("MFR_ID_B6B11",6)
        manufacturer_name_val.set(val.decode())
        val = read_data("MFR_MODEL_B085",6) + read_data("MFR_MODEL_B6B11",6)
        manufacturer_model_name_val.set(val.decode())
        val = read_data("MFR_REVISION_B085",6)
        str_1 = ""
        for i in range(val.__len__()):
            if val[i] != 0xFF:
                str_1 = str_1 + str(val[i]/10) + ", "
        firmware_revision_val.set(str_1[:-2])
        val = read_data("MFR_DATE_B085",6)
        val = val.decode()
        str_1 = "20"
        for i in range(val.__len__()):
            if(i%2==0 and i != 0):
                str_1 = str_1 + "/"
            str_1 = str_1 + val[i]
        manufacturer_date_val.set(str_1)

        val = read_data("MFR_SERIAL_B6B11",6)
        product_serial_number_val.set(val.decode())

        manufacturer_name_val_label.config(text=manufacturer_name_val.get())
        manufacturer_model_name_val_label.config(text=manufacturer_model_name_val.get())
        firmware_revision_val_label.config(text=firmware_revision_val.get())
        manufacturer_date_val_label.config(text=manufacturer_date_val.get())
        product_serial_number_val_label.config(text=product_serial_number_val.get())
    except Exception as e:
        messagebox.showerror(title="Error",message=e)

# Function to read the voltage, current and various flags of the power supply and accordingly update the components
def readings_update():
    global id,paused
    paused = False

    #The registers are read sequencially and necessary operations are performed on the received data and thus fields are updated
    #Refer to Detailed Guide for colour of led on the basis of readings
    try :
        val = read_data("OPERATION",1)
        buffer = int.from_bytes(val,"little")
        operation_label_led.to_grey() if buffer==0 else operation_label_led.to_green(on=True)
        
        val = read_data("FAULT_STATUS",2)
        fan_fail_label_led.to_grey() if ((val[0] & 0x01)>>0) == 0 else fan_fail_label_led.to_red(on=True)
        over_temperature_label_led.to_grey() if ((val[0] & 0x02)>>1) == 0 else over_temperature_label_led.to_red(on=True)
        dc_over_voltage_label_led.to_grey() if ((val[0] & 0x04)>>2) == 0 else dc_over_voltage_label_led.to_red(on=True)
        dc_over_current_label_led.to_grey() if ((val[0] & 0x08)>>3) == 0 else dc_over_current_label_led.to_red(on=True)
        short_circuit_label_led.to_grey() if ((val[0] & 0x10)>>4) == 0 else short_circuit_label_led.to_red(on=True)
        ac_fail_label_led.to_grey() if ((val[0] & 0x20)>>5) == 0 else ac_fail_label_led.to_red(on=True)
        dc_status_label_led.to_grey() if ((val[0] & 0x40)>>6) == 0 else dc_status_label_led.to_red(on=True)
        high_temperature_label_led.to_grey() if ((val[0] & 0x80)>>7) == 0 else high_temperature_label_led.to_red(on=True)
        hv_over_voltage_label_led.to_grey() if ((val[1] & 0x01)>>0) == 0 else hv_over_voltage_label_led.to_red(on=True)    

        val = read_data("SYSTEM_STATUS",2)
        (device_slave_label_led.to_green(on=True),device_master_label_led.to_grey()) if ((val[0] & 0x01)>>0) == 0 else (device_slave_label_led.to_grey(),device_master_label_led.to_green(on=True))
        secondary_dd_output_voltage_label_led.to_red(on=True) if ((val[0] & 0x02)>>1) == 0 else secondary_dd_output_voltage_label_led.to_grey()
        primary_pfc_label_led.to_red(on=True) if ((val[0] & 0x04)>>2) == 0 else primary_pfc_label_led.to_grey()
        active_dummy_load_label_led.to_grey() if ((val[0] & 0x10)>>4) == 0 else active_dummy_load_label_led.to_red(on=True)
        device_initialized_label_led.to_green(on=True) if ((val[0] & 0x20)>>5) == 0 else device_initialized_label_led.to_red(on=True)
        eeprom_data_access_label_led.to_grey() if ((val[0] & 0x40)>>6) == 0 else eeprom_data_access_label_led.to_red(on=True)

        val = read_data("DIRECTION_CTRL",1)
        buffer = int.from_bytes(val,"little")
        (direction_ad_label_led.to_green(on=True),direction_da_label_led.to_grey(),old_values.__setitem__("DIRECTION_CTRL","0")) if buffer == 0 else (direction_ad_label_led.to_grey(),direction_da_label_led.to_green(on=True),old_values.__setitem__("DIRECTION_CTRL","1"))

        val = read_data("BIDIRECTIONAL_CONFIG",2)
        (bidirection_auto_detect_label_led.to_green(on=True),bidirection_battery_label_led.to_grey(),old_values.__setitem__("BIDIRECTIONAL_CONFIG","0"),
        direction_control_write_0_radio_button.config(state=DISABLED),direction_control_write_1_radio_button.config(state=DISABLED)) if ((val[0] & 0x01)>>0) == 0  else (bidirection_auto_detect_label_led.to_grey(),bidirection_battery_label_led.to_green(on=True),old_values.__setitem__("BIDIRECTIONAL_CONFIG","1"),
                                                                                                                                                                        direction_control_write_0_radio_button.config(state=ACTIVE),direction_control_write_1_radio_button.config(state=ACTIVE))

        val = read_data("READ_VIN",2)
        buffer = int.from_bytes(val,"little")
        input_voltage_val.set(str(round(buffer*scaling_factors.get("VIN"),2))+' V')

        val = read_data("READ_VOUT",2)
        buffer = int.from_bytes(val,"little")
        output_voltage_val.set(str(round(buffer*scaling_factors.get("VOUT"),2))+' V')

        val = read_data("READ_IOUT",2)
        buffer = int.from_bytes(val,"little")
        output_current_val.set(str(round(buffer*scaling_factors.get("IOUT"),2))+' A')

        val = read_data("READ_TEMPERATURE_1",2)
        buffer = int.from_bytes(val,"little")
        temperature_val.set(str(round(buffer*scaling_factors.get("TEMPERATURE_1"),2))+ " " + u'\u2103')

        val = read_data("VOUT_SET",2)
        buffer = int.from_bytes(val,"little")
        set_output_voltage_val.set(str(round(buffer*scaling_factors.get("VOUT"),2))+' V')

        val = read_data("IOUT_SET",2)
        buffer = int.from_bytes(val,"little")
        set_output_current_val.set(str(round(buffer*scaling_factors.get("IOUT"),2))+' A')

        val = read_data("REVERSE_VOUT_SET",2)
        buffer = int.from_bytes(val,"little")
        set_discharge_voltage_val.set(str(round(buffer*scaling_factors.get("VOUT"),2))+' V')

        val = read_data("REVERSE_IOUT_SET",2)
        buffer = int.from_bytes(val,"little")
        set_discharge_current_val.set(str(round(buffer*scaling_factors.get("IOUT"),2))+' A')

        input_voltage_val_label.config(text=input_voltage_val.get())
        output_voltage_val_label.config(text=output_voltage_val.get())
        output_current_val_label.config(text=output_current_val.get())
        temperature_val_label.config(text=temperature_val.get())
        set_output_voltage_val_label.config(text=set_output_voltage_val.get()) 
        set_output_current_val_label.config(text=set_output_current_val.get()) 
        set_discharge_voltage_val_label.config(text=set_discharge_voltage_val.get()) 
        set_discharge_current_val_label.config(text=set_discharge_current_val.get()) 

        # Call the function again after 1 second
        id = window.after(1000,readings_update)
    except Exception as e:
        messagebox.showerror(title="Error",message=e)
        id = window.after(1000,readings_update)
        pause_display()


#############################################################################################################################################################################

#instantiate an instance of a window and set its name and size
window = Tk()                   
# window.state('zoomed')
window.geometry("700x700")
window.title("GUI Window")

#create a nootbook in the window
notebook = ttk.Notebook(window)   

#create tabs i.e Frames in the notebook
output_tab = Frame(notebook)
details_tab = Frame(notebook)
mode_tab = Frame(notebook)

#add the created tabs in the nootbook
notebook.add(output_tab,text='Readings')
notebook.add(details_tab,text='Details')
notebook.add(mode_tab,text='Mode')

#place the nootbook into the main window
notebook.pack(expand=TRUE,fill=BOTH)

#add seperators\lines to create seperate zones 
separator = ttk.Separator(output_tab, orient='vertical')
separator.place(relx=0.48, rely=0.01,y=25, relwidth=0.1, relheight=1)
separator = ttk.Separator(output_tab, orient='horizontal')
separator.place(relx=0, rely=0.48, relwidth=0.48, relheight=0.1)
separator = ttk.Separator(output_tab, orient='horizontal')
separator.place(relx=0, rely=0.01, y=25, relwidth=1, relheight=0)


#############################################################################################################################################################################
#First Zone - COM PORT SELECTION

#create a combo box\list to display the com ports available in the system
com_port_combo_box = ttk.Combobox(
    output_tab,
    state="readonly",
    values= list_ports()
)

#add some text to the zone for user to understand different components
com_port_label = Label(output_tab,text="COM Port : ",font=myfont)
com_port_label.place(relx=0.05, rely=0.005, y=0) 
com_port_combo_box.place(relx=0.05,x=100, rely=0.005, y=0,width=100)
#add a refresh button
refresh_button = Button(output_tab,text='Refresh',command=refresh_ports)
refresh_button.place(relx=0.05,x=225,rely=0.005, y=0,width=50)
#add a start button
start_button = Button(output_tab,text='Start',command=initialize)
start_button.place(relx=0.05,x=275,rely=0.005, y=0,width=50)
#add a stop button
stop_button = Button(output_tab,text='Stop',command=deinitialize,state=DISABLED)
stop_button.place(relx=0.05,x=325,rely=0.005, y=0,width=50)
#add a resume display button
resume_display_button = Button(output_tab,text='Resume Updates',command=resume_display,state=DISABLED)
resume_display_button.place(relx=0.05,x=400,rely=0.005, y=0,width=100)
#add a pause display button
pause_display_button = Button(output_tab,text='Pause Updates',command=pause_display,state=DISABLED)
pause_display_button.place(relx=0.05,x=500,rely=0.005, y=0,width=100)


#############################################################################################################################################################################
#Second Zone - FLAGS

# Create labels to place text on the GUI to the corresponding flags, also add LEDs for indication and a TOOLTIP for description of flag
# By default all LED are grey

operation_label = Label(output_tab,text="Operation : ",font=myfont)   
operation_label.place(relx=0.50, rely=0.01, y=50, height=30, width=200)
operation_label_led = Led(output_tab, size=20)
operation_label_led.place(relx=0.50, x=250, rely=0.01, y=50, height=30, width=60)
operation_label_led.to_grey()
ToolTip(operation_label_led, 'If lit supply is ON else OFF')

fan_fail_label = Label(output_tab,text="Fan Fail : ",font=myfont)   
fan_fail_label.place(relx=0.50, rely=0.01, y=75, height=30, width=200)
fan_fail_label_led = Led(output_tab, size=20)
fan_fail_label_led.place(relx=0.50, x=250, rely=0.01, y=75, height=30, width=60)
fan_fail_label_led.to_grey()
ToolTip(fan_fail_label_led, 'If lit fan is locked else working normally')

over_temperature_label = Label(output_tab,text="Over Temperature : ",font=myfont)   
over_temperature_label.place(relx=0.50, rely=0.01, y=100, height=30, width=200)
over_temperature_label_led = Led(output_tab, size=20)
over_temperature_label_led.place(relx=0.50, x=250, rely=0.01, y=100, height=30, width=60)
over_temperature_label_led.to_grey()
ToolTip(over_temperature_label_led, 'If lit temperature is abnormal else normal')

dc_over_voltage_label = Label(output_tab,text="DC Over Voltage : ",font=myfont)   
dc_over_voltage_label.place(relx=0.50,rely=0.01, y=125, height=30, width=200)
dc_over_voltage_label_led = Led(output_tab, size=20)
dc_over_voltage_label_led.place(relx=0.50, x=250, rely=0.01, y=125, height=30, width=60)
dc_over_voltage_label_led.to_grey()
ToolTip(dc_over_voltage_label_led, 'If lit dc over voltage is protected else normal')

dc_over_current_label = Label(output_tab,text="DC Over Current : ",font=myfont)   
dc_over_current_label.place(relx=0.50, rely=0.01, y=150, height=30, width=200)
dc_over_current_label_led = Led(output_tab, size=20)
dc_over_current_label_led.place(relx=0.50, x=250, rely=0.01, y=150, height=30, width=60)
dc_over_current_label_led.to_grey()
ToolTip(dc_over_current_label_led, 'If lit dc over current is protected else normal')

short_circuit_label = Label(output_tab,text="Short Circuit : ",font=myfont)   
short_circuit_label.place(relx=0.50, rely=0.01, y=175, height=30, width=200)
short_circuit_label_led = Led(output_tab, size=20)
short_circuit_label_led.place(relx=0.50, x=250, rely=0.01, y=175, height=30, width=60)
short_circuit_label_led.to_grey()
ToolTip(short_circuit_label_led, 'If lit shorted circuit is protected else it does not exist')

ac_fail_label = Label(output_tab,text="AC Fail : ",font=myfont)   
ac_fail_label.place(relx=0.50, rely=0.01, y=200, height=30, width=200)
ac_fail_label_led = Led(output_tab, size=20)
ac_fail_label_led.place(relx=0.50, x=250, rely=0.01, y=200, height=30, width=60)
ac_fail_label_led.to_grey()
ToolTip(ac_fail_label_led, 'If lit AC range is abnormal else normal')

dc_status_label = Label(output_tab,text="DC Status : ",font=myfont)   
dc_status_label.place(relx=0.50, rely=0.01, y=225, height=30, width=200)
dc_status_label_led = Led(output_tab, size=20)
dc_status_label_led.place(relx=0.50, x=250, rely=0.01, y=225, height=30, width=60)
dc_status_label_led.to_grey()
ToolTip(dc_status_label_led, 'If lit DC Status is OFF else ON')

high_temperature_label = Label(output_tab,text="High Temperature : ",font=myfont)   
high_temperature_label.place(relx=0.50, rely=0.01, y=250, height=30, width=200)
high_temperature_label_led = Led(output_tab, size=20)
high_temperature_label_led.place(relx=0.50, x=250,rely=0.01, y=250, height=30, width=60)
high_temperature_label_led.to_grey()
ToolTip(high_temperature_label_led, 'If lit internal temperature is abnormal else normal')

hv_over_voltage_label = Label(output_tab,text="HV Over Voltage : ",font=myfont)   
hv_over_voltage_label.place(relx=0.50,rely=0.01, y=275, height=30, width=200)
hv_over_voltage_label_led = Led(output_tab, size=20)
hv_over_voltage_label_led.place(relx=0.50, x=250, rely=0.01, y=275, height=30, width=60)
hv_over_voltage_label_led.to_grey()
ToolTip(hv_over_voltage_label_led, 'If lit HV over voltage is protected else normal')

device_slave_label = Label(output_tab,text="Is Slave : ",font=myfont)   
device_slave_label.place(relx=0.50,rely=0.01, y=300, height=30, width=200)
device_slave_label_led = Led(output_tab, size=20)
device_slave_label_led.place(relx=0.50, x=250,rely=0.01, y=300, height=30, width=60)
device_slave_label_led.to_grey()
ToolTip(device_slave_label_led, 'If lit supply is a slave')

device_master_label = Label(output_tab,text="Is Master : ",font=myfont)   
device_master_label.place(relx=0.50, rely=0.01, y=325, height=30, width=200)
device_master_label_led = Led(output_tab, size=20)
device_master_label_led.place(relx=0.50, x=250, rely=0.01, y=325, height=30, width=60)
device_master_label_led.to_grey()
ToolTip(device_master_label_led, 'If lit supply is a master')

secondary_dd_output_voltage_label = Label(output_tab,text="Secondary DD Output Voltage : ",font=myfont)   
secondary_dd_output_voltage_label.place(relx=0.50, rely=0.01, y=350, height=30, width=200)
secondary_dd_output_voltage_label_led = Led(output_tab, size=20)
secondary_dd_output_voltage_label_led.place(relx=0.50, x=250, rely=0.01, y=350, height=30, width=60)
secondary_dd_output_voltage_label_led.to_grey()
ToolTip(secondary_dd_output_voltage_label_led, 'If lit Secondary DD output voltage is TOO LOW else NORMAL')

primary_pfc_label = Label(output_tab,text="Primary PFC : ",font=myfont)   
primary_pfc_label.place(relx=0.50, rely=0.01, y=375, height=30, width=200)
primary_pfc_label_led = Led(output_tab, size=20)
primary_pfc_label_led.place(relx=0.50, x=250, rely=0.01, y=375, height=30, width=60)
primary_pfc_label_led.to_grey()
ToolTip(primary_pfc_label_led, 'If lit Primary PFC is OFF else ON')

active_dummy_load_label = Label(output_tab,text="Active Dummy Load : ",font=myfont)   
active_dummy_load_label.place(relx=0.50, rely=0.01, y=400, height=30, width=200)
active_dummy_load_label_led = Led(output_tab, size=20)
active_dummy_load_label_led.place(relx=0.50, x=250, rely=0.01, y=400, height=30, width=60)
active_dummy_load_label_led.to_grey()
ToolTip(active_dummy_load_label_led, 'If lit Active Dummy Load is OFF else ON')

device_initialized_label = Label(output_tab,text="Device Initialized : ",font=myfont)   
device_initialized_label.place(relx=0.50, rely=0.01, y=425, height=30, width=200)
device_initialized_label_led = Led(output_tab, size=20)
device_initialized_label_led.place(relx=0.50, x=250, rely=0.01, y=425, height=30, width=60)
device_initialized_label_led.to_grey()
ToolTip(device_initialized_label_led, 'If green device is intialization state else NOT')

eeprom_data_access_label = Label(output_tab,text="EEPROM Data Access : ",font=myfont)   
eeprom_data_access_label.place(relx=0.50, rely=0.01, y=450, height=30, width=200)
eeprom_data_access_label_led = Led(output_tab, size=20)
eeprom_data_access_label_led.place(relx=0.50, x=250, rely=0.01, y=450, height=30, width=60)
eeprom_data_access_label_led.to_grey()
ToolTip(eeprom_data_access_label_led, 'If lit EEPROM data access error has occured else normal')

direction_ad_label = Label(output_tab,text="Is AC/DC : ",font=myfont)   
direction_ad_label.place(relx=0.50, rely=0.01, y=475, height=30, width=200)
direction_ad_label_led = Led(output_tab, size=20)
direction_ad_label_led.place(relx=0.50, x=250,rely=0.01, y=475, height=30, width=60)
direction_ad_label_led.to_grey()
ToolTip(direction_ad_label_led, 'If lit device is set to AC/DC')

direction_da_label = Label(output_tab,text="Is DC/AC : ",font=myfont)   
direction_da_label.place(relx=0.50, rely=0.01, y=500, height=30, width=200)
direction_da_label_led = Led(output_tab, size=20)
direction_da_label_led.place(relx=0.50, x=250, rely=0.01, y=500, height=30, width=60)
ToolTip(direction_da_label_led, 'If lit device is set to DC/AC')

bidirection_auto_detect_label = Label(output_tab,text="Is Auto-Detect : ",font=myfont)   
bidirection_auto_detect_label.place(relx=0.50, rely=0.01, y=525, height=30, width=200)
bidirection_auto_detect_label_led = Led(output_tab, size=20)
bidirection_auto_detect_label_led.place(relx=0.50, x=250, rely=0.01, y=525 , height=30, width=60)
bidirection_auto_detect_label_led.to_grey()
ToolTip(bidirection_auto_detect_label_led, 'If lit device is set to Auto-Detect mode')

bidirection_battery_label = Label(output_tab,text="Is Battery : ",font=myfont)   
bidirection_battery_label.place(relx=0.50, rely=0.01, y=550, height=30, width=200)
bidirection_battery_label_led = Led(output_tab, size=20)
bidirection_battery_label_led.place(relx=0.50, x=250, rely=0.01, y=550, height=30, width=60)
bidirection_battery_label_led.to_grey()
ToolTip(bidirection_battery_label_led, 'If lit device is set to Battery mode')

#############################################################################################################################################################################
#Third Zone - READINGS

#create String Variables so that they can be later updated live on the GUI, Add labels for text to display the reading as well as its name

input_voltage_val = StringVar()
input_voltage_label = Label(output_tab,text="Input Voltage : ",font=myfont)   
input_voltage_label.place(relx=0.01, rely=0.01, y=50, height=30, width=200)        
input_voltage_val_label = Label(output_tab,text=input_voltage_val.get())  
input_voltage_val_label.place(relx=0.01, x=200, rely=0.01, y=50, height=30, width=75) 

output_voltage_val = StringVar()
output_voltage_label = Label(output_tab,text="Output Voltage : ",font=myfont)   
output_voltage_label.place(relx=0.01, rely=0.01, y=75, height=30, width=200)        
output_voltage_val_label = Label(output_tab,text=output_voltage_val.get())  
output_voltage_val_label.place(relx=0.01, x=200,rely=0.01, y=75, height=30, width=75)    

output_current_val = StringVar()
output_current_label = Label(output_tab,text="Output Current : ",font=myfont)   
output_current_label.place(relx=0.01, rely=0.01, y=100, height=30, width=200)           
output_current_val_label = Label(output_tab,text=output_current_val.get())  
output_current_val_label.place(relx=0.01, x=200, rely=0.01, y=100, height=30, width=75)   

temperature_val = StringVar()
temperature_label = Label(output_tab,text="Temperature : ",font=myfont)   
temperature_label.place(relx=0.01, rely=0.01, y=125, height=30, width=200)           
temperature_val_label = Label(output_tab,text=temperature_val.get())  
temperature_val_label.place(relx=0.01, x=200, rely=0.01, y=125, height=30, width=75)   

set_output_voltage_val = StringVar()
set_output_voltage_label = Label(output_tab,text="Reference Output Voltage : ",font=myfont)   
set_output_voltage_label.place(relx=0.01, rely=0.01, y=150, height=30, width=200)        
set_output_voltage_val_label = Label(output_tab,text=set_output_voltage_val.get())  
set_output_voltage_val_label.place(relx=0.01, x=200,rely=0.01, y=150, height=30, width=75)  

set_output_current_val = StringVar()
set_output_current_label = Label(output_tab,text="Reference Output Current : ",font=myfont)   
set_output_current_label.place(relx=0.01, rely=0.01, y=175, height=30, width=200)        
set_output_current_val_label = Label(output_tab,text=set_output_current_val.get())  
set_output_current_val_label.place(relx=0.01, x=200,rely=0.01, y=175, height=30, width=75)  

set_discharge_voltage_val = StringVar()
set_discharge_voltage_label = Label(output_tab,text="Reference Discharge Voltage : ",font=myfont)   
set_discharge_voltage_label.place(relx=0.01,rely=0.01, y=200, height=30, width=200)        
set_discharge_voltage_val_label = Label(output_tab,text=set_discharge_voltage_val.get())  
set_discharge_voltage_val_label.place(relx=0.01, x=200,rely=0.01, y=200, height=30, width=75)  

set_discharge_current_val = StringVar()
set_discharge_current_label = Label(output_tab,text="Reference Discharge Current : ",font=myfont)   
set_discharge_current_label.place(relx=0.01, rely=0.01, y=225, height=30, width=200)        
set_discharge_current_val_label = Label(output_tab,text=set_discharge_current_val.get())  
set_discharge_current_val_label.place(relx=0.01, x=200,rely=0.01, y=225, height=30, width=75)  


#############################################################################################################################################################################
#Fourth Zone - INPUTAION

#create radio buttons or entry fields for user to select or input data in respectively so that the input can be transmitted to 
# the power supply when the button is clicked (The button here is call Set Reference Button which also needs to be created in this section)

operation_write_val = StringVar()
operation_write_val.set("1")
operation_write_label = Label(output_tab,text="Operation : ",font=myfont)   
operation_write_label.place(relx=0.01, rely=0.51, height=30, width=125)
operation_write_0_radio_button = Radiobutton(output_tab,text="OFF",variable=operation_write_val,value="0",state=DISABLED)
operation_write_1_radio_button = Radiobutton(output_tab,text="ON",variable=operation_write_val,value="1",state=DISABLED)
operation_write_0_radio_button.place(relx=0.01, x=135, rely=0.51)
operation_write_1_radio_button.place(relx=0.01, x=185, rely=0.51)

output_voltage_write_label = Label(output_tab,text="Output Voltage : ",font=myfont) 
output_voltage_write_label.place(relx=0.01, rely=0.51, y=25, height=30, width=125)
output_voltage_write_entry = Entry(output_tab,state=DISABLED)
output_voltage_write_entry.place(relx=0.01, x=135, rely=0.51, y=25, height=20, width=105)
# ToolTip(output_voltage_write_entry, 'Between 38 and 65')
tooltip_label = Label(output_tab,text="( 38V - 65V )")
tooltip_label.place(relx=0.01, x=250, rely=0.51, y=25, height=20)

output_current_write_label = Label(output_tab,text="Output Current : ",font=myfont) 
output_current_write_label.place(relx=0.01, rely=0.51, y=50, height=30, width=125)
output_current_write_entry = Entry(output_tab,state=DISABLED)
output_current_write_entry.place(relx=0.01, x=135, rely=0.51, y=50, height=20, width=105)
# ToolTip(output_current_write_entry, 'Btween 0 and 45')
tooltip_label = Label(output_tab,text="( 0A - 40A )")
tooltip_label.place(relx=0.01, x=250, rely=0.51, y=50, height=20)

discharge_voltage_write_label = Label(output_tab,text="Discharge Voltage : ",font=myfont) 
discharge_voltage_write_label.place(relx=0.01, rely=0.51, y=75, height=30, width=125)
discharge_voltage_write_entry = Entry(output_tab,state=DISABLED)
discharge_voltage_write_entry.place(relx=0.01, x=135, rely=0.51, y=75, height=20, width=105)
# ToolTip(discharge_voltage_write_entry, 'Between 0 and 0')
tooltip_label = Label(output_tab,text="( 38V - 65V )")
tooltip_label.place(relx=0.01, x=250, rely=0.51, y=75, height=20)

discharge_current_write_label = Label(output_tab,text="Discharge Current : ",font=myfont) 
discharge_current_write_label.place(relx=0.01, rely=0.51, y=100, height=30, width=125)
discharge_current_write_entry = Entry(output_tab,state=DISABLED)
discharge_current_write_entry.place(relx=0.01, x=135, rely=0.51, y=100, height=20, width=105)
tooltip_label = Label(output_tab,text="( 0A - 40A )")
tooltip_label.place(relx=0.01, x=250, rely=0.51, y=100, height=20)

set_submit_button = Button(output_tab,text='Set Reference',command=set_submit,state=DISABLED)
set_submit_button.place(relx=0.01,x=110, rely=0.51, y=150)


#############################################################################################################################################################################
#Fifth Zone - MANUFACTURER'S DETAILS

#create String Variables so that they can be later updated live on the GUI, Add labels for text to display the details as well as its name

manufacturer_name_val = StringVar()
manufacturer_name_label = Label(details_tab,text="Manufacturer's Name : ",font=myfont)   
manufacturer_name_label.place(relx=0.01, rely=0.01, y=0, height=30, width=225)        
manufacturer_name_val_label = Label(details_tab,text=manufacturer_name_val.get())  
manufacturer_name_val_label.place(relx=0.01, x=250, rely=0.01, y=0, height=30, width=75) 

manufacturer_model_name_val = StringVar()
manufacturer_model_name_label = Label(details_tab,text="Manufacturer's Model Name : ",font=myfont)   
manufacturer_model_name_label.place(relx=0.01, rely=0.01, y=25, height=30, width=225)        
manufacturer_model_name_val_label = Label(details_tab,text=manufacturer_model_name_val.get())  
manufacturer_model_name_val_label.place(relx=0.01, x=250, rely=0.01, y=25, height=30, width=75) 

firmware_revision_val = StringVar()
firmware_revision_label = Label(details_tab,text="Firmware Revision : ",font=myfont)   
firmware_revision_label.place(relx=0.01, rely=0.01, y=50, height=30, width=225)        
firmware_revision_val_label = Label(details_tab,text=firmware_revision_val.get())  
firmware_revision_val_label.place(relx=0.01, x=250, rely=0.01, y=50, height=30, width=75) 

# manufacturer_factory_location_val = StringVar()
# manufacturer_factory_location_label = Label(details_tab,text="Manufacturer's Factory Location : ",font=myfont)   
# manufacturer_factory_location_label.place(relx=0.01, rely=0.01, y=75, height=30, width=225)        
# manufacturer_factory_location_val_label = Label(details_tab,text=manufacturer_factory_location_val.get())  
# manufacturer_factory_location_val_label.place(relx=0.01, x=250, rely=0.01, y=75, height=30, width=75) 

manufacturer_date_val = StringVar()
manufacturer_date_label = Label(details_tab,text="Manufacturer's Date : ",font=myfont)   
manufacturer_date_label.place(relx=0.01, rely=0.01, y=75, height=30, width=225)        
manufacturer_date_val_label = Label(details_tab,text=manufacturer_date_val.get())  
manufacturer_date_val_label.place(relx=0.01, x=250, rely=0.01, y=75, height=30, width=75) 

product_serial_number_val = StringVar()
product_serial_number_label = Label(details_tab,text="Product Serial Number : ",font=myfont)   
product_serial_number_label.place(relx=0.01, rely=0.01, y=100, height=30, width=225)        
product_serial_number_val_label = Label(details_tab,text=product_serial_number_val.get())  
product_serial_number_val_label.place(relx=0.01, x=250, rely=0.01, y=100, height=30, width=75) 


#############################################################################################################################################################################
#Fifth Zone - MODE INPUTATION

#create radio buttons for user to select so that the input can be transmitted to 
# the power supply when the button is clicked (The button here is call Set Mode Button which also needs to be created in this section)

direction_control_write_val = StringVar()
direction_control_write_val.set("0")
direction_control_write_label = Label(mode_tab,text="Direction Control : ",font=myfont)   
direction_control_write_label.place(relx=0.01, rely=0.01, y=0, height=30, width=120)
direction_control_write_0_radio_button = Radiobutton(mode_tab,text="AC/DC",variable=direction_control_write_val,value="0",state=DISABLED)
direction_control_write_1_radio_button = Radiobutton(mode_tab,text="DC/AC",variable=direction_control_write_val,value="1",state=DISABLED)
direction_control_write_0_radio_button.place(relx=0.01, x=130 ,rely=0.01, y=0)
direction_control_write_1_radio_button.place(relx=0.01, x=225, rely=0.01, y=0)

bidirection_mode_write_val = StringVar()
bidirection_mode_write_val.set("0")
bidirection_mode_write_label = Label(mode_tab,text="Bidirection Mode : ",font=myfont)   
bidirection_mode_write_label.place(relx=0.01, rely=0.01, y=25, height=30, width=120)
bidirection_mode_write_0_radio_button = Radiobutton(mode_tab,text="Auto-Detect",variable=bidirection_mode_write_val,value="0",state=DISABLED)
bidirection_mode_write_1_radio_button = Radiobutton(mode_tab,text="Battery",variable=bidirection_mode_write_val,value="1",state=DISABLED)
bidirection_mode_write_0_radio_button.place(relx=0.01, x=130, rely=0.01, y=25)
bidirection_mode_write_1_radio_button.place(relx=0.01, x=225, rely=0.01, y=25)

mode_submit_button = Button(mode_tab,text='Set Mode',command=mode_submit,state=DISABLED)
mode_submit_button.place(relx=0.01,x=100, rely=0.01, y=75)

#############################################################################################################################################################################

#Start the application and place window on computer screen, listen for events
window.mainloop()              