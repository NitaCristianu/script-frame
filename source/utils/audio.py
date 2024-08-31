import wave
import sys
import numpy as np
from io import BytesIO

def read_wav(path):
    with wave.open(path, "rb") as wav:
        nchannels, sampwidth, framerate, nframes, _, _ = wav.getparams()

        signed = sampwidth > 1  # 8-bit WAVs are unsigned
        byteorder = sys.byteorder  # wave module uses sys.byteorder for bytes

        # Preallocate list for efficiency
        values = [None] * nframes  
        maxval = -float('inf')

        # Read all frames at once for faster processing
        frames = wav.readframes(nframes)

        for i in range(nframes):
            frame_start = i * sampwidth * nchannels
            channel_vals = [None] * nchannels
            for channel in range(nchannels):
                as_bytes = frames[frame_start + channel * sampwidth: frame_start + (channel + 1) * sampwidth]
                as_int = int.from_bytes(as_bytes, byteorder, signed=signed)
                if as_int > maxval: maxval = as_int
                channel_vals[channel] = as_int
            values[i] = channel_vals

        # Normalize in-place
        maxval = float(maxval)
        for val in values:
            for j in range(nchannels):
                val[j] /= maxval

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
