"""Test_message_instance."""
import pytest
from flask import Flask
from flask.testing import FlaskClient
from tests.spiffworkflow_backend.helpers.base_test import BaseTest

from spiffworkflow_backend.models.db import db
from spiffworkflow_backend.models.message_instance import MessageInstanceModel
from spiffworkflow_backend.models.user import UserModel
from spiffworkflow_backend.services.process_model_service import ProcessModelService


class TestMessageInstance(BaseTest):
    """TestMessageInstance."""

    def setup_message_tests(self, client: FlaskClient, user: UserModel) -> str:
        """Setup_message_tests."""
        process_group_id = "test_group"
        process_model_id = "hello_world"
        bpmn_file_name = "hello_world.bpmn"
        bpmn_file_location = "hello_world"
        process_model_identifier = self.create_group_and_model_with_bpmn(
            client,
            user,
            process_group_id=process_group_id,
            process_model_id=process_model_id,
            bpmn_file_name=bpmn_file_name,
            bpmn_file_location=bpmn_file_location,
        )
        return process_model_identifier

    def test_can_create_message_instance(
        self,
        app: Flask,
        client: FlaskClient,
        with_db_and_bpmn_file_cleanup: None,
        with_super_admin_user: UserModel,
    ) -> None:
        """Test_can_create_message_instance."""
        message_name = "Message Model One"
        process_model_identifier = self.setup_message_tests(
            client, with_super_admin_user
        )

        process_model = ProcessModelService.get_process_model(
            process_model_id=process_model_identifier
        )
        process_instance = self.create_process_instance_from_process_model(
            process_model, "waiting"
        )

        queued_message = MessageInstanceModel(
            process_instance_id=process_instance.id,
            user_id=process_instance.process_initiator_id,
            message_type="send",
            name =message_name,
            payload={"Word":"Eat At Mashita's, delicious!"}
        )
        db.session.add(queued_message)
        db.session.commit()

        assert queued_message.status == "ready"
        assert queued_message.failure_cause is None

        queued_message_from_query = MessageInstanceModel.query.filter_by(  # type: ignore
            id=queued_message.id
        ).first()
        assert queued_message_from_query is not None

    def test_cannot_set_invalid_status(
        self,
        app: Flask,
        client: FlaskClient,
        with_db_and_bpmn_file_cleanup: None,
        with_super_admin_user: UserModel,
    ) -> None:
        """Test_cannot_set_invalid_status."""
        message_name = "message_model_one"
        process_model_identifier = self.setup_message_tests(
            client, with_super_admin_user
        )
        process_model = ProcessModelService.get_process_model(
            process_model_id=process_model_identifier
        )
        process_instance = self.create_process_instance_from_process_model(
            process_model, "waiting"
        )

        with pytest.raises(ValueError) as exception:
            MessageInstanceModel(
                process_instance_id=process_instance.id,
                user_id=process_instance.process_initiator_id,
                message_type="send",
                name=message_name,
                status="BAD_STATUS",
            )
        assert (
            str(exception.value) == "MessageInstanceModel: invalid status: BAD_STATUS"
        )

        queued_message = MessageInstanceModel(
            process_instance_id=process_instance.id,
            user_id=process_instance.process_initiator_id,
            message_type="send",
            name=message_name,
        )
        db.session.add(queued_message)
        db.session.commit()

        with pytest.raises(ValueError) as exception:
            queued_message.status = "BAD_STATUS"
        assert (
            str(exception.value) == "MessageInstanceModel: invalid status: BAD_STATUS"
        )

    def test_cannot_set_invalid_message_type(
        self,
        app: Flask,
        client: FlaskClient,
        with_db_and_bpmn_file_cleanup: None,
        with_super_admin_user: UserModel,
    ) -> None:
        """Test_cannot_set_invalid_message_type."""
        message_name = "message_model_one"
        process_model_identifier = self.setup_message_tests(
            client, with_super_admin_user
        )

        process_model = ProcessModelService.get_process_model(
            process_model_id=process_model_identifier
        )
        process_instance = self.create_process_instance_from_process_model(
            process_model, "waiting"
        )

        with pytest.raises(ValueError) as exception:
            MessageInstanceModel(
                process_instance_id=process_instance.id,
                user_id=process_instance.process_initiator_id,
                message_type="BAD_MESSAGE_TYPE",
                name=message_name
            )
        assert (
            str(exception.value)
            == "MessageInstanceModel: invalid message_type: BAD_MESSAGE_TYPE"
        )

        queued_message = MessageInstanceModel(
            process_instance_id=process_instance.id,
            user_id=process_instance.process_initiator_id,
            message_type="send",
            name=message_name,
        )
        db.session.add(queued_message)
        db.session.commit()

        with pytest.raises(ValueError) as exception:
            queued_message.message_type = "BAD_MESSAGE_TYPE"
        assert (
            str(exception.value)
            == "MessageInstanceModel: invalid message_type: BAD_MESSAGE_TYPE"
        )

    def test_force_failure_cause_if_status_is_failure(
        self,
        app: Flask,
        client: FlaskClient,
        with_db_and_bpmn_file_cleanup: None,
        with_super_admin_user: UserModel,
    ) -> None:
        """Test_force_failure_cause_if_status_is_failure."""
        message_name = "message_model_one"
        process_model_identifier = self.setup_message_tests(
            client, with_super_admin_user
        )

        process_model = ProcessModelService.get_process_model(
            process_model_id=process_model_identifier
        )
        process_instance = self.create_process_instance_from_process_model(
            process_model, "waiting"
        )

        queued_message = MessageInstanceModel(
            process_instance_id=process_instance.id,
            user_id=process_instance.process_initiator_id,
            message_type="send",
            name=message_name,
            status="failed",
        )
        db.session.add(queued_message)
        with pytest.raises(ValueError) as exception:
            db.session.commit()
        assert (
            str(exception.value)
            == "MessageInstanceModel: failure_cause must be set if status is failed"
        )
        assert queued_message.id is None
        db.session.remove()  # type: ignore

        queued_message = MessageInstanceModel(
            process_instance_id=process_instance.id,
            user_id=process_instance.process_initiator_id,
            message_type="send",
            name=message_name,
        )
        db.session.add(queued_message)
        db.session.commit()

        queued_message.status = "failed"
        queued_message.failure_cause = "THIS TEST FAILURE"
        db.session.add(queued_message)
        db.session.commit()
        assert queued_message.id is not None
        assert queued_message.failure_cause == "THIS TEST FAILURE"


