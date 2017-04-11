import json
import logging
import os
import sys
import time

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
    logging.basicConfig(level=logging.WARNING)

    # Loading the configuration
    with open('../etc/app.config') as config_file:
        config = json.load(config_file)

    # Disabling proxy for all future connections
    if config['disable_proxy_for_all_requests']:
        os.environ['NO_PROXY'] = '10.161.3.181'
        os.environ['no_proxy'] = '10.161.3.181'

    if len(sys.argv) != 1:
        usage()
        print('ERROR: Wrong number of parameters')
        exit()
    else:
        application_id = 'virtual-app'   #str(sys.argv[1])
        config['application_id'] = application_id

        payload = {'application_id': config['application_id'], 'location': 'ALL', 'topic': 'ALL', 'obs_level': 'INFORMATION'}

        base_url_for_requests = "http://" + config['iqas_api_endpoint'] + "/requests"
        status_code, response = HttpUtils.post_to_rest_endpoint(url=base_url_for_requests, dictionary=payload)
        request_id = response['request_id']

        if status_code == 200:
            ready = False
            retries = 0
            while not ready and retries < MAX_RETRIES:
                status_code2, response2 = HttpUtils.get_from_rest_endpoint(url=base_url_for_requests + "/" + request_id)
                if response2['current_status'] == 'ENFORCED':
                    break
                else:
                    time.sleep(1)
                    retries += 1

        print('OK')

        # Once the Request has been accepted, we can start consuming observations
        topic_to_subscribe = application_id + '_' + request_id
        consumer_thread = Consumer(config=config, topics_to_subscribe=[topic_to_subscribe])
        consumer_thread.start()
