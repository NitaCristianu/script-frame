import numpy as np
import threading
from config.projectData import *
from config.consts import *
from classes.components.mains.MainEditorComponents.Videoplayer import *
from classes.components.core.Rect import *
from classes.components.core.Text import *
from moviepy.editor import ImageSequenceClip, AudioClip

fps = 30


class RenderMode(Rect):
    def __init__(self, dimension: tuple[int, int, int, int] = (0, 0, '1x', '1y'), app: any = None, color: str | tuple[int, int, int, int] = "#0e0e0e00", borderRadius=0, detectHover=False, onHoverModifiedColor=0.15) -> None:
        super().__init__(dimension, app, color, borderRadius,
                         detectHover, onHoverModifiedColor)

        ends = tuple(el.end for el in elements)
        n_frames = int(max(ends) * 1000 / fps)
        self.frm = pg.Surface((0, 0))
        self.add_child(Rect(
            dimension=(0, 0, '1x', '1y'),
            app=app,
            color="#000000d0",


        ))
        self.add_child(Text(
            dimension=(0, '0.1y', '1x', '1y'),
            autoHeight=True,
            app=self.app,
            text=f"RENDERING : 0 / {n_frames}",
            weight="light",
            fontHeight=20
        ))
        self.add_child(Text(
            dimension=(0, '0.1y + 25', '1x', '1y'),
            autoHeight=True,
            app=self.app,
            text=f"press ESC to cancel",
            weight="light",
            fontHeight=14
        ))
        self.app.event.add_listener(RENDER_VIDEO, lambda: self.render())

    def draw(self):
        if not self.enabled:
            return
        transformed = pg.transform.scale(self.frm, (self.w//2, self.h//2))
        self.app.screen.blit(transformed, (self.w//4, self.h//4))
        super().draw()

    def render(self):

        # AUDIO RENDER
        totalsounds = [
            *((element.pygamesound, element.start)
              for element in elements if element.type == 'audio'),
        ]
        for element in (element for element in elements if element.type == 'video'):
            sounds = element.instance.sounds
            for sound in sounds:
                totalsounds.append((sound[0], sound[1] + element.start))

        sample_rate = 44100
        max_len = 0

        for sound, start_time in totalsounds:
            sound_array = pygame.sndarray.array(sound)
            start_samples = int(sample_rate * start_time)
            max_len = max(max_len, start_samples + len(sound_array))

        mixed_array = np.zeros((max_len, 2), dtype=np.int16)

        for sound, start_time in totalsounds:
            sound_array = pygame.sndarray.array(sound)

            # Ensure the sound is stereo (two channels)
            if sound_array.ndim == 1:  # Mono sound
                sound_array = np.stack((sound_array, sound_array), axis=-1)

            start_samples = int(sample_rate * start_time)
            mixed_array[start_samples:start_samples +
                        len(sound_array)] += sound_array

        max_val = np.max(np.abs(mixed_array))
        if max_val:
            mixed_array = (mixed_array / max_val) * 32767
            mixed_array = mixed_array.astype(np.int16)

        mixed_audio = mixed_array.astype(np.float32) / 32768.0
        duration = len(mixed_audio) / sample_rate

        def make_frame(t: np.ndarray | int):
            if isinstance(t, np.ndarray):
                # Handle the case where t is a numpy array (vectorized)
                indices = (t * sample_rate).astype(int)
                # Ensure indices are within bounds
                indices = np.clip(indices, 0, len(mixed_audio) - 1)
                return mixed_audio[indices]  # Return the array of samples
            else:
                # Handle the scalar case
                index = int(t * sample_rate)
                if index < len(mixed_audio):
                    return tuple(mixed_audio[index])
                else:
                    return (0.0, 0.0)

        # VIDEO RENDER
        n_frames = int(max(tuple(el.end for el in elements)) * 1000 / fps)
        frames = []
        self.children[2].text = "press ESC to cancel"
        for index in range(n_frames):
            events = pg.event.get()
            if next(iter(ev for ev in events if ev.type == pg.KEYDOWN and ev.key == pg.K_ESCAPE), None):
                self.app.setWindowMode(0)
                return

            self.frm = renderFrame((1600, 900), index*fps)

            array = pg.surfarray.array3d(self.frm)
            array = np.transpose(array, (0, 1, 2))
            array = np.flipud(array)
            array = np.rot90(array, k=-1)

            self.children[1].text = f"Frame : {index} / {n_frames-1}"
            self.draw()
            self.app.refresh()
            frames.append(array)
        self.children[1].text = f"WRITING FILE"
        self.children[2].text = ""
        self.draw()
        self.app.refresh()

        clip = ImageSequenceClip(frames, fps=fps)
        audio_clip = AudioClip(make_frame=make_frame,
                               duration=duration, fps=sample_rate)
        clip.audio = audio_clip.subclip(0, clip.duration)
        clip.write_videofile("output.mp4", codec="libx264", audio_codec="aac")
        self.app.setWindowMode(0)
