
from spiffworkflow_backend.services.secret_service import SecretService

from typing import Dict, List, Any

from flask import Flask
from flask_oauthlib.client import OAuth

# TODO: get this from somewhere dynamic, admins need to edit from the UI
# TODO: ^ in the interim, need to get client_id/secret from env? secrets?
# TODO: also don't like the name
AUTHS = {
      "airtable": {
            "name": "airtable",
            "version": "2",
            "client_id": "secret:AIRTABLE_CLIENT_ID",
            "client_secret": "secret:AIRTABLE_CLIENT_SECRET",
            "endpoint_url": "https://airtable.com/",
            "authorization_url": "https://airtable.com/oauth2/v1/authorize",
            "access_token_url": "https://airtable.com/oauth2/v1/token",
            "refresh_token_url": "https://airtable.com/oauth2/v1/token",
            "scope": "data.records:read schema.bases:read",
      },
}

class OAuthService:
      @staticmethod
      def authentication_list() -> List[Dict[str, Any]]:
            return [{"id": f"{k}/OAuth", "parameters": []} for k in AUTHS.keys()]

      @staticmethod
      def supported_service(service: str) -> bool:
            return service in AUTHS

      @staticmethod
      def remote_app(service: str) -> Any: # TODO what is this type
            config = AUTHS[service].copy()

            for k in ["client_id", "client_secret"]:
                  if k in config:
                        config[k] = SecretService.resolve_possibly_secret_value(config[k])

            app = Flask(__name__)
            oauth = OAuth(app)
            remote_app = OAuth.remote_app(**config)
                        
            return remote_app
