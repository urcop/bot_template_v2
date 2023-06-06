import logging

logging.basicConfig(
    level=logging.INFO,
    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(message)s'
)

logger = logging.getLogger(__name__)
