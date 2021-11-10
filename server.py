"""Script to run for the frontend.
This will enable access to a few important endpoints:
    /hits
    /get_responses
    /mturk
    /responses
The last two are particularly important.
"""

from flask import (Flask,
                   jsonify,
                   request)
import os
import goat
import json

STATIC_FOLDER = "/shared/ethanweber/friends/mturk/static"
CONFIG_TYPE = "pickn"
HIT_FOLDER = "/shared/ethanweber/friends/mturk/static/data/hits"
LOCAL_RESPONSE_FOLDER = "/shared/ethanweber/friends/mturk/static/data/local_responses"
RESPONSE_FOLDER = "/shared/ethanweber/friends/mturk/static/data/responses"

app = Flask(__name__, static_url_path="/static", static_folder=STATIC_FOLDER)
app.jinja_env.filters['zip'] = zip

# Get submitted mturk data locally.
@app.route('/mturk/externalSubmit', methods=["POST"])
def submit_external_submit():
    import pprint
    pprint.pprint(request)
    print(request.headers)
    print()
    content = request.form.to_dict()
    print(type(content))
    pprint.pprint(content)

    content["answer"] = json.loads(content["answer"])
    config_name = content["answer"]["GLOBAL_CONFIG_NAME"]
    filename = os.path.join(LOCAL_RESPONSE_FOLDER, config_name + ".json")
    goat.write_to_json(filename, content["answer"])
    return jsonify({"info": "saved to {}".format(filename)})


# Get the config paramters for HIT.
@app.route('/hits/<config_name>', methods=["GET"])
def hits(config_name):
    config_data = goat.load_from_json(os.path.join(HIT_FOLDER, config_name + ".json"))
    return jsonify(config_data)


# Get the config paramters for HIT.
@app.route('/get_responses/<config_name>', methods=["GET"])
def get_responses(config_name):
    config_data = goat.load_from_json(os.path.join(RESPONSE_FOLDER, config_name + ".json"))
    return jsonify(config_data)

# Get the config paramters for HIT.
@app.route('/get_local_responses/<config_name>', methods=["GET"])
def get_local_responses(config_name):
    config_data = goat.load_from_json(os.path.join(LOCAL_RESPONSE_FOLDER, config_name + ".json"))
    return jsonify(config_data)

# The MTurk task. <config_name> is used to specify the .json file config, specifying the task.
@app.route('/mturk/<config_name>', methods=["GET"])
def mturk(config_name):
    with open("pages/mturk.html", 'r') as file:
        html_as_str = file.read()
    modified_html = html_as_str.replace("${CONFIG_TYPE}", CONFIG_TYPE)
    modified_html = modified_html.replace("${CONFIG_NAME}", config_name)
    return modified_html


# Look at the responses from MTurk to see how people responded.
@app.route('/responses/<config_name>', methods=["GET"])
def responses(config_name):
    with open("pages/responses.html", 'r') as file:
        html_as_str = file.read()
    modified_html = html_as_str.replace("${CONFIG_TYPE}", CONFIG_TYPE)
    modified_html = modified_html.replace("${CONFIG_NAME}", config_name)
    return modified_html


if __name__ == '__main__':
    print("running server")
    app.run(debug=False, threaded=True, host="0.0.0.0", port=8891)