from collections import OrderedDict

# local imports

def get_week(value, translate=False):
    data = []
    for i in range(7):
        mask_ = 1 << i
        if mask_ & value:
            data.append(mask_)
    if not translate:
        return data

    from .widgets import WeekMaskWidget
    week_mappings = OrderedDict(WeekMaskWidget.CHOICE)
    return [week_mappings[x] for x in data]
