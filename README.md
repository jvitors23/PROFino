# PROFino
A simple profiler for Arduino.

# Dependencies
* [avr-libc](https://www.nongnu.org/avr-libc/) ```apt install avr-libc```
* [avrdude](https://www.nongnu.org/avrdude/) ```apt install avrdude```
* [ctags-universal](https://github.com/universal-ctags/ctags) ```apt install universal-ctags```
* [pyserial](https://pypi.org/project/pyserial/) - ```pip install pyserial```

# Usage 

```./PROFino.py -c source.c -p /dev/ttyXXX```

or

```python PROFino.py -c source.c -p /dev/ttyXXX```

## //TODO:
- [x] Create basic project structure
- [x] Serial communication
- [x] Define communication protocol
- [x] Implement communication protocol
- [x] Test communication protocol
- [x] Define instrumentation aproach
- [x] Instrument the code
- [x] Collect execution data
- [ ] User interface
- [ ] ...
