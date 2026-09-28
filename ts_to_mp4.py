from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def find_input_files(input_path: Path) -> list[Path]:
    if input_path.is_file():
        return [input_path]
    if input_path.is_dir():
        return sorted(path for path in input_path.glob("*.ts") if path.is_file())
    raise FileNotFoundError(f"Khong tim thay tep hoac thu muc: {input_path}")


def convert_one(input_path: Path, overwrite: bool = False) -> Path:
    output_path = input_path.with_suffix(".mp4")
    if output_path.exists() and not overwrite:
        raise FileExistsError(
            f"Tep dau ra da ton tai: {output_path}. Dung --overwrite de ghi de."
        )

    temporary_path = output_path.with_name(f".{output_path.name}.part")
    if temporary_path.exists():
        temporary_path.unlink()

    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-i",
        str(input_path),
        "-map",
        "0",
        "-c",
        "copy",
        "-bsf:a",
        "aac_adtstoasc",
        "-movflags",
        "+faststart",
        "-f",
        "mp4",
        str(temporary_path),
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode != 0:
            command_without_filter = [
                item for item in command if item not in ("-bsf:a", "aac_adtstoasc")
            ]
            result = subprocess.run(
                command_without_filter,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
        if result.returncode != 0:
            message = (result.stderr or "").strip() or "FFmpeg khong the chuyen tep."
            raise RuntimeError(message)

        os.replace(temporary_path, output_path)
        return output_path
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def convert_files(files: list[Path], workers: int, overwrite: bool) -> int:
    failed = 0
    with ThreadPoolExecutor(max_workers=workers) as executor:
        jobs = {
            executor.submit(convert_one, path, overwrite): path for path in files
        }
        for job in as_completed(jobs):
            input_path = jobs[job]
            try:
                print(f"Da tao: {job.result()}")
            except Exception as error:
                failed += 1
                print(f"Loi [{input_path}]: {error}", file=sys.stderr)
    return failed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Doi video .ts sang .mp4, giu nguyen chat luong bang remux."
    )
    parser.add_argument("input", type=Path, help="Tep .ts hoac thu muc chua cac tep .ts")
    parser.add_argument(
        "--workers",
        type=int,
        default=min(4, os.cpu_count() or 1),
        help="So tep xu ly dong thoi khi input la thu muc (mac dinh: 4).",
    )
    parser.add_argument(
        "--overwrite", action="store_true", help="Ghi de tep .mp4 da ton tai."
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if shutil.which("ffmpeg") is None:
        print(
            "Khong tim thay FFmpeg. Cai FFmpeg va them ffmpeg.exe vao PATH.",
            file=sys.stderr,
        )
        return 1
    if args.workers < 1:
        print("--workers phai lon hon hoac bang 1.", file=sys.stderr)
        return 1

    try:
        files = find_input_files(args.input)
    except FileNotFoundError as error:
        print(error, file=sys.stderr)
        return 1
    if not files:
        print(f"Khong tim thay tep .ts trong: {args.input}", file=sys.stderr)
        return 1

    print(f"Dang xu ly {len(files)} tep voi {args.workers} worker...")
    return min(convert_files(files, args.workers, args.overwrite), 1)


if __name__ == "__main__":
    raise SystemExit(main())