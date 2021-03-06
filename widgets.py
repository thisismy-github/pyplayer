from PyQt5 import QtGui, QtCore  # QtMultimedia, QtMultimediaWidgets
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets as QtW

import qtstart
import constants
import qthelpers
from util import ffmpeg, get_unique_path, get_hms

import os
import time
import math
import logging

import vlc
from colour import Color
from threading import Thread
from traceback import format_exc

# TODO: I absolutely cannot decide what should be camelCase and what should be underscores. It's becoming an issue.
# media_player: ['_as_parameter_', '_instance', 'add_slave', 'audio_get_channel', 'audio_get_delay', 'audio_get_mute', 'audio_get_track', 'audio_get_track_count', 'audio_get_track_description', 'audio_get_volume', 'audio_output_device_enum', 'audio_output_device_get', 'audio_output_device_set', 'audio_output_set', 'audio_set_callbacks', 'audio_set_channel', 'audio_set_delay', 'audio_set_format', 'audio_set_format_callbacks', 'audio_set_mute', 'audio_set_track', 'audio_set_volume', 'audio_set_volume_callback', 'audio_toggle_mute', 'can_pause', 'event_manager', 'from_param', 'get_agl', 'get_chapter', 'get_chapter_count', 'get_chapter_count_for_title', 'get_fps', 'get_full_chapter_descriptions', 'get_full_title_descriptions', 'get_fullscreen', 'get_hwnd', 'get_instance', 'get_length', 'get_media', 'get_nsobject', 'get_position', 'get_rate', 'get_role', 'get_state', 'get_time', 'get_title', 'get_title_count', 'get_xwindow', 'has_vout', 'is_playing', 'is_seekable', 'navigate', 'next_chapter', 'next_frame', 'pause', 'play', 'previous_chapter', 'program_scrambled', 'release', 'retain', 'set_agl', 'set_android_context', 'set_chapter', 'set_equalizer', 'set_evas_object', 'set_fullscreen', 'set_hwnd', 'set_media', 'set_mrl', 'set_nsobject', 'set_pause', 'set_position', 'set_rate', 'set_renderer', 'set_role', 'set_time', 'set_title', 'set_video_title_display', 'set_xwindow', 'stop', 'toggle_fullscreen', 'toggle_teletext', 'video_get_adjust_float', 'video_get_adjust_int', 'video_get_aspect_ratio', 'video_get_chapter_description', 'video_get_crop_geometry', 'video_get_cursor', 'video_get_height', 'video_get_logo_int', 'video_get_marquee_int', 'video_get_marquee_string', 'video_get_scale', 'video_get_size', 'video_get_spu', 'video_get_spu_count', 'video_get_spu_delay', 'video_get_spu_description', 'video_get_teletext', 'video_get_title_description', 'video_get_track', 'video_get_track_count', 'video_get_track_description', 'video_get_width', 'video_set_adjust_float', 'video_set_adjust_int', 'video_set_aspect_ratio', 'video_set_callbacks', 'video_set_crop_geometry', 'video_set_deinterlace', 'video_set_format', 'video_set_format_callbacks', 'video_set_key_input', 'video_set_logo_int', 'video_set_logo_string', 'video_set_marquee_int', 'video_set_marquee_string', 'video_set_mouse_input', 'video_set_scale', 'video_set_spu', 'video_set_spu_delay', 'video_set_subtitle_file', 'video_set_teletext', 'video_set_track', 'video_take_snapshot', 'video_update_viewpoint', 'will_play']
# media: ['_as_parameter_', '_instance', 'add_option', 'add_option_flag', 'add_options', 'duplicate', 'event_manager', 'from_param', 'get_duration', 'get_instance', 'get_meta', 'get_mrl', 'get_parsed_status', 'get_state', 'get_stats', 'get_tracks_info', 'get_type', 'get_user_data', 'is_parsed', 'parse', 'parse_async', 'parse_stop', 'parse_with_options', 'player_new_from_media', 'release', 'retain', 'save_meta', 'set_meta', 'set_user_data', 'slaves_add', 'slaves_clear', 'slaves_get', 'subitems', 'tracks_get']

# ------------------------------------------
# Logger
# ------------------------------------------
logger = logging.getLogger('widgets.py')


# ------------------------------------------
# Aliases (set in main.pyw)
# ------------------------------------------
gui: QtW.QMainWindow = None
app: QtW.QApplication = None
cfg = None
settings = None


# ------------------------------------------
# Core Widgets
# ------------------------------------------
class QVideoPlayer(QtW.QWidget):  # https://python-camelot.s3.amazonaws.com/gpl/release/pyqt/doc/advanced/development.html <- relevant?
    def __init__(self, *args, **kwargs):
        ''' TODO: vlc.Instance() arguments to check out:
            --align={0 (Center), 1 (Left), 2 (Right), 4 (Top), 8 (Bottom), 5 (Top-Left), 6 (Top-Right), 9 (Bottom-Left), 10 (Bottom-Right)}
            --audio-time-stretch, --no-audio-time-stretch   Enable time stretching audio (default enabled) <- disabled = pitch changes with playback speed
            --gain=<float [0.000000 .. 8.000000]>           Audio gain
            --volume-step=<float [1.000000 .. 256.000000]>  Audio output volume step
            --marq-marquee, --sub-source=marq '''
        super().__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)     # https://stackoverflow.com/questions/7276330/qt-stylesheet-for-custom-widget
        self.setToolTipDuration(2000)
        self.setMouseTracking(True)                         # required for detecting idle movement
        self.setMinimumHeight(10)

        # setup VLC instance
        self.instance = vlc.Instance(qtstart.args.vlc)      # VLC arguments can be passed through the --vlc argument
        self.player = self.instance.media_player_new()
        self.media = None
        self.event_manager = self.player.event_manager()    # ??? cannot use .emit as a callback ???
        self.event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, lambda *args: gui.restart_signal.emit())

        self.player.stop()                                  # stopping the player at any point fixes the audio-cutoff bug
        self.player.video_set_key_input(False)              # pass VLC key events to widget
        self.player.video_set_mouse_input(False)            # pass VLC mouse events to widget
        self.player.video_set_marquee_int(vlc.VideoMarqueeOption.Enable, 1)

        self.text = None
        self.last_text = None
        self.text_fade_start_time = 0
        self.text_fade_thread_started = False
        self.text_position = 5
        self.text_height_percent = 0.05
        self.text_x_percent = 0.016
        self.text_y_percent = 0.016
        self.text_opacity = 255

        self.last_move_time = 0
        self.idle_cursor_timeout = 2.5
        self.last_invalid_snap_state_time = 0.0
        self.dragdrop_in_progress = False
        self.dragdrop_last_modifiers = None

        self.dragging: int = None
        self.dragging_offset: QtCore.QPoint = None
        self.drag_axis_lock: int = None
        self.panning = False
        self.true_left = 100
        self.true_right = 250
        self.true_top = 100
        self.true_bottom = 250
        self.true_rect: QtCore.QRect = None

        self.selection: list[QtCore.QPoint] = None
        self.last_factored_points: list[QtCore.QPoint] = None
        self.crop_frames: list[QtW.QFrame] = None
        self.crop_rect: QtCore.QRect = None
        self.reference_example: dict = None
        self.text_y_offsets: dict = None


    def play(self, file,  _error=False):
        try:
            #self.show_text(os.path.basename(file))
            self.media = self.instance.media_new(file)  # combines media_new_path (local files) and media_new_location (urls)
            self.player.set_media(self.media)           # TODO: this single line has a HUGE delay when opening first video after opening extremely large video
            #self.player.set_mrl(self.media.get_mrl())  # not needed? https://www.olivieraubert.net/vlc/python-ctypes/doc/vlc.MediaPlayer-class.html#set_mrl
            self.player.play()
            self.media.parse_with_options(0x0, 0)       # https://www.olivieraubert.net/vlc/python-ctypes/doc/vlc.Media-class.html#parse_with_options
            return True
        except:
            logger.warning(f'VLC failed to play file {file}: {format_exc()}')
            if not _error:  # _error ensures we only attempt to play previous video once
                if not gui.video: self.player.stop()     # no previous video to play, so just stop playing
                else: self.play(gui.video, _error=True)  # attempt to play previous working video
            return False


    def reset_dragdrop_status(self):
        ''' Quickly clears drag-and-drop related messages and properties. '''
        gui.statusbar.clearMessage()
        self.show_text('')
        self.dragdrop_last_modifiers = None
        self.dragdrop_in_progress = False


    # ---------------------
    # Marquees
    # ---------------------
    def show_text(self, text: str, timeout: int = 350, position: int = None):
        ''' Displays marquee `text` on the player, for `timeout` milliseconds at `position`:
            0 (Center), 1 (Left), 2 (Right), 4 (Top), 5 (Top-Left), 6 (Top-Right), 8 (Bottom), 9 (Bottom-Left), 10 (Bottom-Right)

            TODO: marquees are supposed to be chainable -> https://wiki.videolan.org/Documentation:Modules/marq/
            NOTE: vlc.py claims "Marquee requires '--sub-source marq' in the Instance() call" <- not true?
            NOTE: VLC supports %-strings: https://wiki.videolan.org/Documentation:Format_String/
                  Escape isolated % characters with %%. Use VideoMarqueeOption.Refresh to auto-update text on
                  an interval. See the bottom of vlc.py for an example implementation of an on-screen clock. '''
        if not settings.groupText.isChecked(): return           # marquees are completely disabled -> return
        try:
            if position is None: position = self.text_position  # reuse last position if needed
            self.text = (text, timeout, position)               # self.text is read by text_fade_thread
            unique_settings = self.text != self.last_text
            self.last_text = self.text                          # TODO: calling show_text very rapidly results in no fading (text still goes away on time, though)
            self.text_fade_start_time = time.time() + settings.spinTextFadeDelay.value()            # TODO this doesn't look right at low non-zero values (<0.5)
            self.player.video_set_marquee_int(vlc.VideoMarqueeOption.Opacity, self.text_opacity)    # reset opacity to default (repetitive but sometimes necessary)

            if (timeout == 0 and not unique_settings) or not gui.video: return                      # avoid repetitive + pointless calls
            if unique_settings:                                                                     # avoid repetitive set_xyz() calls
                self.player.video_set_marquee_int(vlc.VideoMarqueeOption.Position, position)
                self.player.video_set_marquee_string(vlc.VideoMarqueeOption.Text, text)             # set new text
            if not self.text_fade_thread_started:
                Thread(target=self.text_fade_thread, daemon=True).start()
                self.text_fade_thread_started = True
        except: logger.warning(f'(!) Unexpected error while showing text overlay: {format_exc()}')


    def text_fade_thread(self):
        while not gui.closed:
            now = time.time()
            fade_time = self.text[1] / 1000                     # self.text[1] = timeout
            if now >= self.text_fade_start_time and fade_time != 0:
                if now <= self.text_fade_start_time + fade_time:
                    alpha = (self.text_fade_start_time + fade_time - now) * (self.text_opacity / fade_time)
                    self.player.video_set_marquee_int(vlc.VideoMarqueeOption.Opacity, round(alpha))
                    time.sleep(0.005)
                else:                                           # if we just finished fading, make sure no text is visible
                    #self.player.video_set_marquee_string(vlc.VideoMarqueeOption.Text, '')
                    self.player.video_set_marquee_int(vlc.VideoMarqueeOption.Opacity, 0)
                    self.text_fade_start_time = 9999999999      # set start_time to extreme number to limit
            else: time.sleep(0.5 if self.text_fade_start_time - now < 1 else 0.025)  # sleep less frequently if we're going to fade soon


    def set_text_position(self, button: QtW.QRadioButton):
        ''' Uses the last characters of a given `button`'s object name to detect which position it represents. Positions:
            0 (Center), 1 (Left), 2 (Right), 4 (Top), 5 (Top-Left), 6 (Top-Right), 8 (Bottom), 9 (Bottom-Left), 10 (Bottom-Right) '''
        self.text_position = int(button.objectName()[17:])
        self.player.video_set_marquee_int(vlc.VideoMarqueeOption.Position, self.text_position)


    def set_text_height(self, percent: int):
        self.text_height_percent = percent / 100
        new_size = int(gui.vheight * self.text_height_percent)
        self.player.video_set_marquee_int(vlc.VideoMarqueeOption.Size, new_size)


    def set_text_x(self, percent: float):
        self.text_x_percent = percent / 100
        new_x = int(gui.vheight * self.text_x_percent)          # offset is relative to media's height for both X and Y
        self.player.video_set_marquee_int(vlc.VideoMarqueeOption.X, new_x)


    def set_text_y(self, percent: float):
        self.text_y_percent = percent / 100
        new_y = int(gui.vheight * self.text_y_percent)          # offset is relative to media's height for both X and Y
        self.player.video_set_marquee_int(vlc.VideoMarqueeOption.Y, new_y)


    def set_text_opacity(self, percent: int):
        self.text_opacity = round(255 * (percent / 100))


    # ---------------------
    # Cropping Utilities
    # ---------------------
    def get_crop_point_index_in_range(self, pos: QtCore.QPoint, _range: int = 30, p=False):
        ''' Gets the index of the closest crop-corner to `pos`, if any are within `_range` pixels, otherwise None. '''
        min_dist = 1000
        min_point = None
        for point in self.selection:
            #dist = abs(pos.x() - point.x()) + abs(pos.y() - point.y())     # TODO: verify that manhattanLength is actually better than this
            dist = (pos - point).manhattanLength()              # https://doc.qt.io/qt-5/qpoint.html#manhattanLength
            if dist < min_dist:
                min_dist = dist
                min_point = point
        return None if min_dist > _range else self.selection.index(min_point)


    def get_crop_edge_index_in_range(self, pos: QtCore.QPoint, _range: int = 15):
        ''' Gets the closest crop-edge to `pos`, if any are within `_range` pixels, otherwise None. Returns
            the index of an associated corner for each edge. Left: 0, Top: 1, Right: 2, Bottom: 3. '''
        s = self.selection
        for index in range(2):  # 0, 1
            if s[index].x() - _range <= pos.x() <= s[index].x() + _range and s[index].y() < pos.y() < s[(index + 2) % 4].y():
                return 0 if index == 0 else 2                   # hovering over left edge if index == 0, else right edge
            elif s[index * 2].y() - _range <= pos.y() <= s[index * 2].y() + _range and s[index * 2].x() < pos.x() < s[(index * 2) + 1].x():
                return 1 if index == 0 else 3                   # hovering over top edge if index == 0, else bottom edge
        return None


    def correct_points(self, changed_point_index):
        reference_point = self.selection[changed_point_index]
        x, y = reference_point.x(), reference_point.y()
        corrective_functions = self.reference_example[changed_point_index]
        for index, point in enumerate(self.selection):
            if index in corrective_functions:                                           # only 3/4 points are in each reference_example
                corrective_functions[index](x, y)                                       # run reference_example corrective function
                point.setX(min(self.true_right, max(self.true_left, point.x())))        # clamp each point to true borders
                point.setY(min(self.true_bottom, max(self.true_top, point.y())))        # true_bottom > true_top
                #self.selection[self.dragging].setX(min(self.true_right, max(self.true_left, point.x())))
                #self.selection[self.dragging].setY(min(self.true_bottom, max(self.true_top, point.y())))        # true_bottom > true_top
                #print('true borders (lrtb):', self.true_left, self.true_right, self.true_top, self.true_bottom, '| points:', point.x(), point.y(), f'| widget size: {self.width()}x{self.height()}')


    def factor_point(self, pos: QtCore.QPoint) -> QtCore.QPointF:
        ''' Converts a QPoint `pos` relative to QVideoPlayer to the approximate QPointF relative to the
            media's native resolution using the factor between the size of media within the QVideoPlayer
            frame and the media's native resolution. VLC apparently chooses to not expose the size of the
            media it is actively resizing, which is why we must calculate it manually. '''
        w = self.width()
        h = self.height()
        vw = gui.vwidth
        vh = gui.vheight
        ratio = vw / vh                     # native aspect ratio
        widget_ratio = w / h                # aspect ratio of QVideoPlayer
        if widget_ratio < ratio:            # video fills viewport width (there are black bars top/bottom)
            factor = vw / w
            void = ((h * factor) - vh) / 2  # calculate size of black bars
            x = pos.x() * factor
            y = (pos.y() * factor) - void   # account for black bars
            y = max(0, min(y, vh))          # I don't remember why this is needed
        else:                               # video fills viewport height (there are black bars left/right)
            factor = vh / h
            void = ((w * factor) - vw) / 2  # calculate size of black bars
            x = (pos.x() * factor) - void   # account for black bars
            y = pos.y() * factor
            x = max(0, min(x, vw))          # I don't remember why this is needed
        #print(f'factored pos ({pos.x()}, {pos.y()}) to ({x}, {y}) -> ratio={ratio} widget_ratio={widget_ratio} w={w} h={h} vw={vw} vh={vh} factor={factor} void={void}')
        return QtCore.QPointF(x, y)


    def defactor_point(self, pos: QtCore.QPointF) -> QtCore.QPoint:
        ''' The opposite of factor_point. Does what factor_point does, but in reverse,
            returning the approximate local QPoint relative to QVideoPlayer from a
            QPointF `pos` relative to the media's native resolution. '''
        w = self.width()
        h = self.height()
        vw = gui.vwidth
        vh = gui.vheight
        ratio = vw / vh
        widget_ratio = w / h
        if widget_ratio < ratio:                    # video fills viewport width (there are black bars top/bottom)
            factor = vw / w
            void = ((h * factor) - vh) / 2          # ((h - (w / video_ratio)) / 2)
            x = pos.x() / factor
            y = (pos.y() + void) / factor
            y = max(0, min(y, h))
        else:                                       # video fills viewport height (there are black bars left/right)
            factor = vh / h
            void = ((w * factor) - vw) / 2
            x = (pos.x() + void) / factor
            y = pos.y() / factor
            x = max(0, min(x, w))
        #print(f'de-factored pos ({pos.x()}, {pos.y()}) to ({x}, {y}) -> ratio={ratio} widget_ratio={widget_ratio} w={w} h={h} vw={vw} vh={vh} factor={factor} void={void}')
        return QtCore.QPoint(x, y)


    def find_true_borders(self):
        ''' Calculates a QRect containing the corners of the actual resolution QVideoPlayer
            is displaying media at, similar to factor_point/defactor_point. I don't remember why,
            but a different calculation for the black bar size is required here. '''
        w = self.width()
        h = self.height()

        # TODO which one is faster, vsize version or commented-out version? is having vsize JUST for this worth it?
        #vw = gui.vwidth
        #vh = gui.vheight
        #video_ratio = vw / vh                       # vh is never 0 (handled in gui.open())
        #widget_ratio = w / h
        #if widget_ratio < video_ratio:              # video fills viewport width (there are black bars top/bottom)

        expected_size = gui.vsize.scaled(self.size(), Qt.KeepAspectRatio)
        if expected_size.height() < h:              # video fills viewport width (there are black bars top/bottom)
            logger.debug('Video fills viewport width (there are black bars top/bottom)')
            #void = ((h - (w / video_ratio)) / 2)
            void = (h - expected_size.height()) / 2
            self.true_left =   0
            self.true_right =  w
            self.true_top =    int(void)            # ensure potential error is outside bounds of actual video size
            self.true_bottom = math.ceil(h - void)  # ensure potential error is outside bounds of actual video size
        else:                                       # video fills viewport height (there are black bars left/right)
            logger.debug('Video fills viewport height (there are black bars left/right)')
            #void = ((w - (h * video_ratio)) / 2)
            void = (w - expected_size.width()) / 2
            self.true_left =   int(void)            # ensure potential error is outside bounds of actual video size
            self.true_right =  math.ceil(w - void)  # ensure potential error is outside bounds of actual video size
            self.true_top =    0
            self.true_bottom = h
        self.true_rect = QtCore.QRect(QtCore.QPoint(self.true_left, self.true_top), QtCore.QPoint(self.true_right, self.true_bottom))
        logger.debug(f'void={void} w={w} h={h} expected_size={expected_size}')


    def update_crop_frames(self):
        ''' Updates the geometry for the four QFrames representing cropped out regions. Updates the tooltip to
            include the factored size of the visible region. Saves current set of factored points for later use. '''
        s = self.selection
        crop_top =    s[0].y()                      # TODO make these @property?
        crop_left =   s[0].x()
        crop_right =  s[1].x()
        crop_bottom = s[2].y()
        crop_height = crop_bottom - crop_top
        w = self.width()

        crop_frames = self.crop_frames
        crop_frames[0].setGeometry(0, 0, w, max(0, crop_top))                          # 0 top rectangle (full width)
        crop_frames[1].setGeometry(0, crop_top, crop_left, crop_height)                # 1 left rectangle
        crop_frames[2].setGeometry(crop_right, crop_top, w - crop_right, crop_height)  # 2 right rectangle
        crop_frames[3].setGeometry(0, crop_bottom, w, self.height() - crop_bottom)     # 3 bottom rectangle (full width)

        f = self.last_factored_points
        self.setToolTip(f'{f[1].x() - f[0].x():.0f}x{f[2].y() - f[0].y():.0f}')
        for index, point in enumerate(s): self.last_factored_points[index] = self.factor_point(point)


    # ---------------------
    # Events
    # ---------------------
    def paintEvent(self, event: QtGui.QPaintEvent):
        super().paintEvent(event)                           # TODO this line isn't actually needed?
        if not gui.actionCrop.isChecked(): return           # nothing else to paint if we're not cropping

        s = self.selection
        white = QtGui.QColor(255, 255, 255)
        black = QtGui.QColor(0, 0, 0)

        p = QtGui.QPainter()
        p.begin(self)
        p.setPen(QtGui.QPen(white, 6, Qt.SolidLine))
        p.setBrush(white)
        p.setFont(QtGui.QFont('Segoe UI Light', 10))
        try:
            # draw thin border around video (+2 and -4 to account for size-6 pen)
            p.drawRect(s[0].x() + 2,
                       s[0].y() + 2,
                       s[1].x() - s[0].x() - 4,
                       s[2].y() - s[0].y() - 4)

            # draw handle and coordinates for each corner
            for index, point in enumerate(s):
                #p.drawRect(point.x() - 3, point.y() - 3, 5, 5)
                text = f'({self.last_factored_points[index].x():.0f}, {self.last_factored_points[index].y():.0f})'
                p.setPen(black)                                                              # set color to black
                p.drawText(point.x() + 1, point.y() + self.text_y_offsets[index] + 1, text)  # draw shadow first
                p.setPen(QtGui.QPen(white, 6, Qt.SolidLine))                                 # set color to white
                p.drawText(point.x(), point.y() + self.text_y_offsets[index], text)          # draw actual text over shadow
                p.drawPoint(point.x(), point.y())                                            # size-6 point to represent handles
        except: logger.warning(f'(!) Unexpected error while painting crop view from QVideoPlayer: {format_exc()}')
        p.end()


    def resizeEvent(self, event: QtGui.QResizeEvent):
        ''' Recalculates borders and crop points while resizing if crop-mode
            is enabled. Also sets a timer for snapping the window to the
            current media's aspect ratio, as long as a timer isn't already
            active, snap-mode is enabled, we haven't recently altered the UI/
            maximized/fullscreened, and a file has already been loaded. '''
        if gui.actionCrop.isChecked():
            self.find_true_borders()
            #self.selection = [self.defactor_point(p) for p in self.last_factored_points]    # this should work but has bizarre side effects
            for index in range(4): self.correct_points(index)
            self.update_crop_frames()
        super().resizeEvent(event)

        # mark if we were recently fullscreen/maximized so we know not to snap-resize during the next few resizeEvents
        if gui.isMaximized() or gui.isFullScreen(): self.last_invalid_snap_state_time = time.time()

        # set timer to resize window to fit player (if no file has been played yet, do not set timers on resize)
        elif all((not gui.timer_id_resize_snap,
                  gui.is_snap_mode_enabled(),
                  time.time() - self.last_invalid_snap_state_time > 0.35,
                  gui.first_video_fully_loaded)):
            gui.timer_id_resize_snap = gui.startTimer(150, Qt.CoarseTimer)


    def mousePressEvent(self, event: QtGui.QMouseEvent):
        ''' Handles grabbing crop points/edges in crop-mode, as well as detected the
            forwards/backwards buttons and moving through the recent files list. '''
        try:
            if not gui.actionCrop.isChecked():                          # no crop -> check for back/forward buttons
                if event.button() == Qt.BackButton: gui.cycle_recent_files(forward=False)
                elif event.button() == Qt.ForwardButton: gui.cycle_recent_files(forward=True)
                return  # TODO add back/forward functionality globally (not as easy as it sounds?)

            self.panning = False
            pos = self.mapFromGlobal(QtGui.QCursor.pos())               # mousePressEvent's event.pos() appears to return incorrect values...
            self.dragging = self.get_crop_point_index_in_range(pos)     # ...in certain areas, leading to bad offsets and mismatched selections
            if self.dragging is not None:
                self.drag_axis_lock = None                              # reset axis lock before dragging corners
                self.dragging_offset = pos - self.selection[self.dragging]
            else:
                edge_index = self.get_crop_edge_index_in_range(pos)
                if edge_index is not None:
                    if edge_index % 2 == 0:
                        self.dragging = 0 if edge_index < 2 else 3
                        self.drag_axis_lock = 0
                    else:
                        self.dragging = 0 if edge_index < 2 else 3
                        self.drag_axis_lock = 1
                    self.dragging_offset = pos - self.selection[self.dragging]
                elif self.crop_rect.contains(pos):          # no corners/edges, but clicked inside crop rect -> panning
                    self.dragging = -1
                    self.drag_axis_lock = None              # reset axis lock before panning
                    self.dragging_offset = pos - self.selection[0]
                    if app.overrideCursor() is None: app.setOverrideCursor(QtGui.QCursor(Qt.ClosedHandCursor))
                    else: app.changeOverrideCursor(QtGui.QCursor(Qt.ClosedHandCursor))
            event.accept()
            self.update()
        except: logger.warning(f'(!) Unexpected error while clicking QVideoPlayer: {format_exc()}')
        return super().mousePressEvent(event)


    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        ''' Allows users to drag crop borders by their corners. '''
        if not gui.actionCrop.isChecked():                  # idle timeout is handled in QVideoSlider's paintEvent since it constantly updates
            if settings.checkHideIdleCursor.isChecked() and gui.video:
                self.last_move_time = time.time()           # update move time if a video is playing and idle timeouts are enabled
            else: self.last_move_time = 0                   # otherwise, keep move time at 0
            return event.ignore()                           # only handle idle timeouts if we're not cropping
        self.last_move_time = 0
        try:
            pos = self.mapFromGlobal(event.globalPos())     # event.pos() does not work. I have no explanation.
            if self.dragging is None:
                cursor = app.overrideCursor()
                crop_point_index = self.get_crop_point_index_in_range(pos)
                edge_index = self.get_crop_edge_index_in_range(pos)
                if crop_point_index is not None:            # https://doc.qt.io/qt-5/qguiapplication.html#overrideCursor
                    if cursor is None: app.setOverrideCursor(QtGui.QCursor(self.cursors[crop_point_index]))
                    else: app.changeOverrideCursor(QtGui.QCursor(self.cursors[crop_point_index]))
                elif edge_index is not None:
                    if edge_index % 2 == 0:
                        if cursor is None: app.setOverrideCursor(QtGui.QCursor(Qt.SizeHorCursor))
                        else: app.changeOverrideCursor(QtGui.QCursor(Qt.SizeHorCursor))
                    else:
                        if cursor is None: app.setOverrideCursor(QtGui.QCursor(Qt.SizeVerCursor))
                        else: app.changeOverrideCursor(QtGui.QCursor(Qt.SizeVerCursor))
                elif self.crop_rect.contains(pos):
                    if cursor is None: app.setOverrideCursor(QtGui.QCursor(Qt.SizeAllCursor))
                    else: app.changeOverrideCursor(QtGui.QCursor(Qt.SizeAllCursor))
                elif cursor is not None:
                    while app.overrideCursor():
                        app.restoreOverrideCursor()

            elif app.mouseButtons() == Qt.LeftButton:
                s = self.selection
                if self.drag_axis_lock is None: new_pos = pos - self.dragging_offset
                elif self.drag_axis_lock == 0: new_pos = QtCore.QPoint((pos - self.dragging_offset).x(), s[self.dragging].y())  # x-axis only
                else: new_pos = QtCore.QPoint(s[self.dragging].x(), (pos - self.dragging_offset).y())                           # y-axis only
                new_pos.setX(min(self.true_right, max(self.true_left, new_pos.x())))
                new_pos.setY(min(self.true_bottom, max(self.true_top, new_pos.y())))

                if self.dragging == -1:                     # we are panning the entire crop area
                    delta = new_pos - s[0]
                    for point in s: point += delta

                    if not self.true_rect.contains(s[3]):   # ask on stackoverflow why the better solution didn't work? lmao
                        up =   QtCore.QPoint(0, 1)
                        left = QtCore.QPoint(1, 0)
                        while s[3].y() > self.true_bottom:
                            for point in s: point -= up
                        while s[3].x() > self.true_right:
                            for point in s: point -= left
                    self.panning = True     # indicate that we have started panning so we don't pause video on release
                else:
                    if app.keyboardModifiers() & Qt.ControlModifier:    # TODO this barely works, but it works. for now
                        self.dragging = 0                               # TODO bandaid fix so I don't have to finish all 4 points
                        new_x = new_pos.x()
                        anchor_index = (self.dragging + 1) % 4
                        anchor = s[anchor_index]
                        dragged = s[self.dragging]
                        if self.dragging % 2 == 0:
                            new_y = dragged.y() + (new_x - dragged.x())
                            dragged.setY(new_y)
                            height = s[(self.dragging + 2) % 4].y() - dragged.y()
                            anchor.setX(new_x + height)     # new_x - height is close to making indexes 1/3 work
                        else:
                            new_y = dragged.y() - (new_x - dragged.x())
                            dragged.setY(new_y)
                            height = s[(self.dragging + 2) % 4].y() - dragged.y()
                            anchor.setX(new_x - height)     # new_x - height is close to making indexes 1/3 work
                        ##dragged.setY(anchor.x() - dragged.x())
                        dragged.setX(new_x)
                        #dragged.setY(new_x)
                        #anchor.setX(anchor.x() - (anchor.x() - dragged.x()))
                        #height = s[(self.dragging + 2) % 4].y() - dragged.y()
                        #anchor.setX(new_x + height)         # new_x - height is close to making indexes 1/3 work
                        self.correct_points(self.dragging)
                        self.correct_points(anchor_index)
                    else:
                        s[self.dragging] = new_pos
                        self.correct_points(self.dragging)

                self.crop_rect.setTopLeft(s[0])
                self.crop_rect.setBottomRight(s[3])

                self.update_crop_frames()        # update crop frames and factored points
                self.repaint()                   # repaint QVideoPlayer (TODO: update() vs repaint() here)
        except TypeError: pass                   # self.dragging is None
        except: logger.warning(f'(!) Unexpected error while dragging crop points: {format_exc()}')
        #return super().mouseMoveEvent(event)    # TODO: required for mouseReleaseEvent to work properly?


    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        ''' Pauses media after clicking and releasing left-click over player, ignoring clicks that were
            dragged outside player. Releases dragged crop points/edges if needed, and resets cursor. '''
        #print('release', self.dragging, self.panning)              # TODO: sometimes this STILL pauses
        # left click released and we're either not dragging crop points or we clicked the middle but did not start panning
        if event.button() == Qt.LeftButton and (self.dragging is None or self.dragging == -1) and not self.panning:
            if self.underMouse():                                   # mouse wasn't dragged off player
                gui.pause()
        if self.dragging is not None:
            while app.overrideCursor():                             # reset cursor to default
                app.restoreOverrideCursor()
        #self.panning = False
        self.dragging = None                                        # release drag


    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent):      # fullscreen video by double-clicking on it (left-click only)
        ''' Triggers GUI's fullscreen action after double-clicking the player. '''
        if event.button() == Qt.LeftButton: gui.actionFullscreen.trigger()


    def leaveEvent(self, event: QtCore.QEvent):
        ''' Automatically stop dragging and reset cursor when the mouse leaves the window. '''
        while app.overrideCursor(): app.restoreOverrideCursor()     # reset cursor to default
        self.dragging = None
        #print('setting panning to true', event.buttons())
        #self.panning = True  # TODO this is a bandaid fix. dragging/panning sometimes wrongly report as None and False, causing unexpected pauses in mouseReleaseEvent


    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):         # accept drag if dragging files (requires self.setAcceptDrops(True))
        ''' Accepts a cursor-drag if files are being dragged. Requires self.setAcceptDrops(True). '''
        if event.mimeData().hasUrls(): event.accept()
        else: event.ignore()
        self.dragdrop_in_progress = True
        super().dragEnterEvent(event)                               # run QWidget's built-in behavior


    def dragLeaveEvent(self, event: QtGui.QDragLeaveEvent):
        ''' Resets drag-and-drop status if user drags cursor off the window (to clear messages). '''
        self.reset_dragdrop_status()
        super().dragLeaveEvent(event)


    def dragMoveEvent(self, event: QtGui.QDragMoveEvent):
        ''' Indicates what the currently held button-combination will do once the drag-and-drop finishes on the statusbar and
            player (if possible). Keeps track of currently held button-combination to avoid repetitive statusbar/marquee calls. '''
        if not gui.video:                       # no video is playing, can't show marquee. and don't bother showing special options
            gui.statusbar.showMessage('Drop to play media, or hold ctrl/alt/shift while media is playing for additional options')
        else:
            mod = event.keyboardModifiers()
            if mod != self.dragdrop_last_modifiers:
                self.dragdrop_last_modifiers = mod
                if mod & Qt.ControlModifier:            # ctrl (concat before current)
                    gui.statusbar.showMessage('Drop to concatenate before current media', 0)
                    self.show_text('Drop to concatenate before current media', timeout=0, position=0)
                elif mod & Qt.AltModifier:              # alt (concat after current)
                    gui.statusbar.showMessage('Drop to concatenate after current media', 0)
                    self.show_text('Drop to concatenate after current media', timeout=0, position=0)
                elif mod & Qt.ShiftModifier:            # shift (add audio track)
                    file = [url.toLocalFile() for url in event.mimeData().urls()][0]
                    if os.path.abspath(file) != gui.video:
                        gui.statusbar.showMessage('Drop to add as audio track', 0)
                        self.show_text('Drop to add as audio track', timeout=0, position=0)
                    else:
                        gui.statusbar.showMessage('Drop to add as audio track (disabled due to identical file)', 0)
                        self.show_text('Drop to add as audio track (disabled due to identical file)', timeout=0, position=0)
                else:                                   # no modifiers (play file)
                    gui.statusbar.showMessage('Drop to play media, or hold ctrl/alt/shift for more options', 0)
                    self.show_text('Drop to play media, or hold ctrl/alt/shift for more options', timeout=0, position=0)
        super().dragMoveEvent(event)


    def dropEvent(self, event: QtGui.QDropEvent):       # attempt to open dropped files
        ''' Attempts to interact with the file that has been dropped as either media or a subtitle track.
            Ignores files beyond the first one. Allows modifiers to alter the interaction used.
            No modifiers -> Open single media file/adds subtitle file(s).
            Ctrl         -> Adds single media file as an audio track.
            Shift        -> Concatenates media file(s) to the end of the current media.
            Alt          -> Concatenates media file(s) to the start of the current media. '''
        self.reset_dragdrop_status()
        focus_window = settings.checkFocusDrop.isChecked()
        files = [url.toLocalFile() for url in event.mimeData().urls()]

        if gui.video:
            mod = event.keyboardModifiers()
            if mod & Qt.ControlModifier:                # ctrl (concat before current)
                gui.concatenate(action=gui.actionCatBefore, files=files)
            elif mod & Qt.AltModifier:                  # alt (concat after current)
                gui.concatenate(action=gui.actionCatAfter, files=files)
            elif mod & Qt.ShiftModifier:                # shift (add audio track, one file at time currently)
                file = files[0]
                if os.path.abspath(file) != gui.video: gui.add_audio(path=file)
                else: gui.statusbar.showMessage('Cannot add file to itself as an audio track', 10000)
            else:                                       # no modifiers pressed, check if subtitle files were dropped
                subtitle_files = [QtCore.QUrl.fromLocalFile(file) for file in files if os.path.splitext(file)[-1] in constants.SUBTITLE_EXTENSIONS]
                if subtitle_files: gui.browse_for_subtitle_file(urls=subtitle_files)
                else: gui.open(files[0], focus_window=focus_window)  # no modifiers, no subtitles -> play dropped file as media
        else: gui.open(files[0], focus_window=focus_window)          # no video playing -> ignore modifiers and play dropped file
        if settings.checkRememberDropFolder.isChecked():             # update lastdir if desired
            cfg.lastdir = os.path.dirname(files[0])
        super().dropEvent(event)                        # run QWidget's built-in behavior




class QVideoPlayerLabel(QtW.QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.art = QtGui.QPixmap()
        self.gif = QtGui.QMovie()

        self._imageScale = 0                            # 0 -> No scaling (native size)
        self._artScale = 0                              # 1 -> Fit (keep aspect ratio)
        self._gifScale = 0                              # 2 -> Fill (ignore aspect ratio)
        self._dragging = False
        self._draggingOffset = QtCore.QPoint()          # offset between cursor and image's real pos
        self.pixmapPos = QtCore.QPoint()                # local position of currently drawn QPixmap
        self.gifSize = None                             # gif's native size (not tracked by QMovie)
        self.gif.setCacheMode(QtGui.QMovie.CacheAll)    # required for jumpToFrame to work
        self.image = self.art                           # alias for self.art's QPixmap
        self.isCoverArt = False
        self.filename = None

        self.zoom = 1.0                                 # the true, current zoom level
        self._baseZoom = 1.0                            # base zoom level for the current window size
        self._targetZoom = 1.0                          # the zoom level we're trying to reach
        self._smoothZoomTimerID = None                  # the ID for the smooth zoom timer, if any
        self._smoothZoomPos = QtCore.QPoint()           # the pos a smooth zoom should zoom in on
        self._smoothZoomFactor = 0.33                   # the "speed" at which a smooth zoom occurs
        self.zoomed = False                             # whether or not zoom-mode is enabled


    def play(self, file, gif: bool = False, autostart: bool = True):
        ''' Opens `file`. If `gif` is True, it's opened as a QMovie and starts
            playing immediately based on `autostart`. Otherwise if `file` is a
            string, it is displayed as a QPixmap. If `file` is a bytes object,
            it is decoded as a QPixmap, `isCoverArt` is set to True, and mouse
            events are disabled. If `file` is None, the label is cleared. '''
        self.gif.stop()
        self.filename = file
        self.zoomed = False
        if file is None:
            self.clear()
            self.gif.setFileName('')
            return self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        if gif:
            scale = self._gifScale      # load gif into QPixmap first to get its native size
            self.art.load(file)
            self.gifSize = self.art.size()
            self.clear()

            self.gif.setFileName(file)
            if scale == 1: self._resizeMovieFit()
            self.setMovie(self.gif)
            if autostart: self.gif.start()
            self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
            logger.info('Animated image detected.')

        else:                           # static image. if `file` is bytes, it's cover art
            isBytes = self.isCoverArt = isinstance(file, bytes)
            if isBytes: self.art.loadFromData(file)
            else: self.art.load(file)
            self.setPixmap(self.art)
            self.setAttribute(Qt.WA_TransparentForMouseEvents, isBytes)
            logger.info(f'Static image/cover art detected. (zoom={self.zoom})')
        self.disableZoom()


    def _updateImageScale(self, index: int):
        ''' Updates the scaling mode for images (excluding cover art). '''
        self._imageScale = index
        if self.pixmap():
            if not self.zoomed:
                self._calculateBaseZoom()
            self.update()


    def _updateArtScale(self, index: int):
        ''' Updates the scaling mode specifically for cover art. '''
        self._artScale = index
        if self.pixmap():
            if not self.zoomed:
                self._calculateBaseZoom()
            self.update()


    def _updateGifScale(self, index: int):
        ''' Updates the scaling mode for animated GIFs. '''
        self._gifScale = index
        if self.movie():
            if self.zoomed: self.setZoom(self.zoom, force=True)
            else:
                self._resetMovieSize()
                self._calculateBaseZoom()


    def _updateSmoothZoomFactor(self, factor: int):
        ''' Updates the smooth zoom "speed" `factor`. The QSpinBox is
            a percentage from 0-100 to make it easier to understand. '''
        self._smoothZoomFactor = factor / 100


    def _updatePreciseZoom(self, checked: bool):
        ''' Updates the "precise zoom" mode by swapping `pixmapPos`'s type
            between QPoint and QPointF to minimize errors. Precise zooming
            uses QPointF, normal zooming uses QPoint. '''
        if checked:
            if isinstance(self.pixmapPos, QtCore.QPoint):
                self.pixmapPos = QtCore.QPointF(self.pixmapPos)
        elif isinstance(self.pixmapPos, QtCore.QPointF):
            self.pixmapPos = self.pixmapPos.toPoint()


    def _resetMovieCache(self):
        ''' Stops and resets GIF to clear cached frames.
            Pause state is restored after reset. '''
        self.gif.stop()
        self.gif.setFileName(self.gif.fileName())
        self.gif.start()
        self.gif.setPaused(gui.is_paused)


    def _resetMovieSize(self):
        scale = self._gifScale
        self.setScaledContents(scale == 2)
        if scale == 0: self.gif.setScaledSize(QtCore.QSize(-1, -1))
        elif scale == 1: self._resizeMovieFit()
        elif scale == 2: self.gif.setScaledSize(self.size())
        self._resetMovieCache()


    def _resizeMovieFit(self):
        self.gif.setScaledSize(self.gifSize.scaled(self.size(), Qt.KeepAspectRatio))


    def _calculateBaseZoom(self) -> float:
        ''' Calculates the default zoom level for the current window size. '''
        if self.movie():
            scale = self._gifScale
            if scale == 0: zoom = 1.0
            elif scale == 2: zoom = self.size().width() / self.gifSize.width()
            else: zoom = self.gif.scaledSize().width() / self.gifSize.width()
        elif self.pixmap():
            scale = self._artScale if self.isCoverArt else self._imageScale
            if scale == 0: zoom = 1.0
            elif scale == 2: zoom = self.size().width() / self.art.width()
            else:
                newSize = self.art.size().scaled(self.size(), Qt.KeepAspectRatio)
                zoom = newSize.width() / self.art.width()
        else: return 1.0
        zoom = round(zoom, 4)
        self.zoom = self._baseZoom = self._targetZoom = zoom
        return zoom


    def setZoom(self, zoom: float, pos: QtCore.QPoint = None,
                globalPos: QtCore.QPoint = None,
                force: bool = False, _smooth: bool = False) -> float:
        maxZoom = 100.0 if not self.movie() else 20.0
        minZoomFactor = settings.spinZoomMinimumFactor.value()
        minZoom = self._baseZoom * minZoomFactor
        if settings.checkZoomForceMinimum.isChecked():
            minZoom = min(minZoomFactor, minZoom)

        if not _smooth: zoom = round(min(maxZoom, max(minZoom, zoom)), 4)
        if zoom == self.zoom and not force:
            if minZoomFactor == 1.0 and zoom == self._baseZoom and settings.checkZoomAutoDisable1x.isChecked():
                return self.disableZoom()   # _baseZoom == _targetZoom -> faster reset during smooth zoom (not worth it)
            return zoom

        willSmooth = not _smooth and settings.checkZoomSmooth.isChecked()
        if willSmooth:                      # about to start smoothing -> do first zoom-step now, start timer
            self._targetZoom = zoom
            if self._smoothZoomTimerID is None:
                zoom += (zoom - self.zoom) * self._smoothZoomFactor
                self._smoothZoomTimerID = self.startTimer(17, Qt.PreciseTimer)      # 17ms timer ~= 59fps

        if self.movie():
            if not willSmooth:
                if self._gifScale == 2:
                    self.setScaledContents(False)
                    newSize = self.size().scaled(self.gifSize, Qt.KeepAspectRatio) * zoom
                else: newSize = self.gifSize * zoom
                self.gif.setScaledSize(newSize)
                self._resetMovieCache()     # you can smooth zoom without freezing, but it's SLOWER than spam-resetting
        else:
            if globalPos: pos = self.mapFromGlobal(globalPos)
            if pos:
                if willSmooth: self._smoothZoomPos = pos                            # set pos for smooth zoom to re-use
                elif settings.checkZoomPrecise.isChecked():
                    newSize = QtCore.QSizeF(self.art.size()) * zoom
                    oldSize = QtCore.QSizeF(self.art.size()) * self.zoom
                    oldPos = self.pixmapPos
                    xOffset = ((pos.x() - oldPos.x()) / oldSize.width()) * newSize.width()
                    yOffset = ((pos.y() - oldPos.y()) / oldSize.height()) * newSize.height()
                    self.pixmapPos = pos - QtCore.QPointF(xOffset, yOffset)
                    if not _smooth: self._draggingOffset = pos - self.pixmapPos     # drag + zoom is bad unless it's a smooth zoom
                else:
                    newSize = self.art.size() * zoom
                    oldSize = self.art.size() * self.zoom
                    oldPos = self.pixmapPos
                    xOffset = ((pos.x() - oldPos.x()) / oldSize.width()) * newSize.width()
                    yOffset = ((pos.y() - oldPos.y()) / oldSize.height()) * newSize.height()
                    self.pixmapPos = pos - QtCore.QPoint(xOffset, yOffset)
                    if not _smooth: self._draggingOffset = pos - self.pixmapPos     # drag + zoom is bad unless it's a smooth zoom

        if not willSmooth: self.zoom = zoom
        self.zoomed = True
        self.update()
        if not _smooth: logger.debug(f'QVideoPlayerLabel zoom set to {zoom} (pos={pos} | globalPos={globalPos})')
        return zoom


    def incrementZoom(self, increment: float, pos: QtCore.QPoint = None,
                      globalPos: QtCore.QPoint = None, force: bool = False) -> float:
        return self.setZoom(self.zoom + increment, pos, globalPos, force)


    def disableZoom(self) -> float:
        self.zoomed = False
        self.pixmapPos = self.rect().center() - self.art.rect().center()
        if self._smoothZoomTimerID: self._smoothZoomTimerID = self.killTimer(self._smoothZoomTimerID)
        if self.movie(): self._resetMovieSize()
        else: self.setScaledContents(False)
        self.update()
        return self._calculateBaseZoom()


    def mousePressEvent(self, event: QtGui.QMouseEvent):
        ''' Sets the offset between the cursor and our QPixmap's local position. '''
        if event.button() == Qt.LeftButton and not gui.actionCrop.isChecked():
            self._draggingOffset = event.pos() - self.pixmapPos
        return super().mousePressEvent(event)           # QLabel will pass event to underlying widgets (needed for cropping)


    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        ''' Drags our QPixmap by adjusting its position based on the cursor's
            position relative to the offset we set in mousePressEvent. '''
        if not gui.actionCrop.isChecked() and not self.movie():
            if app.mouseButtons() == Qt.LeftButton:     # TODO normal mousePressEvent implementation, why won't event.button() work?
                self.pixmapPos = event.pos() - self._draggingOffset
                self._dragging = True
                self.update()                           # manually update
        return super().mouseMoveEvent(event)            # QLabel will pass event to underlying widgets (needed for cropping)


    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        ''' Disables drag-mode on releasing a mouse button. If left-clicking
            and drag-mode was never enabled, then zoom-mode is disabled. '''
        if event.button() == Qt.LeftButton:
            if not (self.movie() or self._dragging):    # reset QVideoPlayerLabel's zoom if we click without dragging
                self.disableZoom()
        self._dragging = False
        return super().mouseReleaseEvent(event)         # QLabel will pass event to underlying widgets (needed for cropping)


    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent):
        if self.zoomed and event.button() == Qt.LeftButton: self.disableZoom()
        else: super().mouseDoubleClickEvent(event)


    def wheelEvent(self, event: QtGui.QWheelEvent):
        ''' Increments the zoom factor by 1/6th of its current value if we're
            not cropping. Ctrl zooms twice as much. Shift, half as much. '''
        event.accept()                                  # accept the wheelEvent or QLabel will pass it through no matter what
        if gui.actionCrop.isChecked() or not gui.video: return
        add = event.angleDelta().y() > 0
        mod = event.modifiers()
        zoom = self._targetZoom if settings.checkZoomSmooth.isChecked() else self.zoom
        if not mod: factor = settings.spinZoomIncrement.value()
        elif mod & Qt.ShiftModifier: factor = settings.spinZoomShiftIncrement.value()
        elif mod & Qt.ControlModifier: factor = settings.spinZoomCtrlIncrement.value()
        else: factor = settings.spinZoomIncrement.value()   # defined twice as a slight optimization for normal zooming
        increment = (zoom / factor)
        self.setZoom(zoom + (increment if add else -increment), globalPos=QtGui.QCursor().pos())


    def resizeEvent(self, event: QtGui.QResizeEvent):
        ''' Scales the GIF/image/art while resizing, and calculates
            what zoom factor the new player size should start from. '''
        if self.hasScaledContents(): return
        if not self.zoomed:
            if self.pixmap(): self._calculateBaseZoom()
            elif self.movie():
                if self._gifScale == 1: self._resizeMovieFit()
                self._resetMovieCache()
                self._calculateBaseZoom()
        elif self._gifScale == 2:
            self.gif.setScaledSize(self.size().scaled(self.gifSize, Qt.KeepAspectRatio) * self.zoom)
            self._resetMovieCache()


    def timerEvent(self, event: QtCore.QTimerEvent):        # TODO why is zooming out so slow at lower smoothZoomFactors??
        if self._smoothZoomTimerID is not None:
            currentZoom = self.zoom
            if self._targetZoom == currentZoom:
                self._smoothZoomTimerID = self.killTimer(self._smoothZoomTimerID)
                self.setZoom(self._targetZoom, pos=self._smoothZoomPos, _smooth=True)
                #if self.movie(): self._resetMovieCache()    # only reset gif cache after smooth zoom is finished
            else:
                digits = 4 - (int(math.log10(self._targetZoom)) + 1)                        # smaller zoom, round to more digits
                newZoom = round(currentZoom + (self._targetZoom - currentZoom) * self._smoothZoomFactor, digits)
                if newZoom == currentZoom: newZoom = self._targetZoom
                self.setZoom(newZoom, pos=self._smoothZoomPos, _smooth=True)
        return super().timerEvent(event)


    def paintEvent(self, event: QtGui.QPaintEvent):
        if self.pixmap():
            painter = QtGui.QPainter(self)
            if settings.checkScaleFiltering.isChecked():
                painter.setRenderHint(QtGui.QPainter.Antialiasing)
                painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
                transformMode = Qt.SmoothTransformation
            else: transformMode = Qt.FastTransformation

            # draw zoomed pixmap by using scale mode and the current zoom to generate new size
            scale = self._artScale if self.isCoverArt else self._imageScale
            if self.zoomed:
                zoom = self.zoom

                # at >1 zoom, drawing to QRect is MUCH faster and looks identical to art.scaled()
                try:
                    if zoom >= 1:
                        if settings.checkZoomPrecise.isChecked():
                            if scale == 2: size = self.size().scaled(self.art.size(), Qt.KeepAspectRatio) * zoom
                            else: size = QtCore.QSizeF(self.art.size()) * zoom
                            painter.drawPixmap(QtCore.QRectF(self.pixmapPos, size).toRect(), self.art)
                        else:
                            if scale == 2: size = self.size().scaled(self.art.size(), Qt.KeepAspectRatio) * zoom
                            else: size = self.art.size() * zoom
                            painter.drawPixmap(QtCore.QRect(self.pixmapPos, size), self.art)    # TODO can this deform the image while zooming?
                        #painter.scale(zoom, zoom)                                              # TODO painter.scale() vs. QRect() -> which is faster?
                        #painter.drawPixmap(self.pixmapPos / zoom, self.art)

                    # at <1 zoom, art.scaled() looks MUCH better and the performance drop is negligible
                    else:
                        if scale == 2:
                            size = self.size().scaled(self.art.size(), Qt.KeepAspectRatio) * zoom
                            aspectRatioMode = Qt.IgnoreAspectRatio
                        else:
                            size = self.art.size() * zoom
                            aspectRatioMode = Qt.KeepAspectRatio
                        painter.drawPixmap(self.pixmapPos, self.art.scaled(size, aspectRatioMode, transformMode))
                except TypeError: logger.warning('QVideoPlayerLabel paintEvent failed due to mismatched pixmapPos type.')

            # draw normal pixmap. NOTE: for fill-mode, drawing to a QRect NEVER looks identical (it's much worse)
            else:
                #scale = self._artScale if self.isCoverArt else self._imageScale
                if scale == 0:                          # 0 -> no scaling
                    self.pixmapPos = self.rect().center() - self.art.rect().center()
                    painter.drawPixmap(self.pixmapPos, self.art)
                elif scale == 1:                        # 1 -> fit
                    scaledPixmap = self.art.scaled(self.size(), Qt.KeepAspectRatio, transformMode)
                    self.pixmapPos = self.rect().center() - scaledPixmap.rect().center()
                    painter.drawPixmap(self.pixmapPos, scaledPixmap)
                elif scale == 2:                        # 2 -> fill
                    self.pixmapPos = QtCore.QPoint()
                    painter.drawPixmap(0, 0, self.art.scaled(self.size(), transformMode=transformMode))
        else: super().paintEvent(event)




class QVideoSlider(QtW.QSlider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)   # TODO is having stuff like this here better than in the .ui file?

        self.last_mouseover_time = 0
        self.last_mouseover_pos = None
        self.clamp_minimum = False
        self.clamp_maximum = False
        self.grabbing_clamp_minimum = False
        self.grabbing_clamp_maximum = False

        self.hover_font_color: QtGui.QColor = None
        self.colors: list[Color] = None
        self.color_index = 0
        self.color_order = (Color('red'), Color('blue'), Color('lime'))

    # pass keystrokes through to parent
    def keyPressEvent(self, event: QtGui.QKeyEvent):   return gui.keyPressEvent(event)
    def keyReleaseEvent(self, event: QtGui.QKeyEvent): return gui.keyReleaseEvent(event)


    def paintEvent(self, event: QtGui.QPaintEvent):
        ''' Paints timestamps under the mouse cursor corresponding with its position while hovering over the slider.
            Due to the need for the cursor's up-to-date position regardless '''
        super().paintEvent(event)   # perform built-in paint immediately so we can paint on top
        now = time.time()

        # handle QVideoPlayer's idle cursor/fullscreen controls timeout
        try:
            vlc = gui.vlc
            fade_time = max(settings.spinFullScreenFadeDuration.value(), 0.01)  # 0.01 seconds looks instant while avoiding 0-division (no flicker issues)
            current_opacity = gui.dockControls.windowOpacity()
            min_opacity = settings.spinFullScreenMinOpacity.value() / 100
            max_opacity = settings.spinFullScreenMaxOpacity.value() / 100
        except: return
        try:
            # we keep track of lock_fullscreen_ui manually instead of repeatedly calling gui.dockControls.underMouse()
            # TODO ^^^ is this actually faster, or is underMouse() always kept track of internally?
            if vlc.last_move_time and not gui.lock_fullscreen_ui and vlc.last_move_time + settings.spinHideIdleCursorDuration.value() <= now:
                vlc.setCursor(Qt.BlankCursor)
                if current_opacity > min_opacity:
                    opacity_increment = max_opacity / (fade_time * gui.frame_rate_rounded)
                    gui.dockControls.setWindowOpacity(max(current_opacity - opacity_increment, min_opacity))
            else:
                vlc.unsetCursor()
                if current_opacity < max_opacity:
                    opacity_increment = max_opacity / (fade_time * gui.frame_rate_rounded)
                    gui.dockControls.setWindowOpacity(min(current_opacity + opacity_increment, max_opacity))
        except:
            variables = f'fade_time={fade_time} current_opacity={current_opacity} min_opacity={min_opacity} max_opacity={max_opacity} frame_rate_rounded={gui.frame_rate_rounded}'
            logger.warning(f'(!) Unexpected error while handling idle-timeout - {variables} - {format_exc()}')

        p = QtGui.QPainter()
        p.begin(self)
        try:
            # trim start/end markers
            if self.clamp_minimum or self.clamp_maximum:        # draw trim-boundaries
                if not self.colors:
                    next_index = self.color_index + 1
                    if next_index > len(self.color_order) - 1: next_index = 0
                    self.colors = list(self.color_order[next_index].range_to(self.color_order[self.color_index], int(gui.frame_rate * 4)))
                    self.color_index = next_index
                color = QtGui.QColor(self.colors.pop().get_hex())
                color.setAlpha(100)
                pen_thick = QtGui.QPen(color, 2)
                pen_thin = QtGui.QPen(QtGui.QColor(255, 255, 255), 1)
                #pen_thick.setCapStyle(Qt.RoundCap)
                p.setBrush(QtGui.QColor(0, 0, 0, 200))

                opt = QtW.QStyleOptionSlider()
                self.initStyleOption(opt)
                groove_rect = self.style().subControlRect(QtW.QStyle.CC_Slider, opt, QtW.QStyle.SC_SliderGroove, self)
                #print(groove_rect, groove_rect.left(), groove_rect.topLeft(), dir(groove_rect))

                # draw triangle markers for start/end and cover slider outside trim
                if self.clamp_minimum:
                    x = self.rangeValueToPixelPos(gui.minimum)
                    p.setPen(pen_thick)
                    p.drawRoundedRect(groove_rect.left(), groove_rect.top(), x, groove_rect.height(), 2, 2)
                    p.setPen(pen_thin)
                    p.drawPolygon(QtGui.QPolygon([QtCore.QPoint(x, 2), QtCore.QPoint(x, self.height() - 2), QtCore.QPoint(x - 4, self.height() / 2)]))
                if self.clamp_maximum:
                    x = self.rangeValueToPixelPos(gui.maximum)
                    p.setPen(pen_thick)
                    p.drawRoundedRect(x, groove_rect.top(), groove_rect.width() - x - 1, groove_rect.height(), 2, 2)
                    p.setPen(pen_thin)
                    p.drawPolygon(QtGui.QPolygon([QtCore.QPoint(x, 2), QtCore.QPoint(x, self.height() - 2), QtCore.QPoint(x + 4, self.height() / 2)]))

            #for marker in self.markers:    # an idea for a more general implementation with an arbitrary number of "markers"
            #    x = self.rangeValueToPixelPos(marker)
            #    #print(x)
            #    #p.drawImage(pos, 0, QtGui.QImage(r'C:\cs\python\videoeditor\bin\icon.ico'))
            #    p.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 1))
            #    p.setBrush(QtGui.QColor(255, 255, 255))
            #    #p.drawLine(x, 0, x, self.height())
            #    p.drawPolygon(QtGui.QPolygon([QtCore.QPoint(x, 0), QtCore.QPoint(x, self.height()), QtCore.QPoint(x + 4, self.height() / 2)]))

            # hover timestamps
            if not settings.groupHover.isChecked(): return                          # hover-timestamps are disabled -> return
            fade_time = max(settings.spinHoverFadeDuration.value(), 0.05)           # 0.05 looks instant but avoids flickers
            if now <= self.last_mouseover_time + fade_time:
                if self.underMouse():                                               # reset fade timer if we're still hovering
                    pos = self.mapFromGlobal(QtGui.QCursor().pos())                 # get position relative to widget
                    self.last_mouseover_time = now
                    self.last_mouseover_pos = pos                                   # save last mouse position within slider
                else: pos = self.last_mouseover_pos                                 # use last position if mouse is outside the slider

                frame = self.pixelPosToRangeValue(pos)
                h, m, s, _ = get_hms(round(gui.duration * (frame / gui.frame_count), 2))
                text = f'{m}:{s:02}' if gui.duration < 3600 else f'{h}:{m:02}:{s:02}'

                size = settings.spinHoverFontSize.value()
                font = settings.comboHoverFont.currentFont()    # TODO use currentFontChanged signals + more for performance? not needed?
                font.setPointSize(size)
                #font.setPixelSize(size)
                p.setFont(font)
                pos.setY(self.height() - (self.height() - size) / 2)

                # calculate fade-alpha from 0-255 based on time since we stopped hovering. default to 255 if fading is disabled
                # TODO: I sure used a lot of different methods for fading things. should these be more unified?
                alpha = (self.last_mouseover_time + fade_time - now) * (255 / fade_time) if fade_time != 0.05 else 255

                if settings.checkHoverShadow.isChecked():
                    p.setPen(QtGui.QColor(0, 0, 0, alpha))      # set color to black
                    p.drawText(pos.x() + 1, pos.y() + 1, text)  # draw shadow first
                self.hover_font_color.setAlpha(alpha)
                p.setPen(self.hover_font_color)                 # set color to white
                p.drawText(pos, text)                           # draw actual text over shadow

                # my idea for using tooltips for displaying the time. works, but qt's tooltips don't refresh fast enough
                #h, m, s, _ = get_hms(round(gui.duration * (frame / gui.frame_count), 2))
                #if gui.duration < 3600: self.setToolTip(f'{m}:{s:02}')
                #else: self.setToolTip(f'{h}:{m:02}:{s:02}')    # use cleaner format for time-strings on videos > 1 hour
        finally: p.end()


    def wheelEvent(self, event: QtGui.QWheelEvent):             # https://doc.qt.io/qt-5/qabstractslider.html#SliderAction-enum
        ''' Page-steps along the slider while scrolling. Horizontal sliders are increased by
            scrolling down or right, vertical sliders are increased by scrolling up or left. '''
        add = event.angleDelta().y() > 0 or event.angleDelta().x() > 0
        if self.orientation() == Qt.Vertical: add = not add
        self.triggerAction(4 if add else 3)
        event.accept()


    def enterEvent(self, event: QtGui.QEnterEvent):
        ''' Marks the current time when mousing-over and forces a paintEvent to begin drawing hover-timestamps.
            Does not require setMouseTracking(True), as enterEvent fires regardless. '''
        if gui.video:
            self.last_mouseover_time = time.time()              # save last mouseover time to use as a fade timer
            self.update()                                       # force-update to draw timestamp in self.paintEvent()
        return super().enterEvent(event)


    def mousePressEvent(self, event: QtGui.QMouseEvent):
        ''' Snaps the slider handle to the mouse cursor if left-clicked. Does not use the normal implementation
            to grab the handle, instead allowing it to move freely until the mouse is moved, ensuring a snappier
            experience when clicking the progress bar. Does not emit the sliderPressed signal. '''
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            frame = self.pixelPosToRangeValue(pos)
            if gui.minimum < frame < gui.maximum:
                self.update_parent_progress(frame)

            # https://stackoverflow.com/questions/40100733/finding-if-a-qpolygon-contains-a-qpoint-not-giving-expected-results
            if self.clamp_minimum or self.clamp_maximum:        # ^ alternate solution by finding points inside QPolygons
                radius = 12                                     # 12 pixel radius for the handle
                if self.clamp_minimum:
                    min_pos = self.rangeValueToPixelPos(gui.minimum)
                    if min_pos - radius < pos.x() < min_pos + radius:
                        self.grabbing_clamp_minimum = True
                        self.grabbing_clamp_maximum = False
                        return                                  # return to skip repeating process for maximum
                if self.clamp_maximum:
                    max_pos = self.rangeValueToPixelPos(gui.maximum)
                    if max_pos - radius < pos.x() < max_pos + radius:
                        self.grabbing_clamp_minimum = False
                        self.grabbing_clamp_maximum = True
            #if abs(delta) > 0.025: self.setValue(new_value)    # only change if difference between new/old positions is greater than 2.5%


    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        ''' If dragging, this re-implements scrubbing by grabbing the handle, pausing the player, and updating
            the player position. Does not emit the sliderMoved signal. Does not require setMouseTracking(True),
            as mouse-tracking only applies to firing mouseMoveEvent without holding a button. '''
        frame = self.pixelPosToRangeValue(event.pos())          # get frame
        if app.mouseButtons() == Qt.LeftButton:                 # abnormal mousePressEvent implementation, so event.button() is incorrect
            self.update_parent_progress(frame)                  # "grab" handle
            gui.player.set_pause(True)                          # pause player while scrubbing
            self.last_mouseover_time = 0                        # reset last mouseover time to stop drawing timestamp immediately
            if self.grabbing_clamp_minimum: gui.set_trim_start()
            elif self.grabbing_clamp_maximum: gui.set_trim_end()
        #self.update()      # TODO <- why doesn't this make the animations smooth?


    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        ''' Unpauses the player after scrubbing, unless it was paused originally. Does not emit the sliderReleased signal. '''
        if gui.restarted and settings.checkNavigationUnpause.isChecked(): gui.pause()   # auto-unpause after restart
        else: gui.player.set_pause(False or gui.is_paused)                              # stay paused if we were paused
        self.grabbing_clamp_minimum = False
        self.grabbing_clamp_maximum = False
        #if 0 <= event.x() <= self.width() and 0 <= event.y() <= self.height():
        if self.underMouse(): self.last_mouseover_time = time.time()    # resume drawing timestamp after release
        frame = self.pixelPosToRangeValue(event.pos())                  # get frame
        if frame < gui.minimum: self.update_parent_progress(gui.minimum)
        elif frame > gui.maximum: self.update_parent_progress(gui.maximum)


    def pixelPosToRangeValue(self, pos: QtCore.QPoint) -> int:          # https://stackoverflow.com/questions/52689047/moving-qslider-to-mouse-click-position
        ''' Auto-magically detects the correct value to set the handle to based on a given `pos`.
            Works with horizontal and vertical sliders, with or without stylesheets. '''
        try:
            opt = QtW.QStyleOptionSlider()
            self.initStyleOption(opt)

            groove_rect = self.style().subControlRect(QtW.QStyle.CC_Slider, opt, QtW.QStyle.SC_SliderGroove, self)
            handle_rect = self.style().subControlRect(QtW.QStyle.CC_Slider, opt, QtW.QStyle.SC_SliderHandle, self)
            try: raw_position = pos - handle_rect.center() + handle_rect.topLeft()
            except TypeError: pos = self.mapFromGlobal(QtGui.QCursor().pos())   # event.pos() becomes None in rare, unknown circumstances

            if self.orientation() == Qt.Horizontal:
                slider_min = groove_rect.x()
                slider_max = groove_rect.right() - handle_rect.width() + 1
                new_position = raw_position.x() - slider_min
            else:
                slider_min = groove_rect.y()
                slider_max = groove_rect.bottom() - handle_rect.height() + 1
                new_position = raw_position.y() - slider_min

            return QtW.QStyle.sliderValueFromPosition(
                self.minimum(),             # min
                self.maximum(),             # max
                new_position,               # position
                slider_max - slider_min,    # span
                opt.upsideDown              # upsideDown
            )
        except:
            logger.warning(f'(!) Unexpected error in pixelPosToRangeValue - {format_exc()}')
            return 0                        # return 0 as a failsafe


    def rangeValueToPixelPos(self, value: int) -> int:
        ''' Auto-magically detects the correct X/Y position to set the handle to based on a given `value`.
            Works with horizontal and vertical (...? see TODO below) sliders, with or without stylesheets. '''
        opt = QtW.QStyleOptionSlider()
        self.initStyleOption(opt)

        groove_rect = self.style().subControlRect(QtW.QStyle.CC_Slider, opt, QtW.QStyle.SC_SliderGroove, self)
        handle_rect = self.style().subControlRect(QtW.QStyle.CC_Slider, opt, QtW.QStyle.SC_SliderHandle, self)

        is_horizontal = self.orientation() == Qt.Horizontal
        if is_horizontal:
            slider_min = groove_rect.x()
            slider_max = groove_rect.right() - handle_rect.width() + 1
        else:
            slider_min = groove_rect.y()
            slider_max = groove_rect.bottom() - handle_rect.height() + 1

        raw_position = QtW.QStyle.sliderPositionFromValue(
            self.minimum(),                 # min
            self.maximum(),                 # max
            value,                          # position
            slider_max - slider_min,        # span
            opt.upsideDown                  # upsideDown
        )

        if is_horizontal: return raw_position + handle_rect.center().x() - handle_rect.topLeft().x()
        else: return raw_position + handle_rect.center().y() - handle_rect.topLeft().y()    # TODO test this on vertical



# ------------------------------------------
# Concatenation Widgets
# ------------------------------------------
class QVideoList(QtW.QListWidget):          # TODO this likely is not doing any garbage collection
    ''' A list of interactable media files represented by QVideoListItemWidgets within the concatenation menu. '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)


    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):     # drag and drop requires self.setAcceptDrops(True)
        if event.mimeData().hasUrls(): event.accept()
        else: event.ignore()
        super().dragEnterEvent(event)                           # run QWidget's built-in behavior


    def dropEvent(self, event: QtGui.QDropEvent):
        ''' Handles adding externally dropped items to the list, and includes an ugly workaround for a Qt bug that creates
            duplicated and/or invisible items when dragging an item below itself without actually changing its final position. '''
        old_items = tuple(qthelpers.listGetAllItems(self))
        files = tuple(url.toLocalFile() for url in event.mimeData().urls())
        if files: self.add(files=files)
        super().dropEvent(event)            # run QWidget's built-in behavior
        if not files:                       # if there were no files, assume we did an internal drag/drop
            event.ignore()                  # ignoring the event somehow prevents original item from getting deleted
            for item in qthelpers.listGetAllItems(self):        # cycle through items and
                if item not in old_items:                       # look for "new" item that appeared
                    garbage = self.takeItem(self.row(item))     # delete corrupted item
                    del garbage


    def contextMenuEvent(self, event: QtGui.QContextMenuEvent):
        ''' Creates a context menu for the QListWidgetItem underneath the mouse, if any.
            This could alternatively be accomplished through the itemClicked signal. '''
        item = self.itemAt(event.pos())     # get item under mouse to work with
        if not item: return                 # no item under mouse, return

        action1 = QtW.QAction('&Play')
        action1.triggered.connect(lambda: gui.open(item.toolTip()))
        action2 = QtW.QAction('&Explore')
        action2.triggered.connect(lambda: qthelpers.openPath(item.toolTip(), explore=True))
        action3 = QtW.QAction('&Remove')
        action3.triggered.connect(lambda: qthelpers.listRemoveSelected(self))

        context = QtW.QMenu(self)
        context.addActions((action1, action2, action3))
        context.exec(event.globalPos())


    def add(self, *args, files=None, index=None):
        if files is None: files, cfg.lastdir = qthelpers.browseForFiles(lastdir=cfg.lastdir,
                                                                        caption='Select video to add',
                                                                        filter='MP4 files (*.mp4);;All files (*)')
        elif isinstance(files, str): files = (files,)

        # create QVideoListItemWidgets on top of QListWidgetItems for each file
        thumbnails_needed = []
        for video in files:
            thumbnail_name = get_unique_path(os.path.basename(video).replace('/', '.').replace('\\', '.'))
            thumbnail_path = os.path.join(constants.THUMBNAIL_DIR, f'{thumbnail_name}_thumbnail.jpg')
            last_modified = time.strftime('%#m/%#d/%y | %#I:%M:%S%p', time.localtime(os.path.getmtime(video))).lower()
            html = f'<html><head/><body><p style="line-height:0.5"><span style="font-family:Yu Gothic; font-size:12pt;">{os.path.basename(video)}</span></p><p><span style="color:#676767;">{last_modified}</span></p></body></html>'
            item_widget = QVideoListItemWidget(self, thumbnail_path, html, video == gui.video)

            # create and setup QListWidgetItem as the base for our QVideoListItemWidget with our file and QLabel
            if index is not None:   # {index} is used exclusively for moving items (which requires the workaround too)
                item_base = QtW.QListWidgetItem()
                self.insertItem(index, item_base)
            else: item_base = QtW.QListWidgetItem(self)
            item_base.setToolTip(video)
            self.setItemWidget(item_base, item_widget)
            item_base.setSizeHint(QtCore.QSize(0, 64))          # default width/height is -1, but this is invalid. yeah.

            # check if thumbnail actually existed or not
            if not os.path.exists(thumbnail_path):              # check if thumbnail existed or not
                thumbnails_needed.append((thumbnail_path, video, item_widget))

        # ensure thumbnail folder exists, then create threads to generate thumbnails
        if not os.path.exists(constants.THUMBNAIL_DIR): os.makedirs(constants.THUMBNAIL_DIR)
        for thumbnail_needed in thumbnails_needed:              # TODO: there needs to be some way of cancelling these threads
            Thread(target=self.get_thumbnail, args=thumbnail_needed, daemon=True).start()


    def get_thumbnail(self, thumbnail_path, video, item_widget):
        ''' Generates a thumbnail for a given `video`, saves to `thumbnail_path`,
            and updates the QVideoListItemWidget `item_widget` with the thumbnail.
            constants.FFMPEG is verified beforehand and assumed to be valid. '''
        temp_path = thumbnail_path.replace('_thumbnail', '_thumbnail_unscaled')
        ffmpeg(f'-ss 3 -i "{video}" -vframes 1 "{temp_path}"')                      # generate thumbnail from 3 seconds in
        ffmpeg(f'-i "{temp_path}" -vf scale=-1:56 "{thumbnail_path}"')              # resize thumbnail
        logger.info(f'Generating thumbnail for "{video}" to "{temp_path}"')
        item_widget.thumbnail.setPixmap(QtGui.QPixmap(thumbnail_path))
        try: os.remove(temp_path)
        except Exception as error: logger.warning(f'Could not delete temporary thumbnail {temp_path} - {error}')


    def move(self, *args, down=False):
        indexes = sorted(self.row(item) for item in self.selectedItems())
        if down: indexes = reversed(indexes)
        for old_index in indexes:
            new_index = old_index + (1 if down else -1)
            new_index = min(self.count() - 1, max(0, new_index))
            if old_index != new_index:
                self.add(files=self.takeItem(old_index).toolTip(), index=new_index)  # same corrupted item bug affects moving items
                self.item(new_index).setSelected(True)


    def __iter__(self):
        for i in range(self.count()):
            yield self.item(i)


    #def __contains__(self, other):          # TODO unused
    #    for item in qthelpers.listGetAllItems(self):
    #        if item == other:
    #            return True
    #    return False




class QVideoListItemWidget(QtW.QWidget):  # TODO this likely does not get garbage collected
    ''' An item representing a media file within a QVideoList, within the concatenation menu. '''
    def __init__(self, parent, image, text, is_playing):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)     # required for dragging to work
        self.layout = QtW.QHBoxLayout()
        self.setLayout(self.layout)

        self.thumbnail = QtW.QLabel(self)
        self.thumbnail.setPixmap(QtGui.QPixmap(image))
        self.thumbnail.setAlignment(Qt.AlignCenter)
        if not is_playing: self.thumbnail.setStyleSheet('QLabel { padding: 4px; }')
        else: self.thumbnail.setStyleSheet('QLabel { padding: 4px;background-color: qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0.573864 rgba(0,255,255,255),stop:1 rgba(0,0,119,255)); }')

        self.label = QtW.QLabel(text, self)
        #self.label.setStyleSheet('QLabel { padding-left: 1px; }')
        #self.layout.addSpacerItem(QtW.QSpacerItem(2, 20, QtW.QSizePolicy.Fixed, QtW.QSizePolicy.Minimum))

        self.layout.addWidget(self.thumbnail)
        self.layout.addWidget(self.label)
        self.layout.addSpacerItem(QtW.QSpacerItem(40, 20, QtW.QSizePolicy.Expanding, QtW.QSizePolicy.Minimum))
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(1, 0, 0, 0)



# ------------------------------------------
# Utility Widgets
# ------------------------------------------
class QKeySequenceFlexibleEdit(QtW.QKeySequenceEdit):
    ''' QKeySequenceEdit which supports limiting to a single sequence, ignorable sequences, customizable editing
        delays, clearing focus/sequences with Esc, a clear button, and easier access to the underlying QLineEdit. '''
    def __init__(self, *args, singleSequence=True, escClearsFocus=True, escClearsSequence=True, clearButton=False, delay=200, ignored=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._timerID = None
        self._editing = False
        self.lineEdit = self.children()[0]
        self.setClearButtonEnabled(clearButton)
        self.singleSequence = singleSequence
        self.escClearsFocus = escClearsFocus
        self.escClearsSequence = escClearsSequence
        self.editDelay = delay
        self.ignoredSequences = (               # like the other utility widgets, we manually set this here for simplicity
            QtGui.QKeySequence('Ctrl+O'),
            QtGui.QKeySequence('Ctrl+S'),
            QtGui.QKeySequence('Ctrl+Shift+S'),
            QtGui.QKeySequence('Alt+Q')
        )


    def setSingleSequence(self, state: bool): self.singleSequence = state
    def setEscClearsFocus(self, state: bool): self.escClearsFocus = state
    def setEscClearsSequence(self, state: bool): self.escClearsSequence = state
    def setEditDelay(self, delay: int): self.editDelay = delay
    def setIgnoredSequences(self, *args: QtGui.QKeySequence): self.ignoredSequences = args
    def setClearButtonEnabled(self, state: bool):
        ''' Toggles and connects the clear button for the underlying QLineEdit based on `state`. When disabling,
            the QAction and QToolButton that make up the clear button are automatically discarded by Qt. '''
        self.lineEdit.setClearButtonEnabled(state)
        if state: self.lineEdit.children()[1].triggered.connect(self.clear)


    def clear(self):
        ''' Overrides the clear() method to manually emit keySequenceChanged and editingFinished signals, assuming
            clear() was not called as part of an editing timer. This allows clearing to actually trigger updates. '''
        super().clear()
        if self._timerID is None:               # timerID means a custom timer active
            self.keySequenceChanged.emit(self.keySequence())
            self.editingFinished.emit()


    def keyPressEvent(self, event: QtGui.QKeyEvent):
        ''' If `escClearsFocus` is set, focus is cleared and returned after Esc is pressed. If `singleSequence` is set,
            sequences are truncated to their last sequence, and ", ..." is stripped from the underlying QLineEdit. '''
        if event.key() == Qt.Key_Escape:                                # clear text/focus on Esc
            if self.escClearsSequence: self.clear()
            if self.escClearsFocus: return self.clearFocus()            # do NOT use event.ignore() here

        if self.singleSequence:                 # single sequence only
            super().keyPressEvent(event)        # run built-in keyPressEvent first (this emits keySequenceChanged)
            if self.keySequence().count() > 1:
                self.setKeySequence(QtGui.QKeySequence(self.keySequence()[-1]))  # truncate sequence to last sequence
            return self.lineEdit.setText(self.keySequence().toString())          # strip ", ..." from underlying QLineEdit and return

        elif self.editDelay != 1000:            # not a single sequence, but a custom editing delay (reimplement timer behavior)
            if self._timerID is None:           # no timer running + not actively editing -> clear existing sequence for incoming sequence
                if not self._editing:
                    self.clear()
            else:                               # timer running + actively editing the sequence -> kill/reset timer (we're still editing)
                self._timerID = self.killTimer(self._timerID)
            self._editing = True                # mark that we're actively editing
        super().keyPressEvent(event)            # run built-in keyPressEvent last (this emits the first keySequenceChanged signal)


    def keyReleaseEvent(self, event: QtGui.QKeyEvent):
        ''' Clears the entire field if it contains an ignored sequence. If `singleSequence` is set, the
            `editingFinished` signal is emitted immediately and the normal timer is skipped. Otherwise,
            if a custom `editDelay` is set, then QKeySequenceEdit's edit-finished-timer is reimplemented. '''
        if self.ignoredSequences and self.keySequence() in self.ignoredSequences: self.clear()
        if self.singleSequence: return self.editingFinished.emit()
        elif self.editDelay != 1000:
            self._editing = False
            if self._timerID is not None: self.killTimer(self._timerID)
            self._timerID = self.startTimer(self.editDelay, Qt.CoarseTimer)
        else: return super().keyReleaseEvent(event)


    def timerEvent(self, event: QtCore.QTimerEvent):
        ''' Finishes the reimplementation of QKeySequenceEdit's edit-finished-timer for
            custom `editDelay` values. This doesn't fire if `singleSequence` is set. '''
        if self._timerID is not None:                                   # timerID means a custom timer active
            self.keySequenceChanged.emit(self.keySequence())            # emit second keySequenceChanged signal
            self.editingFinished.emit()
            self._timerID = self.killTimer(self._timerID)               # kill timer and remove ID
            self.lineEdit.setText(self.keySequence().toString())        # strip ", ..." from underlying QLineEdit
        return super().timerEvent(event)




class QWidgetPassthrough(QtW.QWidget):
    ''' QWidget which passes desired keypresses to its parent. Specific
        characters can be ignored, and specific categories (such as letters,
        integers, and punctuation) can be toggled. The option to clear or
        optionally "pass" focus when Esc is pressed is also included. '''
    base = QtW.QWidget      # TODO semi-bandaid fix. without this, we can't access the correct keyPressEvent in subclasses(...?)

    # TODO make the getting/setting syntax fully Qt-like or make it fully normal
    def __init__(self, *args, proxy=None, escClearsFocus=True, passFocus=True,
                 alpha=True, punctuation=True, numeric=False, ignored=tuple(), **kwargs):
        super().__init__(*args, **kwargs)       # normally these kwargs are True, False, False, False
        self.escClearsFocus = escClearsFocus
        self.passFocus = passFocus
        self.ignoreAlpha = alpha
        self.ignorePunctuation = punctuation
        self.ignoreNumeric = numeric
        self.ignoredKeys = ignored
        if proxy:
            self._proxyWidget = proxy
            self._proxyWidgetIsParent = False
        else:
            self._proxyWidget = self.parent()
            self._proxyWidgetIsParent = True

    def proxyWidget(self):  # pointless, but consistent with Qt
        return self._proxyWidget

    def setProxyWidget(self, widget: QtW.QWidget):
        ''' Manually sets `proxyWidget`. The proxy widget is the `widget` that
            receives the this widget's keypresses that are otherwise discarded. '''
        self._proxyWidget = widget
        self._proxyWidgetIsParent = widget is self.parent()

    def setParent(self, parent):
        ''' Captures setParent and sets `proxyWidget` to the new `parent`
            if our proxy widget and parent are expected to be linked. '''
        super().setParent(parent)
        if self._proxyWidgetIsParent:
            self._proxyWidget = parent

    def setIgnoreAll(self, ignore: bool):
        self.ignoreAlpha = ignore
        self.ignorePunctuation = ignore
        self.ignoreNumeric = ignore

    def setEscClearsFocus(self, state: bool): self.escClearsFocus = state
    def setPassFocus(self, state: bool): self.passFocus = state
    def setIgnoreAlpha(self, ignore: bool): self.ignoreAlpha = ignore
    def setIgnorePunctuation(self, ignore: bool): self.ignorePunctuation = ignore
    def setIgnoreNumeric(self, ignore: bool): self.ignoreNumeric = ignore
    def setIgnoredKeys(self, *args): self.ignoredKeys = args

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        key = event.key()
        if self.escClearsFocus and key == 16777216:         # esc (clear/pass focus)
            if self.passFocus: return self._proxyWidget.setFocus()
            else: return self.clearFocus()
        text = event.text()
        if any((key in self.ignoredKeys,
                self.ignoreAlpha and text.isalpha(),
                self.ignorePunctuation and text in '!"#$%&\'()*+, -./:;<=>?@[\\]^_`{|}~',
                self.ignoreNumeric and text.isnumeric())):
            self._proxyWidget.shortcut_bandaid_fix = True   # TODO this is a workaround for QShortcuts refusing to work through this widget. no QShortcut...
            return self._proxyWidget.keyPressEvent(event)   # ...contexts work. I might replace the QShortcuts with a simpler system, or I may leave it like this.
        return self.base.keyPressEvent(self, event)




class QSpinBoxPassthrough(QtW.QSpinBox, QWidgetPassthrough): base = QtW.QSpinBox
class QDockWidgetPassthrough(QtW.QDockWidget, QWidgetPassthrough): base = QtW.QDockWidget
class QLineEditPassthrough(QtW.QLineEdit, QWidgetPassthrough): base = QtW.QLineEdit



class QDraggableWindowFrame(QtW.QFrame):
    ''' Widget which moves a separate widget called the `dragTarget` while dragging on empty spaces, if dragged using
        `button`. If `button` is None, then any click on the widget will move the `dragTarget`. The target widget
        is moved relative to this widget, and does not move while fullscreen or maximized. If no `dragTarget` is
        specified, parent() is used instead, which persists through setParent() until a unique dragTarget is set. '''
    def __init__(self, *args, dragTarget: QtW.QWidget = None, button: int = Qt.LeftButton, **kwargs):
        super().__init__(*args, **kwargs)
        if dragTarget:
            self._dragTarget = dragTarget
            self._dragTargetIsParent = False
        else:
            self._dragTarget = self.parent()
            self._dragTargetIsParent = True
        self._button = button
        self._validDrag = False
        self._draggingOffset: QtCore.QPoint = None

    def dragTarget(self):   # pointless, but consistent with Qt
        return self._dragTarget

    def setDragTarget(self, widget: QtW.QWidget):
        ''' Manually sets `dragTarget`. The drag target is the `widget` that gets moved while dragging `self`. '''
        self._dragTarget = widget
        self._dragTargetIsParent = widget is self.parent()

    def button(self):       # pointless, but consistent with Qt
        return self._button

    def setButton(self, button: int):
        self._button = button

    def setParent(self, parent):
        ''' Captures setParent and sets `dragTarget` to the new `parent`
            if our drag target and parent are expected to be linked. '''
        super().setParent(parent)
        if self._dragTargetIsParent:
            self._dragTarget = parent

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        ''' Confirms that a mouse press is valid for dragging and obtains the offset between the click
            and the top-left corner of our target. Ignore clicks while our target is fullscreened or
            maximized. This event does not fire if we've clicked one of our child widgets. '''
        valid_button = self._button is None or event.button() == self._button
        self._validDrag = not self._dragTarget.isFullScreen() and not self._dragTarget.isMaximized() and valid_button
        self._draggingOffset = event.globalPos() - self._dragTarget.pos()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        ''' If valid, moves our target relative to our mouse's movement using the offset obtained in mousePressEvent. '''
        if not self._validDrag: return    # do not move dragTarget if we're dragging a child widget
        self._dragTarget.move(event.globalPos() - self._draggingOffset)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        self._validDrag = False


# ------------------------------------------
# Unfinished/Unused Widgets
# ------------------------------------------
''' Currently unfinished. Intended to "simplify" the cropping process as well as
    draw the cropping coordinates/border over the frames, instead of underneath. '''
#class QCropFrame(QtW.QFrame):
#    def __init__(self, parent, vlc, index, alpha, *args, **kwargs):
#        super().__init__(parent, *args, **kwargs)
#        self.vlc = vlc
#        self.index = index
#        self.mousePressEvent = vlc.mousePressEvent
#        self.mouseMoveEvent = vlc.mouseMoveEvent
#        self.mouseReleaseEvent = vlc.mouseReleaseEvent
#        self.mouseDoubleClickEvent = vlc.mouseDoubleClickEvent
#        self.setMouseTracking(True)
#        self.setVisible(True)
#        self.setStyleSheet(f'background: rgba(0, 0, 0, {alpha})')
#        #self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
#
#
#    def paintEvent(self, event: QtGui.QPaintEvent):
#        super().paintEvent(event)
#        p = QtGui.QPainter()
#        p.begin(self)
#
#        white = QtGui.QColor(255, 255, 255)
#        black = QtGui.QColor(0, 0, 0)
#
#        p.setPen(QtGui.QPen(white, 6, Qt.SolidLine))
#        p.setBrush(white)
#        p.setFont(QtGui.QFont('Segoe UI Light', 10))
#        print('mapping...', self.vlc.selection, self.mapFrom, self.vlc)
#        print(self.mapFrom(self.vlc, self.vlc.selection[0]))    # mapFrom crashes with no errors
#        s = tuple(self.mapFrom(self.vlc, point) for point in self.vlc.selection)
#        print(1, self.vlc.selection)
#        print(2, s)
#        try:
#            # draw thin border around video (+2 and -4 to account for size-6 pen)
#            p.drawRect(s[0].x() + 2,
#                       s[0].y() + 2,
#                       s[1].x() - s[0].x() - 4,
#                       s[2].y() - s[0].y() - 4)
#
#            # draw handle and coordinates for each corner
#            index = self.index
#            point = s[index]
#            fpoint = self.vlc.last_factored_points[index] = self.vlc.factor_point(point)
#            #p.drawRect(point.x() - 3, point.y() - 3, 5, 5)
#            text = f'({fpoint.x():.0f}, {fpoint.y():.0f})'
#            p.setPen(black)                                                                    # set color to black
#            p.drawText(point.x() + 1, point.y() + self.vlc.text_y_offsets[index] + 1, text)    # draw shadow first
#            p.setPen(QtGui.QPen(white, 6, Qt.SolidLine))                                # set color to white
#            p.drawText(point.x(), point.y() + self.vlc.text_y_offsets[index], text)            # draw actual text over shadow
#            p.drawPoint(point.x(), point.y())                                                  # size-6 point to represent handles
#        except: print(format_exc())
#        p.end()




''' Unfinished QMediaPlayer variant of this project, just in case. Created 3/1/22. '''
#class QVideoPlayer2(QtW.QWidget):
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.last_move_time = 0
#
#        self.player = QtMultimedia.QMediaPlayer(None, QtMultimedia.QMediaPlayer.VideoSurface)
#
#        # VLC-style aliases for testing purposes
#        self.player.get_state = self.player.state
#        self.player.get_rate = self.player.playbackRate
#        self.player.set_rate = self.player.setPlaybackRate
#        self.player.get_position = lambda: (self.player.position() / 1000) / gui.duration
#        self.player.set_position = lambda pos: self.player.setPosition(pos * gui.frame_count * gui.delay)
#        self.player.audio_get_volume = self.player.volume
#        self.player.audio_set_volume = self.player.setVolume
#        self.player.audio_get_mute = self.player.isMuted
#        self.player.audio_set_mute = self.player.setMuted
#        self.player.get_fps = lambda: 60
#        self.player.get_length = lambda: 20 * 1000
#        self.player.is_playing = lambda: True
#        #self.player.pause = lambda: self.player.pause() if self.player.state() == QtMultimedia.QMediaPlayer.PlayingState else self.player.play()
#        self.player.set_pause = lambda paused: self.player.pause() if paused else self.player.play()
#        player_video = QtMultimediaWidgets.QVideoWidget(self.parent())
#        self.player.setVideoOutput(player_video)
#
#
#    def show_text(self, *args, **kwargs): ...
#    def get_state(self, *args, **kwargs): return self.player.state()
#
#
#    def play(self, file, _error=False):
#        try:
#            self.player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(file)))
#            self.player.play()
#            return True
#        except:
#            logger.warning(f'QMediaPlayer failed to play video {file}: {format_exc()}')
#            if not _error:  # _error ensures we only attempt to play previous video once
#                if not gui.video: self.player.stop()        # no previous video to play, so just stop playing
#                else: self.play(gui.video, _error=True)     # attempt to play previous working video
#            return False
#
#
#    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
#        ''' Pauses media after clicking and releasing left-click over player, ignoring clicks that were
#            dragged outside player. Releases dragged crop points/edges if needed, and resets cursor. '''
#        #print('mediaplayer release', self.dragging, self.panning)
#        if event.button() == Qt.LeftButton:                  # left click released
#            if self.underMouse():                                   # mouse wasn't dragged off player
#                gui.pause()
#
#
#    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent):      # fullscreen video by double-clicking on it (left-click only)
#        ''' Triggers GUI's toggle_fullscreen action after double-clicking the player. '''
#        if event.button() == Qt.LeftButton: gui.actionFullscreen.trigger()
#
#
#    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):         # accept drag if dragging files (requires self.setAcceptDrops(True))
#        ''' Accepts a cursor-drag if files are being dragged. Requires self.setAcceptDrops(True). '''
#        if event.mimeData().hasUrls(): event.accept()
#        else: event.ignore()
#        self.dragdrop_in_progress = True
#        super().dragEnterEvent(event)                               # run QWidget's built-in behavior
#
#
#    def dragLeaveEvent(self, event: QtGui.QDragLeaveEvent):
#        self.show_text('')
#        self.dragdrop_in_progress = False
#        super().dragLeaveEvent(event)
#
#
#    def dragMoveEvent(self, event: QtGui.QDragMoveEvent):
#        ''' Updates the statusbar to indicate what the currently held
#            button-combination will do once the drag-and-drop finishes. '''
#        if not gui.video:                   # no video is playing, don't bother showing special options
#            gui.statusbar.showMessage('Drop to play media, or hold ctrl/alt/shift while media is playing for additional options')
#        else:
#            mod = event.keyboardModifiers()
#            if mod & Qt.ControlModifier:     # ctrl (concat before current)
#                gui.statusbar.showMessage('Drop to concatenate before current media', 3000)
#                #self.show_text('Drop to concatenate before current media', 0)
#            elif mod & Qt.AltModifier:       # alt (concat after current)
#                gui.statusbar.showMessage('Drop to concatenate after current media', 3000)
#                #self.show_text('Drop to concatenate after current media', 0)
#            elif mod & Qt.ShiftModifier:     # shift (add audio track)
#                file = [url.toLocalFile() for url in event.mimeData().urls()][0]
#                if os.path.abspath(file) != gui.video:
#                    gui.statusbar.showMessage('Drop to add as audio track', 3000)
#                    #self.show_text('Drop to add as audio track', 0)
#                else:
#                    gui.statusbar.showMessage('Drop to add as audio track (disabled due to identical file)', 3000)
#                    #self.show_text('Drop to add as audio track (disabled due to identical file)', 0)
#            else:                                   # no modifiers (play file)
#                gui.statusbar.showMessage('Drop to play media, or hold ctrl/alt/shift for more options', 3000)
#                #self.show_text('Drop to play media, or hold ctrl/alt/shift for more options', 0)
#        super().dragMoveEvent(event)
#
#
#    def dropEvent(self, event: QtGui.QDropEvent):   # attempt to open dropped files
#        ''' Attempts to interact with the file that has been dropped as media. Ignores files beyond the first one.
#            Allows modifiers to alter the interaction used.
#            No modifiers -> Open media.
#            Ctrl         -> Adds media as an audio track.
#            Shift        -> Concatenates media to the end of the current media.
#            Alt          -> Concatenates media to the start of the current media. '''
#        #self.show_text('')
#        focus_window = settings.checkFocusDrop.isChecked()
#        file = [url.toLocalFile() for url in event.mimeData().urls()][0]
#        if gui.video:
#            mod = event.keyboardModifiers()
#            if mod & Qt.ControlModifier:     # ctrl (concat before current)
#                gui.concatenate(style='before current', files=(file,))
#            elif mod & Qt.AltModifier:       # alt (concat after current)
#                gui.concatenate(style='after current', files=(file,))
#            elif mod & Qt.ShiftModifier:       # shift (add audio track)
#                if os.path.abspath(file) != gui.video: gui.add_audio_track(path=file)
#                else: gui.statusbar.showMessage('Cannot add file to itself as an audio track', 10000)
#            else: gui.open(file, focus_window=focus_window)  # video playing but no modifiers -> play dropped file
#        else: gui.open(file, focus_window=focus_window)      # no video playing -> play dropped file
#        self.dragdrop_in_progress = False
#        super().dropEvent(event)                    # run QWidget's built-in behavior
