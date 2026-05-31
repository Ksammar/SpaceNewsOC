import logging
import time

import schedule

from app.config import settings
from app.services.parser import run_parser

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def job():
    logger.info("Scheduler: starting parser job")
    try:
        run_parser()
    except Exception as e:
        logger.error("Scheduler: parser job failed: %s", e)
    logger.info("Scheduler: parser job finished")


def main():
    interval = settings.parser_interval_hours
    logger.info(
        "Scheduler started. Parser will run every %d hour(s)", interval
    )

    schedule.every(interval).hours.do(job)

    job()

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
