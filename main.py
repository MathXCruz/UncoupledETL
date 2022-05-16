from uncoupledetl.extract import (
    APIExtractor,
    get_specific_data,
    get_multiple_data,
)
from uncoupledetl.transform import WoWTransformer, PokeTransformer
from uncoupledetl.load import Loader, load_to_local_database
from uncoupledetl.variables import URL, ENDPOINTS, WOW_URL, WOW_ENDPOINT
import asyncio


async def main():
    wow_extractor = APIExtractor(WOW_URL, WOW_ENDPOINT)
    wow_data = await wow_extractor.get_data(get_specific_data)
    poke_extractor = APIExtractor(URL, ENDPOINTS)
    poke_data = await poke_extractor.get_data(get_multiple_data)
    transformed_wow = WoWTransformer(wow_data).transform()
    transformed_poke = PokeTransformer(poke_data).transform()
    await Loader(transformed_poke).load_strategy(load_to_local_database)


if __name__ == '__main__':
    asyncio.run(main())
