import subprocess

# Function create to master M3U8 playlist from inout MP4 file
def create_master_playlist(video, output):
    command = "ffmpeg -i {video} -c:v libx264 -crf 20 -g 5 -keyint_min 5 -sc_threshold 0 -hls_time 4 -hls_flags independent_segments \
  -b:v:0 800k -filter:v:0 scale=640:360 \
  -b:v:1 1200k -filter:v:1 scale=842:480 \
  -b:v:2 2400k -filter:v:2 scale=1280:720 \
  -b:v:3 4800k -filter:v:3 scale=1920:1080 \
  -map 0:v -map 0:v -map 0:v -map 0:v -f hls -var_stream_map 'v:0 v:1 v:2 v:3' \
  -master_pl_name master.m3u8 \
  -hls_segment_filename stream_%v/data%03d.ts \
  -use_localtime_mkdir 1 \
  {output}".format(video=video, output=output)
    subprocess.call(command,shell=True)

create_master_playlist('test.mp4', 'stream_%v.m3u8')