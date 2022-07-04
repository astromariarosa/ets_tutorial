from traits.api import Property
from pyface.tasks.api import Editor

from .image_file_view import ImageFileView


class ImageFileEditor(Editor):
    name = Property

    tooltip = Property

    # -------------------------------------------------------------------------
    # 'Editor' interface methods
    # -------------------------------------------------------------------------

    def create(self, parent):
        """ Create and set the toolkit-specific control that represents the
        editor.
        """
        # Setting the kind and the parent allows for the ui to be embedded
        # within the parent UI
        view = ImageFileView(model=self.obj)
        ui = view.edit_traits(kind="subpanel", parent=parent)

        # Grab the Qt widget to return to the editor area
        self.control = ui.control

    # -------------------------------------------------------------------------
    # Traits property methods
    # -------------------------------------------------------------------------

    def _get_name(self):
        return self.obj.filepath[:25]

    def _get_tooltip(self):
        return self.obj.filepath
