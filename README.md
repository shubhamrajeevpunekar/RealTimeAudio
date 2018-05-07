# Realtime Audio with pyaudio#

- install alsa-utils, it bundles alsamixer, arecord and aplay
- add user to "audio" group (may be required, if alsamixer is to be used as remote user)

- To display list of devices that can be used for recording
    arecord --list-devices
    Here, note the "card number" and "device number" -> usually, "hw:2,0"
    NOTE : To open a stream, select the device that has "hw:2,0" in its 'name' parameter, when queried with pyaudio object's get_device_info_by_index() method

- To set mic levels, use *alsamixer.* In alsamixer : 
    - F6 - select sound card
    - F4 - capture device
    - Set the mic input here, if the input is too noisy
    - ESC to exit, settings are saved

- To record,
    arecord -f S16_LE -c 1 -r 16000 -D hw:<card number>,<device number> -d 5 test.wav
    - f : specifies format, S16_LE is 16-bit little endian
    - c : channels, set to 1
    - -r : specifies sampling rate
    - D hw:2,0 : specifies the device, for USB camera, it usually is card 2, device 0
    - -d : delay, audio file length

- To play
    aplay test.wav

- Forsome reason, output playback is not working for device set to "pulse", just test the audio with aplay
- The recorded audio is correct, both numpy arrays -> recording and playback are same