 
import pafy
import tempfile

url = "https://www.youtube.com/watch?v=8CT_txWEo5I"
video = pafy.new(url)
bestaudio = video.getbestaudio()

# f = tempfile.NamedTemporaryFile(delete=False)
# f.close()


filename  = bestaudio.download(filepath="./files/tmp")


