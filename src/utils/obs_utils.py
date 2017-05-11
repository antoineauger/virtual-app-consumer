import json

from utils.time_utils import TimeUtils


class ObsUtils(object):
    @staticmethod
    def consume_obs(config, consumer_record, append_timestamp=False):
        if append_timestamp:
            if config['iqas_request']['obs_level'] == 'RAW_DATA' or config['iqas_request']['obs_level'] == 'INFORMATION':
                obs_temp = dict(consumer_record.value)
                timestamps_str = obs_temp['timestamps']
                timestamps_str += ';consumed:{}'.format(TimeUtils.current_milli_time())
                obs_temp['timestamps'] = timestamps_str
                return obs_temp
            elif config['iqas_request']['obs_level'] == 'KNOWLEDGE':

                print("CONSUMER RECORD")
                print(consumer_record)
                obs_temp = dict(consumer_record.value)
                print(obs_temp)
                for f in obs_temp['obs']:
                    if "@type" in f and f['@type'] == "http://purl.oclc.org/NET/ssnx/ssn#ObservationValue":
                        timestamps_str = f['obsTimestampsValue']
                        timestamps_str += ';consumed:{}'.format(TimeUtils.current_milli_time())
                        f['obsTimestampsValue'] = timestamps_str
                        return obs_temp
        else:
            return dict(consumer_record.value)

    """
        Should extract timestamps and producer fields
    """
    @staticmethod
    def extract_fields_from_jsonld(obs):
        fields_to_return = dict()
        print(obs)
        array_all_fields = obs['obs']

        for f in array_all_fields:
            if "@type" in f and f['@type'] == "http://purl.oclc.org/NET/ssnx/ssn#ObservationValue":
                fields_to_return['timestamps'] = f['obsTimestampsValue']
            elif "@type" in f and f['@type'] == "http://purl.oclc.org/NET/ssnx/ssn#Observation":
                fields_to_return['producer'] = f['observedBy'].split('#')[1]

        return fields_to_return
