# JSON API for European VAT number validation

This Python package contains a web-server that provides a web developer friendly JSON API, making it simple for you to perform European VAT number validation.

The server acts as a robust layer between your app and VIES, and by automatically retrying failed requests multiple times, you will experience fewer failed VAT validation requests than with direct requests to the VIES SOAP service.

## Installation and quick-start instructions

Here follows command line instructions for installation and running the server software on Unix like systems.

Check if Python pip is installed:

    pip -h

If pip is not installed, follow the installation instructions given here: [http://www.pip-installer.org/en/latest/installing.html]()

Install the API server software using pip:

    pip install -U "https://github.com/nephics/euvat-json-api/archive/master.zip"

Start the server:

    /usr/local/bin/euvat

You can start validating EU VAT numbers with the JSON API right away.

If you have [cURL](http://curl.haxx.se/) installed, you can validate a VAT number with the following command:

    curl http://127.0.0.1:8040/SE502070882101

Stop the server with Ctrl+C, or by sending a SIGTERM signal.

Configure your new API server start automatically after reboot, e.g., using [these instructions](http://jacobsondergaard.com/blog/make-your-server-process-run-forever/).

You can change the port of the server, and other options, via the command line.
See available command line options:

    /usr/local/bin/euvat --help

When starting, the server checks for a configuration file at:

    /etc/euvat.conf

In this file, you can set the same options as for the command line.

The following more detailed instructions are also available from your server [http://127.0.0.1:8040/]().


## The JSON API

The API is simple: Send a HTTP request to `http://127.0.0.1:8040/<VAT number>`, and you will receive a JSON encoded reply containing the response from VIES.

See examples of requests and responses below.

## Choose between direct or async request

The API gives you the choice to either 1) wait for the server to reply with the VAT response, or 2) get an asynchronous callback to your server, when the response is available from VIES.

The first option is great for front-end code (running in the browser) or for simple server-side request handling, where you don't have the option or infrastructure for receiving a HTTP callback.

The second (async) option is better for a server-side VAT lookup during payment processing, or when you are running an async web server like Node.js or Tornado.

The async option has one major advantage, namely that the callback to your server will occur when the VAT response is ready from VIES. Hence, if VIES is down or not responding, the API server will wait for VIES to get back online, before retrying the request and making the callback to your server.

It happens regularly that VIES is down, though often for shorter periods. Hence, the async option provides a much higher certainty for getting the VAT response from VIES instead of an error message.

### Making a direct request

Send a HTTP GET request to `http://127.0.0.1:8040/<VAT number>`, and you will receive a JSON encoded reply containing the response from VIES.

You can (optionally) include the jsonp query parameter to receive a JSONP response, i.e., a response with content type `application/javascript` performing a custom callback with the result.

### Making an async request (advanced use)

Send a HTTP POST request to `http://127.0.0.1:8040/<VAT number>` and with callback URL in the body, and the specified URL will receive a HTTP POST request with the JSON encoded response from VIES.

## Example requests

### Example request for validating a VAT number

Send a HTTP GET request to the URL

    http://127.0.0.1:8040/SE502070882101

The following response is returned (formatted for readability):

      {
        "name": "APPLE DISTRIBUTION INTERNATIONAL",
        "countryCode": "SE",
        "vatNumber": "502070882101",
        "valid": true,
        "requestDate": "2015-11-26",
        "address": "HOLLYHILL INDUSTRIAL ESTATE, HOLLY- \\nHILL, CO. CORK. ATT MARIE NIESEN \\nIRLAND",
        "requestStats": {
          "retries": 0,
          "total": 0.48,
          "request": 0.48,
          "queued": 0.0
        }
      }

If the VAT number is invalid the response will contain valid = false, as seen here, trying to validate VAT number "GB0000000":

      {
        "valid": false,
        "requestDate": "2013-11-26",
        "countryCode": "GB",
        "vatNumber": "0000000",
        "requestStats": {
            "total": 0.1,
            "retries": 0,
            "queued": 0.0,
            "request": 0.1
        }
      }

The requestStats object provides some performance statistics for the request:

- queued: Seconds in queue before submitting request to VIES
- retries: Number of retries (>0 when VIES is down or busy)
- request: Duration (seconds) of request to VIES (incl. waiting between retries)
- total: Total duration (seconds) of request on server.

If the VIES service is down, a HTTP 50x error response is returned with a description of the error. For example:

      {"code": 503, "error": "Member State service unavailable."}

If the request is malformed, e.g. missing country code, a HTTP 400 error response is returned with a description of the error. For example:

      {"code": 400, "error": "Invalid country code."}

### Example JSONP request for validating a VAT number

Send a HTTP GET request to the URL

    http://127.0.0.1:8040/SE502070882101?jsonp=myfunc

Response (formatted for readability):

      myfunc({
        "name": "APPLE DISTRIBUTION INTERNATIONAL",
        "countryCode": "SE",
        "vatNumber": "502070882101",
        "valid": true,
        "requestDate": "2015-11-26",
        "address": "HOLLYHILL INDUSTRIAL ESTATE, HOLLY- \\nHILL, CO. CORK. ATT MARIE NIESEN \\nIRLAND",
        "requestStats": {
          "retries": 0,
          "total": 1.71,
          "request": 1.71,
          "queued": 0.0
        }
      })


## Questions and Answers

### What are the valid country codes?

The European VAT numbers that can be validated using this API starts with one of these two letter country codes:

        countries = {
          "AT": "Austria",
          "BE": "Belgium",
          "BG": "Bulgaria",
          "CY": "Cyprus",
          "CZ": "Czech Republic",
          "DE": "Germany",
          "DK": "Denmark",
          "EE": "Estonia",
          "EL": "Greece",
          "ES": "Spain",
          "FI": "Finland",
          "FR": "France",
          "GB": "United Kingdom",
          "HR": "Croatia",
          "HU": "Hungary",
          "IE": "Ireland",
          "IT": "Italy",
          "LT": "Lithuania",
          "LU": "Luxembourg",
          "LV": "Latvia",
          "MT": "Malta",
          "NL": "The Netherlands",
          "PL": "Poland",
          "PT": "Portugal",
          "RO": "Romania",
          "SE": "Sweden",
          "SI": "Slovenia",
          "SK": "Slovakia"
        }

### Are VAT validation requests cached?

VAT replies are cached when the server is started with the --cache=/path/to/cache/ command line argument.

When caching is enabled and a cached result exists that is not older than 24 hours, the cached result is returned, and the response will contain cachedResult=true.

You can get the cached result, even when it is older than 24 hours, by setting the query parameter stale_ok=true.  
Example:

    http://127.0.0.1:8040/SE502070882101?stale_ok=true

You can force the server to perform the request, even if a cached result exists, by setting the query parameter no_cache=true.  
Example:

    http://127.0.0.1:8040/SE502070882101?no_cache=true


## Copyright and License

euvat-json-api - JSON API for European VAT number validation
Copyright (c) 2010-2015 Nephics AB, Jacob Söndergaard.  
Licensed under the Apache License, Version 2.0

Source code available at <a href="https://github.com/nephics/euvat-json-api">https://github.com/nephics/euvat-json-api</a>.