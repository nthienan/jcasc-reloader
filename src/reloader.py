import logging
from subprocess import Popen, PIPE


def reload_jcasc(*agrs, **keywords):
    logging.info("Reloading Jenkins configurations...")
    try:
        url = "%s/reload-configuration-as-code/?casc-reload-token=%s" % (keywords["jenkins_url"], keywords["token"])
        cmd = "curl -X POST %s --fail --silent --show-error" % url
        if not keywords["verify"]:
            cmd = "%s --insecure" % cmd
        logging.debug("cmd: %s" % cmd)
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        stdout, stderr = p.communicate()
        logging.debug("stdout: %s" % stdout)
        logging.debug("stderr: %s" % stderr)
        if stderr:
            raise RuntimeError('An unexpected error occurred: %s' % stderr)
    except Exception as err:
        logging.error("%s" % err)
        logging.error("Reload Jenkins configurations was failed")
    else:
        logging.info("Reload Jenkins configurations successfully")

