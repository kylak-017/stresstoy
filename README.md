# Arduino Joystick Destress Activity Selector

A hardware-software system that uses an Arduino joystick to select destressing activities based on your energy level, available time, and location preference. The system uses rule-based suggestions to recommend personalized activities.

## Components

- **Arduino Sketch** (`arduino_joystick.ino`): Reads joystick input and sends binary data via Serial
- **Python Script** (`script.py`): Communicates with Arduino and triggers activity suggestions
- **Activity Suggester** (`model.py`): Suggests personalized destressing activities based on inputs

## Hardware Requirements

- Arduino board (Uno, Nano, or compatible)
- Analog joystick module (2-axis with button)
- Jumper wires
- USB cable to connect Arduino to computer

## Hardware Connections

Connect the joystick to Arduino:

- **Joystick X-axis** → A0 (for inside/outside selection)
- **Joystick Y-axis** → A1 (for energy level selection)
- **Joystick VCC** → 5V
- **Joystick GND** → GND
- **Joystick Button** → D2 (with pull-up resistor)

## Software Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Upload Arduino Sketch

1. Open `arduino_joystick.ino` in Arduino IDE
2. Select your board (Tools → Board → Arduino Uno/Nano)
3. Select the correct port (Tools → Port)
4. Upload the sketch

## Usage

### Running the Python Script

#### Automatic Port Detection (Recommended)
```bash
python script.py
```

#### Manual Port Specification
```bash
# On Mac/Linux:
python script.py --port /dev/cu.usbmodem*

# On Windows:
python script.py --port COM3

# On Linux:
python script.py --port /dev/ttyUSB0
```

### Using the Joystick

The joystick controls three inputs:

1. **Energy Level** (Y-axis):
   - **Up/Right** = High energy
   - **Down/Left** = Low energy

2. **Time Available** (Button):
   - **Pressed** = +5 minutes available
   - **Not Pressed** = <5 minutes available

3. **Location** (X-axis):
   - **Right** = Outside preferred
   - **Left** = Inside preferred

Move the joystick and press the button to select your preferences. The system will suggest a destressing activity based on your inputs.

## Binary Data Format

The Arduino sends a single byte with the following bit encoding:

- **Bit 0**: Energy level (1=high, 0=low)
- **Bit 1**: Time available (1=+5min, 0=<5min)
- **Bit 2**: Location (1=outside, 0=inside)

Example: `0b110` (binary 110) means:
- High energy (bit 0 = 1)
- +5 minutes available (bit 1 = 1)
- Inside location (bit 2 = 0)

## Troubleshooting

### Arduino Not Found
- Check USB connection
- Verify Arduino drivers are installed
- Try manually specifying the port with `--port` flag

### Serial Communication Errors
- Ensure Arduino is connected before running Python script
- Check that baudrate matches (default: 9600)
- Try resetting the Arduino

### Joystick Not Responding
- Verify wiring connections
- Check that joystick is receiving power (5V)
- Test joystick with Arduino Serial Monitor


## Example Output

```
============================================================
Current Input:
  Energy: high
  Time: +5min
  Location: outside

Suggested Activity:
  Go for a brisk walk or jog
  Get your heart rate up and enjoy the fresh air
============================================================
```

## Files

- `arduino_joystick.ino` - Arduino sketch for joystick input
- `script.py` - Main Python script for Arduino communication
- `model.py` - Activity suggester for rule-based activity suggestions
- `requirements.txt` - Python dependencies

## License

This project is provided as-is for personal use.
