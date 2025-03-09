"""World initialization."""

from __future__ import annotations

from collections.abc import Iterable
from random import Random

import tcod.ecs

from game.action_logic import simulate
from game.actions import HostileAI
from game.actor_logic import spawn_actor
from game.components import HP, Graphic, Location, MaxHP, Offset, Str, Vector2
from game.faction import Faction
from game.map_gen import generate_cave_map
from game.tags import FacetOf, IsActor, IsItem, IsPlayer
from game.tile import Tile, TileDB
from game.timesys import schedule
from game.travel import force_move


def init_world(registry: tcod.ecs.Registry) -> None:
    """Initialize or reinitialize a world."""
    registry[None].components.setdefault(Random, Random())
    tile_db = registry[None].components.setdefault(TileDB, TileDB())
    tile_db.assign(Tile(name="bedrock", ch=ord("#")))
    tile_db.assign(Tile(name="dirt wall", ch=ord("-"), bg=(0x80, 0, 0), dig_cost=100, excavated_tile="dirt floor"))
    tile_db.assign(Tile(name="dirt floor", ch=ord("."), bg=(0x40, 0, 0), transparent=True, move_cost=100))
    tile_db.assign(
        Tile(name="rock wall", ch=ord("="), bg=(0x40, 0x40, 0x40), dig_cost=400, excavated_tile="rock floor")
    )
    tile_db.assign(Tile(name="rock floor", ch=ord("."), bg=(0x20, 0x20, 0x20), transparent=True, move_cost=100))
    tile_db.assign(
        Tile(name="grass", ch=ord("."), fg=(0x0, 0x80, 0x0), bg=(0x00, 0x20, 0x00), transparent=True, move_cost=100)
    )

    gold = registry["gold"]
    gold.components[Graphic] = Graphic(ord("$"))
    gold.tags.add(IsItem)

    kobold = registry["kobold"]
    kobold.components[Graphic] = Graphic(ord("k"))
    kobold.components[Str] = 2
    kobold.components[MaxHP] = 4

    orc = registry["orc"]
    orc.components[Graphic] = Graphic(ord("o"))
    orc.components[Str] = 3
    orc.components[MaxHP] = 8

    human = registry["human"]
    human.components[Graphic] = Graphic(ord("U"))
    human.components[Str] = 3
    human.components[MaxHP] = 8


def _configure_multi_tile_entity(entity: tcod.ecs.Entity, graphic: Iterable[str]) -> None:
    registry = entity.registry
    for facet in list(registry.Q.all_of(relations=[(FacetOf, entity)])):
        facet.clear()
    for y, row in enumerate(graphic):
        for x, ch in enumerate(row):
            facet = registry[object()]
            facet.components[Offset] = Vector2(x=x, y=y)
            facet.components[Graphic] = Graphic(ord(ch))
            facet.relation_tag[FacetOf] = entity


def new_world() -> tcod.ecs.Registry:
    """Return a newly created world."""
    registry = tcod.ecs.Registry()
    init_world(registry)

    map_ = generate_cave_map(registry)

    player = registry["player"]
    player.tags |= {IsPlayer, Faction.Player, IsActor}

    player.components[Str] = 12
    player.components[HP] = 100

    _2x2 = ("@┐", "└┘")
    _2x2b = ("@▜", "▙▟")
    _3x3 = ("┌─┐", "│@│", "└─┘")
    _3x3b = ("▛▀▜", "▌@▐", "▙▄▟")
    _configure_multi_tile_entity(player, _3x3)

    force_move(player, Location(1, 32, map_))
    schedule(player, 0)

    for p in [Location(1, 29, map_), Location(1, 30, map_), Location(2, 29, map_), Location(2, 30, map_)]:
        spawn_actor(registry["kobold"], pos=p, ai=HostileAI(), faction=Faction.Player)

    simulate(registry)

    return registry
