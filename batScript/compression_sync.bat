@echo off
setlocal enabledelayedexpansion
set "root_dir=D:\Mi Camera Videos\xiaomi_camera_videos"
set "clone_dir=D:\Mi Camera Videos\compressed\xiaomi_camera_videos"

set "crf=40"
if not exist "%clone_dir%" mkdir "%clone_dir%"
for /R "%root_dir%" %%f in (*.mp4 *.avi) do (
    set "file=%%f"
    set "rel_path=!file:%root_dir%=!"
    set "compressed_file=%clone_dir%!rel_path!"
    set "compressed_dir=%clone_dir%!rel_path:%[^].mp4=!"

    if not exist "!compressed_file:=_compressed.mp4!" (
        if not exist "!compressed_dir!" mkdir "!compressed_dir!" 
        echo Compressing !file!
        ffmpeg -y -i "!file!" -vcodec h264 -acodec aac -strict -2 -crf !crf! "!compressed_file:.mp4=_compressed.mp4!"
        aws s3 sync "%clone_dir%" s3://ftmg-camera-videos/Dwarka-Office/
        for /f "delims=" %%d in ('dir "%clone_dir%" /s /b /ad ^| sort /r') do rd "%%d"

    
    )
)
for /R "%clone_dir%" %%f in (*_compressed.mp4) do (
    set "compressed_file=%%f"y
    set "rel_path=!compressed_file:%clone_dir%=!"
    set "file=%root_dir%!rel_path:_compressed.mp4=.mp4!"

    if not exist "!file!" (
        echo Deleting !compressed_file!
        del "!compressed_file!"
    )
)
for /R "%clone_dir%" %%d in (*) do (
    if not exist "%%d*" rd /s /q "%%d"
)
@REM for /f "delims=" %%d in ('dir "%clone_dir%" /s /b /ad ^| sort /r') do rd "%%d"
echo All videos are processed successfully.
@REM aws s3 sync "%clone_dir%" s3://ftmg-camera-videos/Dwarka-Office/
echo All videos sync successfully.

