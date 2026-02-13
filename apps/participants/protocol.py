#this file contains info about baseline, month 3 and 1 year. The structure is a list with a dict which contains the info about each of these

VISIT_SCHEDULE = [
    {
        #the code is the name of the visit
        "visit_code": "baseline",
        #the target day is 0 for baseline and we dont allow windows for the baseline
        "target_day": 0,
        "window_before": 0,
        "window_after": 0
    },
    {
        "visit_code": "month_3",
        "target_day": 90,
        "window_before": 14,
        "window_after": 21
    },
    {
        "visit_code": "year_1",
        "target_day": 365,
        "window_before": 30,
        "window_after": 30
    }
]