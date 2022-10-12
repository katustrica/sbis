from django.shortcuts import render

from django.shortcuts import render
from Hotel.models import EventBRS, ActiveIntervalsBRS, Booking
from Hotel.const import ROOM_ID_NAME_DICT, MESSHIGH_NAME_DICT
import pandas as pd
from plotly.offline import plot
import plotly.express as px
from datetime import datetime
from constance import config


def index(request):
    start_date = config.START_TIME
    finish_date = config.FINISH_TIME

    events_by_sensor_id = EventBRS.get_by_interval(start_date, finish_date)
    intervals_by_sensor_id = ActiveIntervalsBRS.get_sensor_id_intervals_by_events_dict(events_by_sensor_id)
    bookings_by_room_number = Booking.get_by_interval(start_date, finish_date)
    plotly_tasks = []
    for bookings in bookings_by_room_number.values():
        for booking in bookings:
            name = ROOM_ID_NAME_DICT.get(booking.room_id)
            if not name:
                continue
            plotly_tasks.append(
                {'Task': f'{name}', 'Start': str(booking.start), 'Finish': str(booking.finish),
                 'Resource': 'Travelline'}
            )
    for intervals in intervals_by_sensor_id.values():
        for interval in intervals:
            name = MESSHIGH_NAME_DICT.get(interval.sensor_id)
            if not name:
                continue
            plotly_tasks.append(
                {'Task': f'{name}', 'Start': str(interval.start), 'Finish': str(interval.finish), 'Resource': 'БРС'}
            )
    fig = px.timeline(pd.DataFrame(plotly_tasks), x_start="Start", x_end="Finish", y="Task", color='Resource')
    fig.update_yaxes(autorange="reversed")
    gantt_plot = plot(fig, output_type="div")
    return render(request, 'index.html', context={'plot_div': gantt_plot})