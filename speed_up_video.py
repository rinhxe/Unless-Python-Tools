import os
import sys

if sys.platform == "win32" and not sys.flags.utf8_mode:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from moviepy import VideoFileClip, vfx


def speed_up_video(input_path, factor=2.0):
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"File khong ton tai: {input_path}")

    base, ext = os.path.splitext(input_path)
    output_path = f"{base}_{factor}x{ext}"

    with VideoFileClip(input_path) as clip:
        print(f"Thoi luong goc: {clip.duration:.2f}s, toc do x{factor}")
        clip = clip.with_effects([vfx.MultiplySpeed(factor)])
        clip.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            ffmpeg_params=["-crf", "28"],
        )

    print(f"Da tao: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Cach dung: python speed_up_video.py <duong-dan-video> [he-so-toc-do=2]")
        sys.exit(1)
    factor = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
    speed_up_video(sys.argv[1], factor)