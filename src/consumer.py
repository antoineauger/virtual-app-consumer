import json
import threading

from kafka import KafkaConsumer

from utils.obs_utils import ObsUtils


class Consumer(threading.Thread):
    def __init__(self, topics_to_subscribe):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()  # to stop the main thread
        self.kafka_consumer = None
        self.topics_to_subscribe = topics_to_subscribe

    def __del__(self):
        self._stop_event.set()
        if self.kafka_consumer is not None:
            self.kafka_consumer.close()

    def run(self):
        self.kafka_consumer = KafkaConsumer(bootstrap_servers='10.161.3.181:9092',
                                            client_id='dummy-consumer',
                                            group_id='dummy-consumer',
                                            auto_offset_reset='earliest',
                                            value_deserializer=lambda m: json.loads(m.decode('ascii')))
        self.kafka_consumer.subscribe(self.topics_to_subscribe)

        for record in self.kafka_consumer:
            print(ObsUtils.consume_obs(consumer_record=record,
                                       append_timestamp=True))

