import serial
import serial.tools.list_ports
import time
from model import ActivitySuggester


class ArduinoReader:
    
    def __init__(self, port=None, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.serial_conn = None
        self.activity_suggester = ActivitySuggester()
        self.last_byte = None
        self.last_suggestion_time = 0
        self.suggestion_cooldown = 2
    
    def find_arduino_port(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if any(keyword in port.description.lower() for keyword in 
                   ['arduino', 'usb serial', 'ch340', 'ft232', 'cp210']):
                return port.device
        return None
    
    def connect(self):
        if not self.port:
            print("Searching for Arduino...")
            self.port = self.find_arduino_port()
            if not self.port:
                print("Could not find Arduino automatically.")
                print("Available ports:")
                ports = serial.tools.list_ports.comports()
                for port in ports:
                    print(f"  - {port.device}: {port.description}")
                return False
        
        try:
            print(f"Connecting to Arduino on {self.port}...")
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=1
            )
            time.sleep(2)
            print("Connected successfully!")
            return True
        except serial.SerialException as e:
            print(f"Error connecting to Arduino: {e}")
            return False
    
    def parse_byte(self, byte):
        energy_bit = (byte >> 0) & 1
        time_bit = (byte >> 1) & 1
        location_bit = (byte >> 2) & 1
        
        return {
            "energy": "high" if energy_bit else "low",
            "time": "+5min" if time_bit else "<5min",
            "location": "outside" if location_bit else "inside"
        }
    
    def read_and_process(self):
        if not self.serial_conn or not self.serial_conn.in_waiting:
            return None
        
        try:
            byte = ord(self.serial_conn.read(1))
            
            current_time = time.time()
            if byte != self.last_byte or (current_time - self.last_suggestion_time) >= self.suggestion_cooldown:
                self.last_byte = byte
                self.last_suggestion_time = current_time
                
                inputs = self.parse_byte(byte)
                suggestion = self.activity_suggester.suggest_activity(
                    inputs["energy"],
                    inputs["time"],
                    inputs["location"]
                )
                
                return {
                    "inputs": inputs,
                    "suggestion": suggestion,
                    "raw_byte": byte
                }
        except Exception as e:
            print(f"Error reading from Arduino: {e}")
            return None
        
        return None
    
    def run_loop(self):
        if not self.connect():
            print("\nTo connect manually, run:")
            print("python script.py --port <PORT_NAME>")
            return
        
        print("\nReading joystick input...")
        print("Controls:")
        print("  - Joystick Y-axis: Energy level (up=high, down=low)")
        print("  - Joystick X-axis: Location (right=outside, left=inside)")
        print("  - Button: Time available (pressed=+5min, not pressed=<5min)")
        print("\nPress Ctrl+C to exit\n")
        
        try:
            while True:
                result = self.read_and_process()
                if result:
                    print("\n" + "="*60)
                    print("Current Input:")
                    print(f"  Energy: {result['inputs']['energy']}")
                    print(f"  Time: {result['inputs']['time']}")
                    print(f"  Location: {result['inputs']['location']}")
                    print(f"\nSuggested Activity:")
                    print(f"  {result['suggestion']['activity']}")
                    print(f"  {result['suggestion']['description']}")
                    print("="*60 + "\n")
                
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n\nExiting...")
        finally:
            if self.serial_conn:
                self.serial_conn.close()
                print("Serial connection closed.")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Arduino Joystick Destress Activity Selector')
    parser.add_argument('--port', help='Serial port name (e.g., COM3, /dev/ttyUSB0, /dev/cu.usbmodem*)')
    parser.add_argument('--baudrate', default=9600, help='Serial baudrate (default: 9600)')
    
    args = parser.parse_args()
    
    reader = ArduinoReader(port=args.port, baudrate=args.baudrate)
    reader.run_loop()


if __name__ == "__main__":
    main()
