'Garden Lighting Controller'

import astral
import click
import datetime
import logging
import paho.mqtt.client
import schedule
import threading
import time

__version__ = '1.0.0'

SEQUENCE = [
    'c101', 'c107', 'c108', 'c105', 'c102',
    'c103', 'c106', 'c111', 'c109', 'c104'
]

lock = threading.RLock()


def plc_latch(mqtt):
    mqtt.publish('plc/c200/set', 'true', qos=1)


def plc_out_set(mqtt, output, value):
    mqtt.publish('plc/%s/set' % output, 'true' if value else 'false', qos=1)


def worker_lights_on(mqtt):
    lock.acquire()
    for sequence in SEQUENCE:
        logging.debug('Switching on `%s`' % sequence)
        plc_out_set(mqtt, sequence, True)
        time.sleep(0.5)  # TODO Remove after controller fix
        plc_latch(mqtt)
        time.sleep(0.5)
    lock.release()


def worker_lights_off(mqtt):
    lock.acquire()
    for sequence in SEQUENCE[::-1]:
        logging.debug('Switching off `%s`' % sequence)
        plc_out_set(mqtt, sequence, False)
        time.sleep(0.5)  # TODO Remove after controller fix
        plc_latch(mqtt)
        time.sleep(0.5)
    lock.release()


def job_lights_on(mqtt):
    logging.info('Job: Lights on')
    threading.Thread(target=worker_lights_on, args=(mqtt,)).start()
    return schedule.CancelJob


def job_lights_off(mqtt):
    logging.info('Job: Lights off')
    threading.Thread(target=worker_lights_off, args=(mqtt,)).start()
    return schedule.CancelJob


def job_plan_day(mqtt):
    logging.info('Job started: job_plan_day')
    a = astral.Astral()
    a.solar_depression = 'civil'
    city = a['Prague']
    sun = city.sun(date=datetime.date.today(), local=True)
    dawn = '%02d:%02d' % (sun['dawn'].hour, sun['dawn'].minute)
    sunset = '%02d:%02d' % (sun['sunset'].hour, sun['sunset'].minute)
    logging.info('Dawn is at %s' % dawn)
    logging.info('Sunset is at %s' % sunset)
    schedule.every().day.at(dawn).do(job_lights_off, mqtt)
    schedule.every().day.at(sunset).do(job_lights_on, mqtt)
    logging.info('Job started: job_plan_day')


def on_connect(client, userdata, flags, rc):
    logging.info('MQTT connected (code: %d)' % rc)
    client.subscribe("sunrice/on")
    client.subscribe("sunrice/off")


def on_message(client, userdata, msg):
    logging.debug('Received topic: %s' % msg.topic)
    if msg.topic == 'sunrice/on':
        logging.info("Received ON request via MQTT")
        client.publish('%s/ok' % msg.topic, qos=1)
        threading.Thread(target=worker_lights_on, args=(client,),
                         daemon=True).start()
    elif msg.topic == 'sunrice/off':
        logging.info("Received OFF request via MQTT")
        client.publish('%s/ok' % msg.topic, qos=1)
        threading.Thread(target=worker_lights_off, args=(client,),
                         daemon=True).start()


@click.command()
@click.option('--host', '-h', default='127.0.0.1', help='MQTT broker host.')
@click.option('--port', '-p', default='1883', help='MQTT broker port.')
@click.version_option(version=__version__)
def main(host, port):
    try:
        logging.basicConfig(format='%(asctime)s <%(levelname)s> %(message)s',
                            level=logging.DEBUG, datefmt="%Y-%m-%dT%H:%M:%S")
        logging.getLogger('schedule').propagate = False
        logging.info('Program started')
        mqtt = paho.mqtt.client.Client()
        mqtt.on_connect = on_connect
        mqtt.on_message = on_message
        mqtt.connect(host, int(port))
        schedule.every().day.at("00:00").do(job_plan_day, mqtt)
        while True:
            schedule.run_pending()
            mqtt.loop()
    except KeyboardInterrupt:
        pass
