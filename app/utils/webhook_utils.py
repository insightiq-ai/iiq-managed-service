import hashlib
import hmac
import logging
import sys
from http import HTTPStatus

from fastapi import HTTPException
from starlette.requests import Request

from app.core.config import settings


async def webhook_signature_validator(request: Request):

    signatures = request.headers.get('Phyllo-Signatures') or request.headers.get('Webhook-Signatures')
    body = await request.body()
    if not signatures:
        logging.warning("Webhook Signatures are missing in the headers.")
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)

    requested_signatures = signatures.split(",")

    if not requested_signatures:
        logging.warning("Webhook Signatures are empty in the headers.")
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)

    for req_signature in requested_signatures:

        if await _validate_signature(body, req_signature):
            return True

    logging.warning("Signature is invalid")
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)


async def _validate_signature(body, req_signature: str):
    if str(settings.TENANT_APP_SECRET):
        signature = _generate_signature(message=body, key=str(settings.TENANT_APP_SECRET))

        if hmac.compare_digest(req_signature, signature):
            return True

    return False


def _generate_signature(message, key: str) -> str:
    if sys.version_info[0] == 3:  # pragma: no cover
        if not isinstance(key, bytes):
            key = bytes(key, 'utf-8')
        if not isinstance(message, bytes):
            message = bytes(message, 'utf-8')

    dig = hmac.new(key=key, msg=message, digestmod=hashlib.sha256)
    return dig.hexdigest()
