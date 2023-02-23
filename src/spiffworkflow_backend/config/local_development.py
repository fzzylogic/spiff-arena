"""Development."""
from os import environ

SPIFFWORKFLOW_BACKEND_PERMISSIONS_FILE_NAME = environ.get(
    "SPIFFWORKFLOW_BACKEND_PERMISSIONS_FILE_NAME", default="local_development.yml"
)

SPIFFWORKFLOW_BACKEND_LOG_LEVEL = environ.get(
    "SPIFFWORKFLOW_BACKEND_LOG_LEVEL", default="debug"
)

SPIFFWORKFLOW_BACKEND_RUN_BACKGROUND_SCHEDULER = (
    environ.get("SPIFFWORKFLOW_BACKEND_RUN_BACKGROUND_SCHEDULER", default="false")
    == "true"
)
SPIFFWORKFLOW_BACKEND_GIT_PUBLISH_CLONE_URL = environ.get(
    "SPIFFWORKFLOW_BACKEND_GIT_PUBLISH_CLONE_URL",
    default="https://github.com/sartography/sample-process-models.git",
)
SPIFFWORKFLOW_BACKEND_GIT_USERNAME = "sartography-automated-committer"
SPIFFWORKFLOW_BACKEND_GIT_USER_EMAIL = (
    f"{SPIFFWORKFLOW_BACKEND_GIT_USERNAME}@users.noreply.github.com"
)
