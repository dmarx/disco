del *.png
del *.mp4

copy \\wsl.localhost\Ubuntu-20.04\home\twmmason\dev\disco\content\images_out\TimeToDisco\*.png C:\Users\twmma\OneDrive\Desktop\ArtTemp
# forfiles /S /M *.png /C "cmd /c rename @file Work@file"

Get-ChildItem -Filter "*TimeToDisco*" -Recurse | Rename-Item -NewName {$_.name -replace "TimeToDisco\(0\)","mainframe" } 

ffmpeg -framerate 15 -i mainframe_%4d.png main.mp4

# "C:\Program Files\Topaz Labs LLC\Topaz Video Enhance AI"
# veai.exe --help