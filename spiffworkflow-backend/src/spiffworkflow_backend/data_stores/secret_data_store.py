"""secret_data_store."""
from flask import g
from SpiffWorkflow.bpmn.serializer.helpers.spec import BpmnSpecConverter
from SpiffWorkflow.bpmn.specs.data_spec import BpmnDataStoreSpecification

from spiffworkflow_backend.services.secret_service import SecretService
from spiffworkflow_backend.services.user_service import UserService


class SecretDataStore(BpmnDataStoreSpecification):
    """SecretDataStore - just for demonstration purposes."""

    def get(self, my_task):
        """get."""
        secret_value = SecretService.get_secret(self.name).value
        my_task.data[self.name] = secret_value

    def set(self, my_task):
        """set."""
        secret_value = my_task.data[self.name]
        user_id = g.user.id if UserService.has_user() else None
        SecretService.update_secret(self.name, secret_value, user_id, True)
        del my_task.data[self.name]

    def copy(self, source, destination, data_input=False, data_output=False):
        """copy."""
        raise NotImplementedError("SecretDataStore does not yet implement copy.")


class SecretDataStoreConverter(BpmnSpecConverter):
    """SecretDataStoreConverter - just for demonstration purposes."""

    def __init__(self, registry):
        """__init__."""
        super().__init__(SecretDataStore, registry)

    def to_dict(self, spec):
        """to_dict."""
        return {
            "name": spec.name,
            "description": spec.description,
            "capacity": spec.capacity,
            "is_unlimited": spec.is_unlimited,
        }

    def from_dict(self, dct):
        """from_dict."""
        return SecretDataStore(**dct)
