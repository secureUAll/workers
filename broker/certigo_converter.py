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

    else:
        try:
            data = json.loads(file_data)
        except ValueError as error:
            logging.warning("not loadable")
            output_json["TOOL"] = "certigo"
            output_json["state"] = "timed out"
            return output_json


        #logging.warning(json.dumps(data, indent=2))

        output_json["state"] = "up"

        output_json["TOOL"] = "certigo"

        output_json["scan"] = list()

        if "certificates" in data:
            for certificate in data["certificates"]:
                each_cert = dict()
                each_cert["valid_after"] = certificate["not_before"] if ("not_before" in certificate) else None
                each_cert["valid_until"] = certificate["not_after"] if ("not_after" in certificate) else None
                each_cert["algorithm"] = certificate["signature_algorithm"] if ("signature_algorithm" in certificate) else None
                each_cert["algorithm"] = certificate["signature_algorithm"] if ("signature_algorithm" in certificate) else None

                each_cert["issuer"] = dict()

                each_cert["issuer"] = certificate["issuer"] if ("issuer" in certificate) else None
                each_cert["key_usage"] = certificate["key_usage"] if ("key_usage" in certificate) else None
                each_cert["pem"] = certificate["pem"] if ("pem" in certificate) else None

                output_json["scan"].append(each_cert)


        output_json["tls"] = data["tls_connection"] if ("tls_connection" in data) else None
        output_json["verification"] = data["verify_result"] if ("verify_result" in data) else None

        logging.warning(json.dumps(output_json, indent=2))


    return output_json
