import wave
import sys
import math

def read_wav(path, downsample_factor = 10):
    with wave.open(path, "rb") as wav:
        nchannels, sampwidth, framerate, nframes, _, _ = wav.getparams()

        signed = sampwidth > 1  # 8 bit wavs are unsigned
        byteorder = sys.byteorder  # wave module uses sys.byteorder for bytes

        values = []  # e.g. for stereo, values[i] = [left_val, right_val]
        maxval = -9999999999999
        for _ in range(nframes):
            frame = wav.readframes(1)  # read next frame
            channel_vals = []  # mono has 1 channel, stereo 2, etc.
            for channel in range(nchannels):
                as_bytes = frame[channel * sampwidth: (channel + 1) * sampwidth]
                as_int = int.from_bytes(as_bytes, byteorder, signed=signed)
                if as_int > maxval: maxval = as_int
                channel_vals.append(as_int)
            values.append(channel_vals)

        for i, val in enumerate(values):
            for j, chan in enumerate(val):
                values[i][j] /= maxval

    return values, framerate