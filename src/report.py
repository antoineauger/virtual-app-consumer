from utils.obs_utils import ObsUtils


class Report(object):
    def __init__(self, use_iqas, application_id, timestamps, battery_level, provenance):
        self.metrics = dict()
        self.metrics['use_iqas'] = use_iqas
        self.metrics['battery_level'] = battery_level
        self.metrics['timestamps'] = dict()
        self.metrics['application_id'] = application_id
        self.metrics['provenance'] = provenance

        for s in timestamps.split(";"):
            a = s.split(':')
            self.metrics['timestamps'][a[0]] = a[1]


class RDorInformationReport(Report):
    def __init__(self, use_iqas, observation, config, battery_level):
        super().__init__(use_iqas,
                         config['application_id'],
                         observation['timestamps'],
                         battery_level,
                         observation['producer'])


class KnowledgeReport(Report):
    def __init__(self, use_iqas, observation, config, battery_level):
        extracted_fields = ObsUtils.extract_fields_from_jsonld(observation)
        super().__init__(use_iqas,
                         config['application_id'],
                         extracted_fields['timestamps'],
                         battery_level,
                         extracted_fields['producer'])
