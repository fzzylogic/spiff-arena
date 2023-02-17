from SpiffWorkflow.bpmn.serializer.helpers.spec import BpmnSpecConverter
from SpiffWorkflow.bpmn.specs.data_spec import BpmnDataStoreSpecification

from spiffworkflow_backend.services.secret_service import SecretService

class SecretDataStore(BpmnDataStoreSpecification):
    """SecretDataStore - just for demonstration purposes."""
    def get(self, my_task):
        raise NotImplementedError("SecretDataStore does not yet implement get.")

    def set(self, my_task):
        raise NotImplementedError("SecretDataStore does not yet implement set.")

    def copy(self, source, destination, data_input=False, data_output=False):
        raise NotImplementedError("SecretDataStore does not yet implement copy.")

class SecretDataStoreConverter(BpmnSpecConverter):
    """SecretDataStoreConverter - just for demonstration purposes."""

    def __init__(self, registry):
        super().__init__(SecretDataStore, registry)

    def to_dict(self, spec):
        return {
            "name": spec.name,
            "description": spec.description,
            "capacity": spec.capacity,
            "is_unlimited": spec.is_unlimited,
        }

    def from_dict(self, dct):
        return SecretDataStore(**dct)
