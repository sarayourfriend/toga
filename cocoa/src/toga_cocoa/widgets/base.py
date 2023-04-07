from toga.colors import TRANSPARENT
from toga_cocoa.colors import native_color
from toga_cocoa.constraints import Constraints


class Widget:
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.interface._impl = self
        self._container = None
        self._viewport = None
        self.constraints = None
        self.native = None
        self.create()
        self.interface.style.reapply()

    def create(self):
        raise NotImplementedError()

    def set_app(self, app):
        pass

    def set_window(self, window):
        pass

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, container):
        if self.container:
            if container:
                raise RuntimeError("Already have a container")
            else:
                # existing container should be removed
                self.constraints.container = None
                self._container = None
                self.native.removeFromSuperview()
        elif container:
            # setting container
            self._container = container
            self._container.native.addSubview(self.native)
            self.constraints.container = container

        for child in self.interface.children:
            child._impl.container = container

        self.rehint()

    @property
    def viewport(self):
        return self._viewport

    @viewport.setter
    def viewport(self, viewport):
        self._viewport = viewport

    def get_enabled(self):
        return self.native.isEnabled

    def set_enabled(self, value):
        self.native.enabled = value

    # APPLICATOR

    def set_bounds(self, x, y, width, height):
        # print("SET BOUNDS ON", self.interface, x, y, width, height)
        self.constraints.update(x, y, width, height)

    def set_alignment(self, alignment):
        pass

    def set_hidden(self, hidden):
        if self.native:
            self.native.setHidden(hidden)

    def set_font(self, font):
        pass

    def set_color(self, color):
        pass

    def set_background_color(self, color):
        if color is TRANSPARENT:
            self.native.drawsBackground = False
        else:
            self.native.backgroundColor = native_color(color)
            self.native.drawsBackground = True

    def focus(self):
        self.interface.window._impl.native.makeFirstResponder(self.native)

    def get_tab_index(self):
        self.interface.factory.not_implementated("Widget.get_tab_index()")

    def set_tab_index(self, tab_index):
        self.interface.factory.not_implementated("Widget.set_tab_index()")

    # INTERFACE

    def add_child(self, child):
        if self.viewport:
            # we are the the top level NSView
            child.container = self
        else:
            child.container = self.container

    def insert_child(self, index, child):
        self.add_child(child)

    def remove_child(self, child):
        child.container = None

    def add_constraints(self):
        self.native.translatesAutoresizingMaskIntoConstraints = False
        self.constraints = Constraints(self)

    def refresh(self):
        self.rehint()

    def rehint(self):
        pass
