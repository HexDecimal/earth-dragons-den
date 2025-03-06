"""Action functions."""

from __future__ import annotations

import tcod.ecs

from game.action import Action, Impossible, Success
from game.components import AI
from game.timesys import next_ticket, schedule


def do_action(actor: tcod.ecs.Entity, action: Action) -> None:
    """Apply an action and its side effects."""
    ticket = next_ticket(actor.registry)
    assert ticket.entity is actor
    match action(actor):
        case Success(time_cost=time_cost):
            schedule(actor, time_cost)
        case Impossible(msg=msg):
            if AI in actor.components:
                schedule(actor, 100)
            print(msg)

    if ticket.entity.components.get(AI) is None:
        simulate(actor.registry)


def simulate(registry: tcod.ecs.Registry) -> None:
    """Simulate the world until a player entity is active."""
    while True:
        ticket = next_ticket(registry)
        ai = ticket.entity.components.get(AI)
        if ai is None:
            return
        do_action(ticket.entity, ai)
