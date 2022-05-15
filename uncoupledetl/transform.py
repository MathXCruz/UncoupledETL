from typing import Protocol, List
from uncoupledetl.data_types import PokeSchema, PokeORM, WoWSchema

class TransformerFactory(Protocol):
    def __init__(self, data: dict) -> None:
        pass

    def transform(self, data) -> object:
        pass


class PokeTransformer:
    def __init__(self, data: List[dict]):
        self.data = data

    def transform(self) -> PokeORM:
        poke = parse_poke_batch(self.data)
        poke = poketypes_to_string(poke)
        return pydantic_to_pokeorm(poke)


class WoWTransformer:
    def __init__(self, data: dict):
        self.data = data

    def transform(self) -> WoWSchema:
        return parse_wow_dict(self.data)


def parse_poke_dict(pokemon: dict) -> PokeSchema:
    """Return the parsed data of the pokemon.
    Args:
        pokemon (dict): The dictionary of the pokemon data.
    Returns:
        PokeSchema: The parsed data of the pokemon in a pydantic object.
    """
    poke_dict = {
        'id': pokemon['id'],
        'name': pokemon['name'],
        'types': [poke['type']['name'] for poke in pokemon['types']],
        'weight': pokemon['weight'] / 10,
        'height': pokemon['height'] / 10,
        'sprite': pokemon['sprites']['front_default'],
    }
    return PokeSchema(**poke_dict)


def parse_poke_batch(pokemon: List[dict]) -> List[PokeSchema]:
    """Return the parsed data of all the pokemon.
    Args:
        pokemon (List[dict]): The list of all the pokemon data.
    Returns:
        List[PokeSchema]: The parsed data of all the pokemon.
    """
    return [parse_poke_dict(p) for p in pokemon]


def pydantic_to_pokeorm(pokemon: List[PokeSchema]) -> List[PokeORM]:
    """Convert the pydantic data to the ORM data.
    Args:
        pokemon (List[PokeSchema]): The list of all the pokemon data.
    Returns:
        List[PokeORM]: The list of all the pokemon data converted
         to the ORM format.
    """
    poke = []
    [
        poke.append(
            PokeORM(
                id=p.id,
                name=p.name,
                types=p.types,
                weight=p.weight,
                height=p.height,
                sprite=p.sprite,
            )
        )
        for p in pokemon
    ]
    return poke


def poketypes_to_string(pokemon: List[PokeSchema]) -> List[PokeSchema]:
    """Convert the types of the pokemon to a comma separated string.
    Args:
        pokemon (List[PokeSchema]): The list of all the pokemon data.
    Returns:
        List[PokeSchema]: The list of all the pokemon data with the
        types as a string.
    """
    for p in pokemon:
        p.types = ', '.join(p.types)
    return pokemon


def parse_wow_dict(data: dict) -> WoWSchema:
    wow_dict = {
    'name': data['name'],
    'race': data['race'],
    'Class': data['class'],
    'active_spec_name': data['active_spec_name'],
    'gender': data['gender'],
    'faction': data['faction']
}
    return WoWSchema(**wow_dict)