class Report(object):
    def __init__(self, timestamps, battery_level, application_id, provenance):
        self.metrics = dict()
        self.metrics['battery_level'] = battery_level
        self.metrics['timestamps'] = dict()
        self.metrics['application_id'] = application_id
        self.metrics['provenance'] = provenance
        for s in timestamps.split(";"):
            a = s.split(':')
            self.metrics['timestamps'][a[0]] = a[1]
