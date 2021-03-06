"""
   Copyright 2020 InfAI (CC SES)

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from splitter.configuration import conf
from splitter import splitFile
import requests
import os


file_map = splitFile(conf.data_cache_path, conf.input_file, conf.column)

try:
    resp = requests.post(
        conf.job_callback_url,
        json={
            conf.worker_instance: [{"unique_id": key, "result_table": value} for key, value in file_map.items()]
        }
    )
    if not resp.ok:
        raise RuntimeError(resp.status_code)
except Exception as ex:
    for value in file_map.values():
        try:
            os.remove(os.path.join(conf.data_cache_path, value))
        except Exception:
            pass
    raise ex
