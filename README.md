# PROFino
A simple *live-profiler* for Arduino, **PROFino** provides infos about the time spend on each called function, as well as the numbers of calls itself. **PROFino** can be used on terminal or on it's GUI.
* PROFino CLI (Command Line Interface):

![PROFino CLI](https://i.imgur.com/hFLFDFP.png)

* PROFino GUI (Graphical User Interface):

![PROFino GUI](https://i.imgur.com/sB93Moa.png)

After the profiling via GUI stops, a graph with the collected data is displayed.

![Graph](https://i.imgur.com/lMkpIHy.png)


# Dependencies
* [avr-libc](https://www.nongnu.org/avr-libc/) ```apt install avr-libc```
* [avrdude](https://www.nongnu.org/avrdude/) ```apt install avrdude```
* [ctags-universal](https://github.com/universal-ctags/ctags) ```apt install universal-ctags```
* [pyserial](https://pypi.org/project/pyserial/) - ```pip install pyserial```

# Usage 
```
-h --help           Displays help.
-c --source         Path to source code.
-p --port           USB port where the Arduino is connected, Ex: /dev/ttyACM0, /dev/ttyUSB0.
-g --graphic        Flag that indicates if the program must run in GUI mode.
```
Example: `./PROFino.py -c source.c -p /dev/ttyXXXX` or `python PROFino.py -c source.c -p /dev/ttyXXXX`

## //TODO:
- [x] Create basic project structure
- [x] Serial communication
- [x] Define communication protocol
- [x] Implement communication protocol
- [x] Test communication protocol
- [x] Define instrumentation aproach
- [x] Instrument the code
- [x] Collect execution data
- [x] User interface
- [x] Displays data in graphics
