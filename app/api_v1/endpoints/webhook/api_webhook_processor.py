from http import HTTPStatus

from fastapi import APIRouter, Depends, BackgroundTasks

from app.schemas.webhook_schemas import WebhookRequestData
from app.services import webhook_service
from app.utils.webhook_utils import webhook_signature_validator

api_router = APIRouter(dependencies=[Depends(webhook_signature_validator)])


@api_router.post("/process", status_code=HTTPStatus.OK)
async def process_webhook(webhook_request_data: WebhookRequestData,
                          background_tasks: BackgroundTasks):
    background_tasks.add_task(webhook_service.process_webhook, webhook_request_data=webhook_request_data)
