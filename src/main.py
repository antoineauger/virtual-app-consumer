import json
import sys
import time

import logging

import logstash

from consumer import Consumer
from utils.http_utils import HttpUtils

MAX_RETRIES = 5


def usage():
    """ Helper function and check of the arguments supplied """
    print("#################################################################")
    print("#                                                               #")
    print("# iQAS: an integration platform for QoO Assessment as a Service #")
    print("# Module: Virtual App Consumer                                  #")
    print("# (C) 2017 Antoine Auger                                        #")
    print("#                                                               #")
    print("#################################################################\n")


if __name__ == "__main__":
    host = '10.161.3.181'
    test_logger = logging.getLogger('python-logstash-logger')
    test_logger.setLevel(logging.INFO)
    test_logger.addHandler(logstash.UDPLogstashHandler(host, 54321, version=1))

    # Loading the configuration
    with open('../etc/app.config') as config_file:
        config = json.load(config_file)

    if len(sys.argv) < 3 or len(sys.argv) > 4:
        usage()
        print('ERROR: Wrong number of parameters')
        exit()
    else:
        topics_to_subscribe = None

        if len(sys.argv) == 4:  # The Request is given as a single string
            config['application_id'] = str(sys.argv[2])
            config['use_iqas'] = True
            config['iqas_request'] = json.loads(str(sys.argv[3]))
        else: # Direct consumption without iQAS
            config['application_id'] = "direct_" + str(sys.argv[2])
            config['use_iqas'] = False
            config['iqas_request'] = "NA"
            config['request_id'] = "direct"
            topics_to_subscribe = str(sys.argv[2]).split(",")

        if config['use_iqas']:
            config['iqas_request']['application_id'] = config['application_id']
            base_url_for_requests = "http://" + config['iqas_api_endpoint'] + "/requests"
            status_code, response = HttpUtils.post_to_rest_endpoint(url=base_url_for_requests,
                                                                    dictionary=config['iqas_request'])
            config['request_id'] = response['request_id']

            if status_code == 200:
                ready = False
                retries = 0
                while not ready and retries < MAX_RETRIES:
                    status_code2, response2 = HttpUtils.get_from_rest_endpoint(url=base_url_for_requests + "/" + config['request_id'])
                    if response2['current_status'] == 'ENFORCED':
                        break
                    else:
                        time.sleep(1)
                        retries += 1

            time.sleep(5)

            # Once the Request has been accepted, we can start consuming observations
            topics_to_subscribe = list()
            topics_to_subscribe.append(config['application_id'] + '_' + config['request_id'])

        consumer_thread = Consumer(config=config,
                                   topics_to_subscribe=topics_to_subscribe,
                                   logstash=test_logger)
        consumer_thread.run()
