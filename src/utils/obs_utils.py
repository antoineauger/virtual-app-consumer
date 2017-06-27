class ObsUtils(object):
    @staticmethod
    def consume_obs_from_iqas(config, consumer_record, timestamp_consumption):
        if timestamp_consumption is not None:
            if config['iqas_request']['obs_level'] == 'RAW_DATA' \
                    or config['iqas_request']['obs_level'] == 'INFORMATION':
                obs_temp = dict(consumer_record.value)
                timestamps_str = obs_temp['timestamps']
                timestamps_str += ';consumed:{}'.format(timestamp_consumption)
                obs_temp['timestamps'] = timestamps_str
                return obs_temp
            elif config['iqas_request']['obs_level'] == 'KNOWLEDGE':
                obs_temp = dict(consumer_record.value)
                for f in obs_temp['obs']:
                    if "@type" in f and f['@type'] == "http://purl.oclc.org/NET/ssnx/ssn#ObservationValue":
                        timestamps_str = f['obsTimestampsValue']
                        timestamps_str += ';consumed:{}'.format(timestamp_consumption)
                        f['obsTimestampsValue'] = timestamps_str
                        return obs_temp
        else:
            return dict(consumer_record.value)

    @staticmethod
    def consume_obs_direct(consumer_record, timestamp_consumption):
        if timestamp_consumption is not None:
            obs_temp = dict(consumer_record.value)
            timestamps_str = obs_temp['timestamps']
            timestamps_str += ';consumed:{}'.format(timestamp_consumption)
            obs_temp['timestamps'] = timestamps_str
            return obs_temp
        else:
            return dict(consumer_record.value)

    """
        Should extract timestamps and producer fields
    """
    @staticmethod
    def extract_fields_from_jsonld(obs):
        fields_to_return = dict()
        fields_to_return['qoo'] = dict()

        array_all_fields = obs['obs']

        for f in array_all_fields:
            if "@type" in f and f['@type'] == "http://purl.oclc.org/NET/ssnx/ssn#ObservationValue":
                fields_to_return['obsStrValue'] = f['obsStrValue']
                fields_to_return['quantityKind'] = f['hasQuantityKind']
                fields_to_return['unit'] = f['hasUnit']
                fields_to_return['timestamps'] = f['obsTimestampsValue']
            elif "@type" in f and f['@type'] == "http://purl.oclc.org/NET/ssnx/ssn#Observation":
                fields_to_return['producer'] = f['observedBy'].split('#')[1]
            elif "@type" in f and f['@type'] == "http://isae.fr/iqas/qoo-ontology#QoOValue":
                fields_to_return['qoo'][f['@id'].split('#')[1].replace('qooValue_', '')] = f['qooStrValue']

        return fields_to_return
