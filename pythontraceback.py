import re

import sublime
import sublime_plugin

TRACEBACK_WINDOW_NAME = '* traceback *'
LINE_REGEXP = re.compile(r'"(.*)", line (\d+)')


class TracebackPasteCommand(sublime_plugin.WindowCommand):
    """Paste traceback into new window

    Paste clipboard contents (assuming clipboard contains python traceback,
    copied from console) to a dedicated transient window.
    """
    def run(self, *args):
        v = find_traceback_view(self.window)
        if not v:
            # Create new traceback view
            self.window.new_file(sublime.TRANSIENT)
            v = self.window.active_view()
            v.set_name(TRACEBACK_WINDOW_NAME)
            v.set_scratch(True)
        else:
            # Clear existing traceback view before pasting new traceback
            v.set_read_only(False)
            v.run_command("select_all")
            v.run_command("right_delete")

        v.run_command('paste')
        v.set_read_only(True)
        # Python syntax file fits well with tracebacks
        v.set_syntax_file('Packages/Python/Python.tmLanguage')

        # Put cursor to the bottom of the screen
        self.view_tail(v)
        # Place markers on lines, that belongs to current project
        self.mark_lines(v)
        # Show the traceback buffer (if hidden)
        self.window.focus_view(v)

    def mark_lines(self, view):
        total_lines, _ = view.rowcol(view.size())
        ownregions = []

        last_tb_line = None

        for lnum in range(total_lines):
            reg = view.line(view.text_point(lnum, 0))
            line_contents = view.substr(reg)
            tbfname, tbline = parse_line(line_contents)
            if not tbfname:
                continue

            last_tb_line = lnum
            if self.is_own_file(tbfname):
                ownregions.append(reg)

        view.add_regions("traceback.own", ownregions,
                         "keyword", "dot",
                         sublime.PERSISTENT | sublime.HIDDEN)

        if last_tb_line is not None:
            # For convenience, cursor will be placed on the last traceback line
            view.run_command("goto_line", {"line": last_tb_line+1})

    def is_own_file(self, filename):
        for f in self.window.folders():
            if filename.startswith(f):
                return True
        return False

    def view_tail(self, view):
        """Display the end of the buffer in view port

        By default, sublime puts cursor on top of the screen, hiding all the
        pasted text. This will put cursor to the bottom instead.
        """
        lowidth, loheight = view.text_to_layout(view.size())
        vpwidth, vpheight = view.viewport_extent()
        lheight = view.line_height()
        view.set_viewport_position((0, loheight - vpheight + lheight))


class TracebackGotoLine(sublime_plugin.TextCommand):
    """Open file under cursor in traceback window and set curser on
    appropriate line.
    """
    def run(self, edit):
        for region in self.view.sel():
            line = self.view.line(region)
            line_contents = self.view.substr(line)

            jump_to(self.view.window(), line_contents)


class TracebackGoUp(sublime_plugin.WindowCommand):
    def run(self, *args):
        jump_to_next(self.window, -1)


class TracebackGoDown(sublime_plugin.WindowCommand):
    def run(self, *args):
        jump_to_next(self.window, 1)


class ActionContextHandler(sublime_plugin.EventListener):
    """Provide special `python_traceback` context in traceback window

    So that plugin could provide traceback specific bindings.
    """
    def on_query_context(self, view, key, op, operand, match_all):
        if not key.startswith('python_traceback'):
            return None

        return view.name() == TRACEBACK_WINDOW_NAME


def find_traceback_view(window):
    for view in window.views():
        if view.name() == TRACEBACK_WINDOW_NAME:
            return view
    return None


def jump_to_next(window, direction):
        tbview = find_traceback_view(window)
        if not tbview:
            sublime.status_message("No traceback available")
            return

        tbsel = tbview.sel()

        if not tbsel:
            # No selection - current position is not known
            return

        firstreg = tbsel[0]
        lineno = tbview.rowcol(firstreg.a)[0]
        newpos = firstreg.a

        # Check each line until end of traceback is reached, or proper link to
        # file is found.
        while True:
            lineno += direction
            if lineno < 0:
                # We went above first line
                break

            oldpos = newpos
            newpos = tbview.text_point(lineno, 0)
            if oldpos == newpos:
                # We reached end of file
                break

            cursorreg = sublime.Region(newpos, newpos)
            line_contents = tbview.substr(tbview.line(cursorreg))

            jumped = jump_to(window, line_contents)
            if jumped:
                # Update cursor position in traceback view
                tbview.run_command("goto_line", {"line": lineno+1})
                return

        # Infinite loop ended, that means that we have reached to end of the
        # traceback. Let user know.
        sublime.status_message("No more lines in traceback")


def jump_to(window, line):
    fname, lineno = parse_line(line)
    if fname is None:
        return False

    open_file(window, fname, lineno)
    return True


def parse_line(line):
    not_found = None, None
    if not line:
        return not_found

    m = LINE_REGEXP.search(line)
    if not m:
        return not_found

    filename, lnum = m.groups()
    return filename, int(lnum)


def open_file(window, filename, linenum):
    window = sublime.active_window()
    window.open_file("%s:%s" % (filename, linenum),
                     sublime.ENCODED_POSITION)
