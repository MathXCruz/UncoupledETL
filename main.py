from uncoupledetl.extract import (
    APIExtractor,
    get_specific_data,
    get_multiple_data,
)
from uncoupledetl.transform import WoWTransformer, PokeTransformer
from uncoupledetl.load import Loader, load_to_local_database
from uncoupledetl.variables import URL, ENDPOINTS, WOW_URL, WOW_ENDPOINT
import asyncio
import logging
import traceback
from sentry_sdk.integrations.logging import LoggingIntegration
import sentry_sdk
import os


async def main():
    wow_extractor = APIExtractor(WOW_URL, WOW_ENDPOINT)
    wow_data = await wow_extractor.get_data(get_specific_data)
    poke_extractor = APIExtractor(URL, ENDPOINTS)
    poke_data = await poke_extractor.get_data(get_multiple_data)
    transformed_wow = WoWTransformer(wow_data).transform()
    transformed_poke = PokeTransformer(poke_data).transform()
    await Loader(transformed_poke).load_strategy(load_to_local_database)
    logging.info('Test run completed.')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        filename='logs.log',
        format='%(name)s - %(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filemode='a',
    )

    sentry_logging = LoggingIntegration(
        level=logging.INFO, event_level=logging.INFO
    )

    sentry_sdk.init(
        dsn=os.environ.get('sentry_test'), integrations=[sentry_logging]
    )
    try:
        asyncio.run(main())
    except Exception as e:
        tb = ''.join(traceback.format_tb(e.__traceback__))
        tb = tb.replace('\n', ' - ')
        logging.critical(f'main(uncoupledetl): unexpected error - {e} {tb}')
        raise e
