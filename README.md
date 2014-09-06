MusicEntrepreneurSplitter
=========================
Project goals
---
This project is about creating an environment for playing and editing music. It consists modules for:

* Playing tunes.
* Cutting tunes.
* Adding or removing tunes to a list for manipulation.
* Concatenating tunes from the list.
* Cutting tunes from the list.
* Lulling start or end (~ 4 secs) of the tune, that's about to be cut.
* Tool for drawing graphics of the played tune (in GUI).

All these functions are packed in sufficient GUI.

The music player implements "mixer" module from pygame, and is named "pymplayer". For cutting, concatenating, and lulling, is used pydub. For drawing are used numerous libraries, including matplotlib, numpy, scipy, and wand.

For user interface's been used PyQt4 - QtGui and QtCore. The initial view consists of (empty) list of tunes, timer, sliders for volume control and track position control, textboxes for input of place to start and end cutting, buttons for play/pause, stop, importing tunes to list, turning on/off lulling effect in the beginning or the end, concatenating, and cutting. After playing tune from list, a graphic is being generated and showed inside the window.

Project Dependencies
--------------------
* [Python 3](https://www.python.org/) *(or later)*
* [Pygame](http://www.pygame.org/news.html)
* [Pydub] (https://github.com/jiaaro/pydub)
* [NumPy] (http://www.numpy.org/)
* [SciPy] (http://www.scipy.org/)
* [Matplotlib] (http://matplotlib.org/)
* [Wand] (http://docs.wand-py.org/en/0.3.8/)
* [PyQt4] (http://www.riverbankcomputing.co.uk/software/pyqt/intro)

License
-------
The project falls under [GNU General Public License *(version 3)*](http://choosealicense.com/licenses/gpl-3.0/)

[License to use Python](https://docs.python.org/3/license.html#terms-and-conditions-for-accessing-or-otherwise-using-python)
