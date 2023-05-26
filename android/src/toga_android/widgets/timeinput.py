from datetime import datetime, time

from ..libs.android import R__drawable
from ..libs.android.widget import (
    TimePickerDialog,
    TimePickerDialog__OnTimeSetListener as OnTimeSetListener,
)
from .internal.pickers import PickerBase


class TimePickerListener(OnTimeSetListener):
    def __init__(self, picker_impl):
        super().__init__()
        self.picker_impl = picker_impl

    def onTimeSet(self, _, *args):
        new_value = time(*args)

        self.picker_impl._dialog = None
        self.picker_impl.interface.value = new_value
        if self.picker_impl.interface.on_change:
            self.picker_impl.interface.on_change(self.picker_impl)


class TimeInput(PickerBase):
    @classmethod
    def _get_icon(cls):
        return R__drawable.ic_menu_recent_history

    @classmethod
    def _get_hint(cls):
        return "HH:MM"

    def create(self):
        self._value = datetime.now().time()
        self._min_time = None
        self._max_time = None

        return super().create()

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value
        self.native.setText(value.isoformat(timespec="minutes"))
        if self._dialog is not None:
            self._dialog.updateTime(value.hour, value.minute)

    def get_min_time(self):
        return self._min_time

    def set_min_time(self, value):
        self.interface.factory.not_implemented("TimeInput.set_min_time()")

    def get_max_time(self):
        return self._max_time

    def set_max_time(self, value):
        self.interface.factory.not_implemented("TimeInput.set_max_time()")

    def _create_dialog(self):
        self._dialog = TimePickerDialog(
            self._native_activity,
            TimePickerListener(self),
            self._value.hour,
            self._value.minute,
            True,
        )
        self._dialog.show()
