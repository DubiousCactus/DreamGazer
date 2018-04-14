#! flask/bin/python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hbartle <hbartle@geeknotebook>
#
# Distributed under terms of the MIT license.
import requests

data = {'mytext':  'We did it!'}
#r = requests.post("http://localhost:5000/api/add_message/1234", json={'json_payload': data})
r = requests.post("http://httpbin.org/post", json={'json_payload': data})

if r.ok:
    print(r.json())
