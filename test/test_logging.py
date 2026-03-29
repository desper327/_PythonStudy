import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,filename="log.txt",filemode="a")
logger.info("T"*100)