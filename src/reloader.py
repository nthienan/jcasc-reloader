import logging
import requests


def reload_jcasc(*agrs, **keywords):
    logging.info("Reloading Jenkins configurations...")
    try:
        url = "%s/reload-configuration-as-code" % keywords["jenkins_url"]
        response = requests.post(url, verify=keywords["verify"],
            params={"casc-reload-token": keywords["token"]})
        response.raise_for_status()
    except Exception as err:
        logging.error("Reloaded Jenkins configurations was failed")
        logging.error("%s" % err)
    else:
        logging.info("Reloaded Jenkins configurations successfully")

