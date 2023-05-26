from datetime import date, datetime

from ..libs.android import R__drawable
from ..libs.android.widget import (
    DatePickerDialog,
    DatePickerDialog__OnDateSetListener as OnDateSetListener,
)
from .internal.pickers import PickerBase


class DatePickerListener(OnDateSetListener):
    def __init__(self, picker_impl):
        super().__init__()
        self.picker_impl = picker_impl

    def onDateSet(self, _, *args):
        day, month, year = args
        new_value = date(day, month + 1, year)

        self.picker_impl._dialog = None
        self.picker_impl.interface.value = new_value
        if self.picker_impl.interface.on_change:
            self.picker_impl.interface.on_change(self.picker_impl)


class DateInput(PickerBase):
    @classmethod
    def _get_icon(cls):
        return R__drawable.ic_menu_my_calendar

    @classmethod
    def _get_hint(cls):
        return "YYYY-MM-DD"

    def create(self):
        self._value = date.today()
        self._min_date = None
        self._max_date = None

        return super().create()

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value
        if value is not None:
            self.native.setText(value.isoformat())
            if self._dialog is not None:
                self._dialog.updateDate(value.year, value.month - 1, value.day)

    def get_min_date(self):
        return self._min_date

    def set_min_date(self, value):
        self._min_date = value
        if value is not None and self._dialog is not None:
            self._dialog.getDatePicker().setMinDate(self._date_to_milli(value))

    def get_max_date(self):
        return self._max_date

    def set_max_date(self, value):
        self._max_date = value
        if value is not None and self._dialog is not None:
            self._dialog.getDatePicker().setMaxDate(self._date_to_milli(value))

    @classmethod
    def _date_to_milli(cls, value):
        datetime_value = datetime.combine(value, datetime.min.time())
        timestamp = datetime_value.timestamp()
        return int(timestamp * 1000)

    def _create_dialog(self):
        self._dialog = DatePickerDialog(
            self._native_activity,
            DatePickerListener(self),
            self._value.year,
            self._value.month - 1,
            self._value.day,
        )
        self.set_min_date(self._min_date)
        self.set_max_date(self._max_date)
        self._dialog.show()
