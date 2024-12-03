from moviepy.editor import VideoFileClip, AudioFileClip

title = '重制【自制中日字幕】Ado 2023 武道馆 LIVE 翻唱歌曲《ブリキノダンス》（馬口鐵之舞）'
# 加载视频文件
video = VideoFileClip('video\\' + title + '.mp4')

# 加载音频文件
audio = AudioFileClip('video\\' + title + '.mp3')

# 将音频添加到视频中
video_with_audio = video.set_audio(audio)

# 导出带音频的视频
video_with_audio.write_videofile("output_with_audio.mp4", codec="libx264", preset="ultrafast", audio_codec="aac")