from utils.obs_utils import ObsUtils


class Report(object):
    def __init__(self, use_iqas, request_id, application_id, timestamps, battery_level, provenance, obsStrValue, quantityKind, unit, qoo):
        self.metrics = dict()
        self.metrics['use_iqas'] = use_iqas
        self.metrics['request_id'] = request_id
        self.metrics['battery_level'] = battery_level
        self.metrics['qoo'] = qoo
        self.metrics['timestamps'] = dict()
        self.metrics['application_id'] = application_id
        self.metrics['obsStrValue'] = obsStrValue
        if quantityKind is not None:
            self.metrics['quantityKind'] = quantityKind
        if unit is not None:
            self.metrics['unit'] = unit
        self.metrics['provenance'] = provenance

        for s in timestamps.split(";"):
            a = s.split(':')
            self.metrics['timestamps'][a[0]] = a[1]


class RDorInformationReport(Report):
    def __init__(self, use_iqas, observation, config, battery_level):
        qoo = dict()
        if 'qoOAttributeValues' in observation:
            for k, v in observation['qoOAttributeValues'].items():
                qoo[k] = float(v)

        super().__init__(use_iqas=use_iqas,
                         request_id=config['request_id'],
                         application_id=config['application_id'],
                         timestamps=observation['timestamps'],
                         battery_level=battery_level,
                         provenance=observation['producer'],
                         obsStrValue=observation['value'],
                         quantityKind=None,
                         unit=None,
                         qoo=qoo)


class KnowledgeReport(Report):
    def __init__(self, use_iqas, observation, config, battery_level):
        extracted_fields = ObsUtils.extract_fields_from_jsonld(observation)
        super().__init__(use_iqas=use_iqas,
                         request_id=config['request_id'],
                         application_id=config['application_id'],
                         timestamps=extracted_fields['timestamps'],
                         battery_level=battery_level,
                         provenance=extracted_fields['producer'],
                         obsStrValue=extracted_fields['obsStrValue'],
                         quantityKind=extracted_fields['quantityKind'],
                         unit=extracted_fields['unit'],
                         qoo=extracted_fields['qoo'])
