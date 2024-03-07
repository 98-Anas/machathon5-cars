import asyncio
from bleak import BleakScanner, BleakClient
import keyboard  # Make sure to install this library first

command_char_uuid = "00001142-0000-1000-8000-00805f9b34fb"

async def run_ble_client(device_address: str):
    async with BleakClient(device_address) as client:
        if client.is_connected:
            print(f"Connected to {device_address}")
            print("Control the car: \nW/S: Accelerate/Decelerate\nA/D: Turn Left/Right\nESC: Quit")
            while True:
                await asyncio.sleep(0.1)  # Prevents the loop from using too much CPU
                if keyboard.is_pressed('esc'):  # Quit if ESC is pressed
                    print("Quitting...")
                    break
                elif keyboard.is_pressed('w'):
                    await client.write_gatt_char(command_char_uuid, b'W')
                    print("Forward")
                    while keyboard.is_pressed('w'):  # Wait for key release
                        await asyncio.sleep(0.1)
                elif keyboard.is_pressed('s'):
                    await client.write_gatt_char(command_char_uuid, b'S')
                    print("Backward")
                    while keyboard.is_pressed('s'):
                        await asyncio.sleep(0.1)
                elif keyboard.is_pressed('a'):
                    await client.write_gatt_char(command_char_uuid, b'A')
                    print("Left")
                    while keyboard.is_pressed('a'):
                        await asyncio.sleep(0.1)
                elif keyboard.is_pressed('d'):
                    await client.write_gatt_char(command_char_uuid, b'D')
                    print("Right")
                    while keyboard.is_pressed('d'):
                        await asyncio.sleep(0.1)

async def discover_device(target_device_name: str):
    devices = await BleakScanner.discover()
    for device in devices:
        if device.name and target_device_name.lower() in device.name.lower():
            print(f"Found target device: {device.name}, Address: {device.address}")
            return device.address
    return None

async def connect_and_control_rc_car(target_device_name: str):
    device_address = await discover_device(target_device_name)
    if device_address:
        await run_ble_client(device_address)
    else:
        print("Target device not found.")

if __name__ == "__main__":
    target_device_name = "Car 3"  # Name of the BLE device (Arduino)
    asyncio.run(connect_and_control_rc_car(target_device_name))
