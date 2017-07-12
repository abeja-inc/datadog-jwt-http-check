Datadog custom agent check for http authorized with JWT
===
Http checks of http endpoints authorized with JWT.

This plugin collects:
- `${metrics_prefix}.http.request.success` ( `1` for request success and `0` for request failure)
- `${metrics_prefix}.http.request.latency`

# Installation

On the agent host.
- Install dependency by executing `/opt/datadog-agent/embedded/bin/pip install -r requirements.txt`
- Copy `checks.d/jwt_http_check.py` to `checks.d`.
- Copy `conf.d/jwt_http_check.yaml` to `conf.d` and write config.

*You can check the path of `checks.d` and `conf.d` by typing `sudo dd-agent info`.*

Then,
```
$ sudo service datadog-agent reload
```


# Configuration

```
init_config:
  default_timeout: 5

instances:
  - url: https://example.com/cars
    method: POST
    headers:
      Content-Type: image/jpeg
    data_image_url: https://example.com/test.jpg
    tags:
      - app:example-api
      - env:dev
      - endpoint:cars
    jwt:
      iss: xxx
      aud: yyy
      kid: kkk
      algorithm: RS256
      secret_key: |
        -----BEGIN RSA PRIVATE KEY-----
        .........
        -----END RSA PRIVATE KEY-----

  - url: https://example.com/drivers
    method: GET
    tags:
      - app:example-api
      - env:dev
      - endpoint:drivers
    jwt:
      iss: xxx
      aud: yyy
      kid: kkk
      algorithm: RS256
      secret_key: |
        -----BEGIN RSA PRIVATE KEY-----
        .........
        -----END RSA PRIVATE KEY-----
```

|Setting |Description|
|---|---|
|url | the url to test|
|method | The HTTP method. This setting defaults to GET, though many other HTTP methods are supported, including POST and PUT.  |
|timeout | The time in seconds to allow for a response.|
|headers | http headers|
| http_response_status_code|A string or Python regular expression for an HTTP status code. This check will report DOWN for any status code that does not match. This defaults to 1xx, 2xx and 3xx HTTP status codes. For example: 401 or 4\d\d.|
| data_image_url | image data will be sent in the body of the request. data is ignored if data_image_url is specified|
| data | Data should be included as key-value pairs and will be sent in the body of the request as json|
| metrics_prefix | prefix of metrics |
| jwt.iss | jwt param to get token |
| jwt.aud  |  jwt param to get token |
| jwt.kid  |  jwt param to get token |
| jwt.algorithm  |  jwt param to get token |
| jwt.ttl_in_second  |  jwt param to get token, default value is 86400 |
| jwt.secret_key  |  jwt param to get token |
