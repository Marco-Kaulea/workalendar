from datetime import date
from ..core import WesternCalendar
from ..registry_tools import iso_register


@iso_register('HU')
class Hungary(WesternCalendar):
    'Hungary'

    # Christian holidays
    include_easter_sunday = True
    include_easter_monday = True
    include_whit_sunday = True
    whit_sunday_label = "Pentecost Sunday"
    include_whit_monday = True
    whit_monday_label = "Pentecost Monday"
    include_boxing_day = True
    boxing_day_label = "Second Day of Christmas"
    include_all_saints = True

    # Civil holidays
    include_labour_day = True
    FIXED_HOLIDAYS = WesternCalendar.FIXED_HOLIDAYS + (
        (3, 15, "National Day"),
        (8, 20, "St Stephen's Day"),
        (10, 23, "National Day"),
    )
    compensated_rest_days = (
        ((2022, 3, 14), (2022, 3, 26)),
        ((2022, 10, 31), (2022, 10, 15)),
    )
    """Rest days with the additional workday that compensates for it."""

    def is_working_day(self, day,
                       extra_working_days=None, extra_holidays=None):
        extra_working_days = (
            list(extra_working_days) if extra_working_days is not None else []
        )
        extra_holidays = (
            list(extra_holidays) if extra_holidays is not None else []
        )
        for holiday, working_day in self.compensated_rest_days:
            extra_working_days.append(date(*working_day))
            extra_holidays.append(date(*holiday))
        return super().is_working_day(day, extra_working_days, extra_holidays)

    def get_variable_days(self, year):
        # As of 2017, Good Friday became a holiday
        self.include_good_friday = (year >= 2017)
        days = super().get_variable_days(year)
        for holiday, _working_day in self.compensated_rest_days:
            if holiday[0] == year:
                days.append((date(*holiday), 'Rest Day'))
        return days
