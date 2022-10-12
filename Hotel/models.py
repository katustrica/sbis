import asyncio
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import IntEnum
from Hotel.const import AlarmType

from Hotel.request_helpers import request
import fdb
from django.contrib.auth.models import User
from django.db import models


class Booking(models.Model):
    number = models.CharField(max_length=50)
    room_id = models.CharField(max_length=10)
    start = models.DateTimeField()
    finish = models.DateTimeField()

    def __str__(self):
        return str(self.number)

    @classmethod
    def get_room_info_by_numbers(cls, numbers: list[str]):
        loop = asyncio.get_event_loop()
        urls = (f'https://partner.tlintegration.com/api/webpms/v1/bookings/{number}' for number in numbers)
        results = loop.run_until_complete(asyncio.gather(*[request('GET', url) for url in urls]))
        booking_infos = loop.run_until_complete(asyncio.gather(*[res.json() for res in results]))
        result = defaultdict(list)
        for booking in booking_infos:
            number = booking['number']
            room_stays = booking['roomStays'][0]
            room_id = room_stays['roomId']
            start = room_stays['checkInDateTime'] or room_stays['actualCheckInDateTime']
            finish = room_stays['checkOutDateTime'] or room_stays['actualCheckOutDateTime']
            result[room_id].append(Booking(number=number, room_id=room_id, start=start, finish=finish))
        return result

    @classmethod
    def get_by_interval(cls, start_date: datetime, finish_date: datetime):
        url = (
            r'https://partner.tlintegration.com/api/webpms/v1/bookings?affectsPeriodFrom='
            f'{start_date:%Y-%m-%dT%H:%M}&affectsPeriodTo={finish_date:%Y-%m-%dT%H:%M}'
        )
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        res = loop.run_until_complete(request('GET', url))
        json_res = loop.run_until_complete(res.json())

        return cls.get_room_info_by_numbers(json_res.get('bookingNumbers', []))

class EventBRS(models.Model):
    """ События из БРС """
    sensor_id: models.IntegerField()
    datetime = models.DateTimeField()
    type = models.IntegerField(choices=AlarmType.choices)

    @classmethod
    def get_by_interval(cls, start_date: datetime, finish_date: datetime):
        # Соединение
        con = fdb.connect(dsn=r'83.69.116.18:c:/STRUNA-5_DB/STRUNA24.FDB',
                          user='TUKAYA88',
                          role='HOTEL',
                          password='864273')
        # Объект курсора
        cur = con.cursor()

        # Выполняем запрос
        cur.execute(f"""
            SELECT 
                d.MESSHIGH,
                d.DTTM, 
                d.MESSLOW
            FROM 
                DATA d
            WHERE 
                GRP = 1 
                and MDM = 1
                and DTTM >= TIMESTAMP'{start_date:%Y-%m-%d %H:%M:%S}'
                and DTTM <= TIMESTAMP'{finish_date:%Y-%m-%d %H:%M:%S}'
                and (d.MESSLOW = 21 or d.MESSLOW = 32)
            ORDER BY DTTM asc
        """)

        result = defaultdict(list)
        for sensor_id, event_datetime, event_type in cur.fetchall():
            result[sensor_id].append(EventBRS(sensor_id, event_datetime, event_type))
        return result


class ActiveIntervalsBRS(models.Model):
    sensor_id = models.IntegerField()
    start = models.DateTimeField()
    finish = models.DateTimeField()

    @classmethod
    def get_sensor_id_intervals_by_events_dict(cls, sensor_id_events: dict[int, list[EventBRS]]) -> list['ActiveIntervalsBRS']:
        result = defaultdict(list)
        for sensor_id, events in sensor_id_events.items():
            if events[0].type != AlarmType.motion:
                events = events[1:]
            if events[-1].type != AlarmType.calm:
                events = events[:-1]

            start_time, finish_time = None, None
            for start_event, finish_event in zip(events[::2], events[1::2]):
                start_time = start_event.datetime if not start_time else start_time
                finish_time = finish_event.datetime if not finish_time else finish_time

                if start_event.datetime - finish_time < timedelta(minutes=5):
                    finish_time = finish_event.datetime
                else:
                    result[sensor_id].append(cls(sensor_id=sensor_id, start=start_time, finish=finish_time))
                    result[sensor_id].append(cls(sensor_id=sensor_id, start=start_event.datetime, finish=finish_event.datetime))
                    start_time = start_event.datetime
                    finish_time = finish_event.datetime
        return result