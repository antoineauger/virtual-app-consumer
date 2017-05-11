import json
import logging
import threading

import logstash
from kafka import KafkaConsumer

from report import RDorInformationReport, KnowledgeReport
from utils.obs_utils import ObsUtils


class Consumer(threading.Thread):
    def __init__(self, config, topics_to_subscribe):
        threading.Thread.__init__(self)
        self.config = config
        self._stop_event = threading.Event()  # to stop the main thread
        self.kafka_consumer = None
        self.topics_to_subscribe = topics_to_subscribe
        self.consumed_battery = 0.0
        host = '10.161.3.181'

        self.test_logger = logging.getLogger('python-logstash-logger')
        self.test_logger.setLevel(logging.INFO)
        self.test_logger.addHandler(logstash.TCPLogstashHandler(host, 54321, version=1))

    def __del__(self):
        self._stop_event.set()
        if self.kafka_consumer is not None:
            self.kafka_consumer.close()

    def run(self):
        self.kafka_consumer = KafkaConsumer(bootstrap_servers='10.161.3.181:9092',
                                            client_id=self.config['application_id'] + "_" + self.config['request_id'],
                                            group_id=self.config['application_id'],
                                            auto_offset_reset='earliest',
                                            value_deserializer=lambda m: json.loads(m.decode('ascii')))
        self.kafka_consumer.subscribe(self.topics_to_subscribe)

        for record in self.kafka_consumer:
            observation = ObsUtils.consume_obs(config=self.config, consumer_record=record, append_timestamp=True)
            print(observation)
            self.consumed_battery += 0.01

            if self.config['iqas_request']['obs_level'] == 'RAW_DATA' or self.config['iqas_request']['obs_level'] == 'INFORMATION':
                rep = RDorInformationReport(observation=observation,
                                            config=self.config,
                                            battery_level=self.consumed_battery)
                self.test_logger.info(msg='TEST', extra=rep.metrics)
            elif self.config['iqas_request']['obs_level'] == 'KNOWLEDGE':
                rep = KnowledgeReport(observation=observation,
                                      config=self.config,
                                      battery_level=self.consumed_battery)
                self.test_logger.info(msg='TEST', extra=rep.metrics)
