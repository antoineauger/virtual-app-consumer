import json
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
    # Loading the configuration
    with open('../etc/app.config') as config_file:
        config = json.load(config_file)

    if len(sys.argv) < 3 or len(sys.argv) > 4:
        usage()
        print('ERROR: Wrong number of parameters')
        exit()
    else:
        config['application_id'] = str(sys.argv[1])
        if len(sys.argv) == 4:  # -f /path/to/file
            with open(str(sys.argv[3])) as request_template:
                config['iqas_request'] = json.load(request_template)
        else:  # The Request is given as a single string
            config['iqas_request'] = json.loads(str(sys.argv[2]))

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
        print('OK')

        # Once the Request has been accepted, we can start consuming observations
        topic_to_subscribe = config['application_id'] + '_' + config['request_id']
        consumer_thread = Consumer(config=config, topics_to_subscribe=[topic_to_subscribe])
        consumer_thread.start()
