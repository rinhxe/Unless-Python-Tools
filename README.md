# Unless Python Tools

A collection of command-line tools for converting and editing video files.

## Requirements

- Python 3.10 or newer
- FFmpeg available on `PATH` for `ts_to_mp4.py`
- An NVIDIA GPU with NVENC support for `split_video.py`

The Python package dependencies are listed in [`requirements.txt`](requirements.txt). Install them in a virtual environment from the repository root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks virtual-environment activation, run the commands with the environment's Python executable directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

`ts_to_mp4.py` uses only the Python standard library. It requires the FFmpeg command-line program separately; verify it is available with `ffmpeg -version`.

## Tools

| File | Python requirements | External requirements | Purpose |
| --- | --- | --- | --- |
| `ts_to_mp4.py` | Python standard library | FFmpeg on `PATH` | Remux one `.ts` file or every `.ts` file in a directory to `.mp4` without re-encoding |
| `split_video.py` | `moviepy` from `requirements.txt` | FFmpeg build with `h264_nvenc` and a compatible NVIDIA GPU/driver | Split a video into two equal-duration parts |
| `speed_up_video.py` | `moviepy` from `requirements.txt` | None beyond MoviePy's FFmpeg support | Speed up a video and save a new copy |

## Usage

Run commands from the repository root after activating the virtual environment.

### Convert MPEG-TS to MP4

Convert one file:

```powershell
python .\ts_to_mp4.py .\input.ts
```

Convert all `.ts` files in a directory with up to four workers:

```powershell
python .\ts_to_mp4.py .\videos
```

Choose the number of concurrent conversions or overwrite existing output files:

```powershell
python .\ts_to_mp4.py .\videos --workers 2 --overwrite
```

Each output is written next to its input using the `.mp4` extension. The command exits with a nonzero status if any input fails.

### Split a video in half

```powershell
python .\split_video.py .\input.mp4
```

The script creates `input_part1.mp4` and `input_part2.mp4` next to the source. It encodes with NVIDIA NVENC (`h264_nvenc`), so FFmpeg must include that encoder and a compatible NVIDIA GPU and driver must be available.

### Speed up a video

Use the default 2x speed:

```powershell
python .\speed_up_video.py .\input.mp4
```

Set a different speed factor:

```powershell
python .\speed_up_video.py .\input.mp4 1.5
```

The script creates `input_2.0x.mp4` by default; the output name includes the selected factor.

## Adding dependencies

Add third-party Python packages to `requirements.txt`, one package per line, then install the updated dependencies with:

```powershell
python -m pip install -r requirements.txt
```

Keep imports in the script that uses each dependency. If a script needs a non-Python executable, document it in that tool's external requirements and make sure the executable is available on `PATH` instead of adding it to `requirements.txt`.
