import os
import sys

from moviepy import VideoFileClip


def split_video_into_two(input_path):
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"File khong ton tai: {input_path}")

    base, ext = os.path.splitext(input_path)
    part1_path = f"{base}_part1{ext}"
    part2_path = f"{base}_part2{ext}"

    with VideoFileClip(input_path) as clip:
        total = clip.duration
        midpoint = total / 2
        print(f"Tong thoi luong: {total:.2f}s, chia tai: {midpoint:.2f}s")

        export_options = {
            "codec": "h264_nvenc",
            "audio_codec": "aac",
            "ffmpeg_params": ["-preset", "p4"],
        }
        clip.subclipped(0, midpoint).write_videofile(part1_path, **export_options)
        clip.subclipped(midpoint, total).write_videofile(part2_path, **export_options)

    print(f"Da tao:\n  {part1_path}\n  {part2_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Cach dung: python split_video.py <duong-dan-video>")
        sys.exit(1)
    split_video_into_two(sys.argv[1])