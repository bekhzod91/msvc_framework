# Python
import logging

# Django
from django.conf import settings
from django.core.management.base import BaseCommand

from ...utils import get_broker
from ...tasks import register_tasks

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Subscribe'

    def handle(self, *args, **options):
        broker = get_broker()

        if settings.DEBUG:
            logger.warning('Disable DJANGO debug mode')

        logger.info('Start tasks')
        register_tasks()
        consumer = broker.consumer()
        consumer.subscribe()
