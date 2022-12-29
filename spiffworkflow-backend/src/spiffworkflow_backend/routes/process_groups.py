# task_type = restplus_app.model('TaskType', { 'name': fields.String })
# return_task_type = restplus_app.model('ReturnTaskType', { 'name_two': fields.String })
# class TaskClass(fields.Raw):
#     def format(self, value):
#         return { 'name': value.name}
# @restplus_app.route('/hello', endpoint="this-this-what")
# @restplus_app.doc(params={'hey': {"description": 'not a thing', "type": int}})
# class HelloWorld(Resource):
#     @restplus_app.doc(model=task_type)
#     def get(self):
#         value = {'hello': 'world'}
#         return make_response(jsonify(value), 200)
#     # @restplus_app.doc(model=task_type, body=TaskClass)
#     @restplus_app.doc(model=return_task_type, body=task_type)
#     # @restplus_app.expect(TaskClass, validate=True)
#     # @restplus_app.response(400, 'Validation error')
#     # @restplus_app.response(201, 'WE GOT IT', return_task_type)
#     def post(self):
#         value = {'hello': 'world'}
#         return make_response(jsonify(value), 201)

from flask_restx import Api, Resource, fields, Namespace, reqparse
from spiffworkflow_backend.services.git_service import GitService
from flask import current_app
from flask import jsonify
from flask import g
import flask.wrappers
from flask import make_response
from spiffworkflow_backend.models.process_group import ProcessGroup, ProcessGroupSchema
from spiffworkflow_backend.services.process_model_service import ProcessModelService
from typing import Optional
from flask import request
import json

api = Namespace('process-groups', description='Process groups')

process_group = api.model('ProcessGroup', {'id': fields.String, 'name': fields.String, 'display_name': fields.String, 'display_order': fields.Integer})
pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument("page", type=int, location="args")
pagination_parser.add_argument("per_page", type=int, location="args")
pagination_parser.add_argument("process_group_identifier", type=str, location="args")


@api.route('')
@api.doc(params={
    'process_group_identifier': {"description": 'Optional parameter to filter by a single group', "type": str, "required": False},
})
class ProcessGroups(Resource):
    @api.expect(pagination_parser)
    @api.doc(params={
        'process_group_identifier': {"description": 'Optional parameter to filter by a single group', "type": str, "required": False},
        'page': {"description": "The page number to return. Defaults to page 1.", "type": int, "required": False},
        'per_page': {"description": "The number of groups to show per page. Defaults to page 10.", "type": int, "required": False},
    })
    @api.response(200, 'Process group list.', process_group)
    def get(self) -> flask.wrappers.Response:
        args = pagination_parser.parse_args()
        process_group_identifier = args['process_group_identifier']
        page = args['page'] or 1
        per_page = args['per_page'] or 100
        if process_group_identifier is not None:
            process_groups = ProcessModelService.get_process_groups(
                process_group_identifier
            )
        else:
            process_groups = ProcessModelService.get_process_groups()
        batch = ProcessModelService().get_batch(
            items=process_groups, page=page, per_page=per_page
        )
        pages = len(process_groups) // per_page
        remainder = len(process_groups) % per_page
        if remainder > 0:
            pages += 1

        response_json = {
            "results": ProcessGroupSchema(many=True).dump(batch),
            "pagination": {
                "count": len(batch),
                "total": len(process_groups),
                "pages": pages,
            },
        }
        return make_response(jsonify(response_json), 200)

    @api.expect(process_group, validate=True)
    @api.response(201, 'Process group was created.', process_group)
    def post(self) -> flask.wrappers.Response:
        body = json.loads(request.get_data().decode("utf-8"))
        process_group = ProcessGroup(**body)
        ProcessModelService.add_process_group(process_group)
        self._commit_and_push_to_git(
            f"User: {g.user.username} added process group {process_group.id}"
        )
        return make_response(jsonify(process_group), 201)

    def _commit_and_push_to_git(self, message: str) -> None:
        """Commit_and_push_to_git."""
        if current_app.config["GIT_COMMIT_ON_SAVE"]:
            git_output = GitService.commit(message=message)
            current_app.logger.info(f"git output: {git_output}")
        else:
            current_app.logger.info("Git commit on save is disabled")
