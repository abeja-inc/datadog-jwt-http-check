#!/usr/bin/env python
from checks import AgentCheck
import requests
import os
import time
import json
import jwt
import re
import tempfile
import datetime


class JwtHttpCheck(AgentCheck):
    def get_token(self, iss, aud, kid, secret_key, algorithm, ttl_in_seconds):
        now = time.time()
        td = now + ttl_in_seconds
        payload = {
            "iss": iss,
            "aud": aud,
            "iat": str(int(now)),
            "exp": str(int(td))
        }
        encoded = jwt.encode(payload, secret_key, algorithm, headers={'kid': kid})
        scheme = 'Bearer'
        authorization_token = '{} {}'.format(scheme, encoded.decode('utf-8'))
        return authorization_token

    def get_image(self, url):
        filename = os.path.basename(url)
        tempdir = tempfile.gettempdir()
        filepath = os.path.join(tempdir, filename)
        if not os.path.exists(filepath):
            r = requests.get(url)
            with open(filepath, 'wb') as f:
                f.write(r.content)
        with open(filepath, 'rb') as f:
            return f.read()

    def check(self, instance):
        url = instance['url'].format(datetime.datetime.utcnow())
        method = instance['method']
        headers = instance.get('headers', {})
        data = instance.get('data', {})
        metrics_prefix = instance.get('metrics_prefix', 'jwt')
        data_image_url = instance.get('data_image_url', None)
        iss = instance['jwt']['iss']
        aud = instance['jwt']['aud']
        ttl_in_seconds = int(instance['jwt'].get('ttl_in_seconds', (24 * 60 * 60)))
        kid = instance['jwt']['kid']
        algo = instance['jwt']['algorithm']
        secret_key = instance['jwt']['secret_key']
        tags = instance['tags']
        http_response_status_code = instance.get('http_response_status_code', '2\d\d')
        default_timeout = self.init_config.get('default_timeout', 5)
        timeout = float(instance.get('timeout', default_timeout))

        token = self.get_token(iss, aud, kid, secret_key, algo, ttl_in_seconds)
        headers = {'Authorization': token}

        if data_image_url is not None:
            _data = self.get_image(data_image_url)
        else:
            _data = json.dumps(data)
        s = time.time()
        try:
            r = requests.request(method, url, headers=headers, data=_data, timeout=timeout)
        except:
            success = 0
        else:
            if not re.match(http_response_status_code, str(r.status_code)):
                success = 0
            else:
                success = 1
        e = time.time()
        latency = int((e - s) * 1000)
        self.gauge('{}.http.request.success'.format(metrics_prefix), success, tags=tags)
        self.gauge('{}.http.request.latency'.format(metrics_prefix), latency, tags=tags)
