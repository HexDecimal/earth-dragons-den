"""Time system."""

from __future__ import annotations

import heapq
from typing import Final, NamedTuple

import tcod.ecs


class Ticket(NamedTuple):
    """Scheduled task item."""

    time: int
    uid: int
    entity: tcod.ecs.Entity


Tick: Final = ("Tick", int)
NextTicketUID: Final = ("NextTicketUID", int)
TurnQueue: Final = ("TurnQueue", list[Ticket])


def schedule(entity: tcod.ecs.Entity, interval: int) -> Ticket:
    """Schedule an entity to run after an interval."""
    registry = entity.registry
    entity.components[Ticket] = ticket = Ticket(
        time=registry[None].components.setdefault(Tick, 0) + interval,
        uid=registry[None].components.setdefault(NextTicketUID, 0),
        entity=entity,
    )
    queue = registry[None].components.setdefault(TurnQueue, [])
    heapq.heappush(queue, ticket)
    registry[None].components[NextTicketUID] += 1
    return ticket


def next_ticket(registry: tcod.ecs.Registry) -> Ticket:
    """Return the next valid Ticket."""
    queue = registry[None].components[TurnQueue]
    while queue[0] is not queue[0].entity.components.get(Ticket):
        heapq.heappop(queue)
    registry[None].components[Tick] = queue[0].time
    return queue[0]
