
from spiffworkflow_backend.services.secret_service import SecretService

from typing import Dict, List, Any

from flask import Flask
from flask_oauthlib.client import OAuth
from hashlib import sha256
import base64

# TODO: get this from somewhere dynamic, admins need to edit from the UI
# TODO: also don't like the name
# TODO: build non scope request_token_params in remote_app
AUTHS = {
      "airtable": {
            "consumer_key": "SPIFF_SECRET:AIRTABLE_CONSUMER_KEY",
            "consumer_secret": "SPIFF_SECRET:AIRTABLE_CONSUMER_SECRET",
            "request_token_params": {
                  "code_verifier": sha256("code_verifier".encode("utf8")).hexdigest(),
                  "code_challenge": base64.urlsafe_b64encode(sha256("code_verifier".encode("utf-8")).digest())[:43],
                  "code_challenge_method": "S256",
                  "state": sha256("justtesting".encode("utf8")).hexdigest(),
                  "scope": "data.records:read schema.bases:read",
            },
            "base_url": "https://airtable.com/",
            "access_token_method": "POST",
            "access_token_url": "https://airtable.com/oauth2/v1/token",
            "authorize_url": "https://airtable.com/oauth2/v1/authorize",
            #"request_token_url": "https://airtable.com/oauth2/v1/token",
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

            for k in ["consumer_key", "consumer_secret"]:
                  if k in config:
                        config[k] = SecretService.resolve_possibly_secret_value(config[k])

            app = Flask(__name__)
            oauth = OAuth(app)
            remote_app = oauth.remote_app(service, **config)

            token_store = {}

            @remote_app.tokengetter
            def get_token(token=None):
                  return token_store.get('token')
            
            return remote_app