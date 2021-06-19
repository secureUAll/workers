import json
import logging

def certigo_converter(filename):

    f = open(filename)
    file_data = f.read()
    f.close()

    logging.warning(file_data)

    output_json = dict()

    if len(file_data) < 5:
        output_json["TOOL"] = "certigo"
        output_json["state"] = "timed out"
        return output_json

    data = json.loads(file_data)

    logging.warning(json.dumps(data, indent=2))

    output_json["TOOL"] = "certigo"

    return output_json
