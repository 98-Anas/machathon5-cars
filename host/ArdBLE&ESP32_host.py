import asyncio
from bleak import BleakScanner, BleakClient
import keyboard
import cv2
import numpy as np
import urllib.request

command_char_uuid = "00001142-0000-1000-8000-00805f9b34fb"

# Function to control the car based on keyboard input
async def run_ble_client(device_address: str):
    async with BleakClient(device_address) as client:
        if client.is_connected:
            print(f"Connected to {device_address}")
            print("Control the car: \nW/S: Accelerate/Decelerate\nA/D: Turn Left/Right\nESC: Quit")
            while True:
                command = None
                if keyboard.is_pressed('esc'):
                    print("Quitting...")
                    break
                if keyboard.is_pressed('w'):
                    command = b'W'
                    print("Forward")
                elif keyboard.is_pressed('s'):
                    command = b'S'
                    print("Backward")
                if keyboard.is_pressed('a'):
                    command = b'A'
                    print("Left")
                elif keyboard.is_pressed('d'):
                    command = b'D'
                    print("Right")
                elif not any([keyboard.is_pressed(key) for key in ['w', 's', 'a', 'd']]):
                    command = b'N'  # Neutral command to stop and center
                    print("Neutral")
                
                if command:
                    await client.write_gatt_char(command_char_uuid, command)
                await asyncio.sleep(0.1)

# Discover BLE devices
async def discover_device(target_device_name: str):
    devices = await BleakScanner.discover()
    for device in devices:
        if device.name and target_device_name.lower() in device.name.lower():
            print(f"Found target device: {device.name}, Address: {device.address}")
            return device.address
    return None

# Connect to RC car and control it
async def connect_and_control_rc_car(target_device_name: str):
    device_address = await discover_device(target_device_name)
    if device_address:
        await run_ble_client(device_address)
    else:
        print("Target device not found.")

# Function to process and display video stream from ESP32-CAM
def process_video_stream(esp32_cam_url: str):
    # Placeholder for the video capture creation
    cap = cv2.VideoCapture(esp32_cam_url)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame")
            break

        # PLACE YOUR ALGORITHM HERE
        # This is where competitors will implement their algorithms.
        # For example, to apply a lane detection algorithm on the 'frame' variable.
        # processed_frame = your_algorithm_here(frame)
        # For demonstration, we will just show the original frame.
        processed_frame = frame  # This line should be replaced with your processing

        # Display the processed frame
        cv2.imshow('Processed Frame', processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    target_device_name = "Car 3"  # Name of the BLE device (Arduino)
    esp32_cam_url = "http://your_esp32_cam_stream_url"  # ESP32-CAM video stream URL

    # Running car control and video stream processing concurrently requires a threading or async mechanism.
    # For simplicity, the following line is commented. You should integrate it according to your application's architecture.
    # Example: asyncio.run(connect_and_control_rc_car(target_device_name))

    # Start processing video stream
    process_video_stream(esp32_cam_url)
