from utils.time_utils import TimeUtils


class ObsUtils(object):
    @staticmethod
    def consume_obs(consumer_record, append_timestamp=False):
        if append_timestamp:
            obs_temp = dict(consumer_record.value)
            timestamps_str = obs_temp['timestamps']
            timestamps_str += ';consumed:{}'.format(TimeUtils.current_milli_time())
            obs_temp['timestamps'] = timestamps_str
            return obs_temp
        else:
            return dict(consumer_record.value)
