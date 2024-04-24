import subprocess

def get_usb_devices():
    lsusb_output = subprocess.check_output("lsusb").decode("utf-8")
    usb_devices = []

    for line in lsusb_output.split('\n'):
        usb_devices.append(line)

    return usb_devices

def get_usb_port_index(device_name):
    lsusb_output = subprocess.check_output("lsusb").decode("utf-8")

    for line in lsusb_output.split('\n'):
        if device_name in line:
          
            index = int(line.split()[1])
            return index

    
    return None

def main():
    usb_devices = get_usb_devices()

    
    for index, device_info in enumerate(usb_devices):
        print(f"Index USB-port {index}: {device_info}")


    #device_name = "GEMBIRD Generic UVC 1.00 camera [AppoTech AX2311]"
    device_name = "Microsoft Corp. LifeCam VX-500 [1357]"
    port_index = get_usb_port_index(device_name)

    if port_index is not None:
        print(f"Index USB-port for device '{device_name}': {port_index}")
    else:
        print(f"Device '{device_name}' not find.")

if __name__ == "__main__":
    main()
