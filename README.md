PythonTraceback
===============

PythonTraceback is a plug-in for Sublime Text, that allows easy navigation in
your python tracebacks.  Copy a traceback from your terminal to clipboard,
switch to Sublime Text and press `Ctrl+t`, `Ctrl+v`. New scratch buffer will be
opened with the traceback. Place cursor on a line you want to navigate to and
press `Alt+d`: file will be opened at the line, specified in traceback.

While traceback window open (but not necessarily active), you can navigate up
and down in traceback by pressing `Alt-k` and `Alt-d` respectively.

Pressing `Ctrl+t`, `Ctrl+v` again will replace traceback buffer with new
traceback from the clipboard.

Defined commands
----------------

PythonTraceback defines the following commands:

Command                 | Title                      | Default Key Binding
:-----------------------|:---------------------------|:----------------------------------------------------
`traceback_paste`       | Traceback: Paste Traceback | `Ctrl+t`, `Ctrl+v` on PC or `⌘-t`, `⌘+v` on OSX
`traceback_goto_line`   | Traceback: Go To Line      | `Alt+d`
`traceback_go_up`       | Traceback: Go Up           | `Alt+k`
`traceback_go_down`     | Traceback: Go Down         | `Alt+j`
