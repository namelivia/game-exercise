import pyglet
from pyglet.gl import *
import ctypes

# This is initialization
def start_video():
    VIDEO_FILE = 'your_video.mp4'
    try:
        media_source = pyglet.media.load(VIDEO_FILE)
        player = pyglet.media.Player()
        player.queue(media_source)
        player.play()
    except pyglet.media.MediaException as e:
        print(f"Error al cargar el video: {e}. Asegúrate de que el archivo de video sea válido.")
        player = None


# This is what needs to happen on every screen update so the video frame
# is displayed on the window
def update():
    pyglet.clock.tick()
    if player and player.source and player.source.video_format:
        video_texture = player.get_texture()
        
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, video_texture.id)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, WIDTH, 0, HEIGHT, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        video_x, video_y = 50, 50
        video_width, video_height = video_texture.width, video_texture.height
        
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(video_x, video_y)
        
        glTexCoord2f(1.0, 0.0)
        glVertex2f(video_x + video_width, video_y)
        
        glTexCoord2f(1.0, 1.0)
        glVertex2f(video_x + video_width, video_y + video_height)
        
        glTexCoord2f(0.0, 1.0)
        glVertex2f(video_x, video_y + video_height)
        glEnd()

        glDisable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)

# This is cleanup
def exit():
    if player:
        player.pause()
        player.delete()
