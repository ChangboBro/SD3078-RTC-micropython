# SD3078-RTC-micropython

A simple micropython file for driving SD3078, a Real Time Chip (RTC) with Digital Temperature Compensation Crystal Oscillator integrated inside, functions with I2C bus. The frequency accuracy is supposed to be $\le$3.8ppm at 25$^{\circ}C$.

This code is only tested with RaspberryPi Pico. And have no warrenty for any usage.

`settime.py` demonstrates how to set time to the RTC, `readtime.py` demonstrates how to read out the time, temperature, backup battery voltage from the RTC.
