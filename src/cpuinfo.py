# Mock implementation of py-cpuinfo

import json

def get_cpu_info():
    return json.loads(get_cpu_info_json())

def get_cpu_info_json():
    info_str = "{'python_version': '3.11.1.final.0 (64 bit)', 'cpuinfo_version': [9, 0, 0], 'cpuinfo_version_string': '9.0.0', 'arch': 'ARM_8', 'bits': 64, 'count': 10, 'arch_string_raw': 'arm64', 'brand_raw': 'Apple M2 Pro'}"
    # Convert the single quotes to double quotes for valid JSON format
    return info_str.replace("'", '"')