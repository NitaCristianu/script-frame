import inspect
import wave
import sys
import math
import numpy as np
from io import BytesIO


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

def splitaudio(sound_array : np.ndarray, framerate: int, nchannels : int, sampwidth : float, split_time_sec):
    sound_array = sound_array.reshape(-1, nchannels)

    split_frame = int(framerate * split_time_sec)

    print("spliting time:" , round(split_time_sec, 2))
    print("spliting frame", split_frame)
    print("lenght", len(sound_array))
    print("---------")
    part1_array = sound_array[:split_frame]
    part2_array = sound_array[split_frame:]
    a = len(part1_array)
    b = len(part2_array)
    c = len(sound_array)
    print("a", a, "seconds:", a/framerate)
    print("b", b, "seconds:", b/framerate)
    print("c", c, "seconds:", c/framerate)
    print("---------")
    print("a + b", a + b)
    print("a%", a / c)
    print("b%", b / c)

    # Step 3: Convert both parts into in-memory WAV files
    def array_to_wav_file(array, *params):
        wav_data = BytesIO()
        with wave.open(wav_data, "wb") as wav_file:
            wav_file.setnchannels(params[0])
            wav_file.setsampwidth(params[1])
            wav_file.setframerate(params[2])
            wav_file.setnframes(params[3])
            # Flatten the array back to 1D before writing
            wav_file.writeframes(array.flatten().tobytes())

        wav_data.seek(0)  # Reset the pointer to the beginning
        
        return wav_file, wav_data

    params = (nchannels, sampwidth, framerate)
    part1_wav = array_to_wav_file(part1_array, *params, a)
    part2_wav = array_to_wav_file(part2_array, *params, b)
    print("X")

    return part1_wav, part2_wav
