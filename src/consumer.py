import json
from kafka import KafkaConsumer

from report import RDorInformationReport, KnowledgeReport
from utils.obs_utils import ObsUtils
from utils.time_utils import TimeUtils


class Consumer(object):
    def __init__(self, config, topics_to_subscribe, logstash):
        self.config = config
        self.kafka_consumer = None
        self.logstash = logstash
        self.topics_to_subscribe = topics_to_subscribe
        self.consumed_battery = 0.0

    def __del__(self):
        if self.kafka_consumer is not None:
            self.kafka_consumer.close()

    def run(self):
        self.kafka_consumer = KafkaConsumer(bootstrap_servers='10.161.3.181:9092',
                                            group_id=None,
                                            auto_offset_reset='latest',
                                            enable_auto_commit=False,
                                            receive_buffer_bytes=65536,
                                            check_crcs=False,
                                            value_deserializer=lambda m: json.loads(m.decode('ascii')))
        self.kafka_consumer.subscribe(self.topics_to_subscribe)

        for record in self.kafka_consumer:
            print(str(record))
            timestamp_consumption = TimeUtils.current_milli_time()
            report = None
            if self.config['use_iqas']:
                observation = ObsUtils.consume_obs_from_iqas(config=self.config,
                                                             consumer_record=record,
                                                             timestamp_consumption=timestamp_consumption)
                self.consumed_battery += 0.01

                if self.config['iqas_request']['obs_level'] == 'RAW_DATA' \
                        or self.config['iqas_request']['obs_level'] == 'INFORMATION':
                    report = RDorInformationReport(use_iqas=True,
                                                   observation=observation,
                                                   config=self.config,
                                                   battery_level=self.consumed_battery)
                elif self.config['iqas_request']['obs_level'] == 'KNOWLEDGE':
                    report = KnowledgeReport(use_iqas=True,
                                             observation=observation,
                                             config=self.config,
                                             battery_level=self.consumed_battery)
            else:
                observation = ObsUtils.consume_obs_direct(consumer_record=record,
                                                          timestamp_consumption=timestamp_consumption)
                self.consumed_battery += 0.01

                report = RDorInformationReport(use_iqas=False,
                                               observation=observation,
                                               config=self.config,
                                               battery_level=self.consumed_battery)

            self.logstash.info(msg='TEST', extra=report.metrics)

