"""Action functions."""

from __future__ import annotations

import tcod.ecs

from game.action import Action, Impossible, Success
from game.timesys import next_ticket, schedule


def do_action(actor: tcod.ecs.Entity, action: Action) -> None:
    """Apply an action and its side effects."""
    ticket = next_ticket(actor.registry)
    assert ticket.entity is actor
    match action(actor):
        case Success(time_cost=time_cost):
            schedule(actor, time_cost)
        case Impossible(msg=msg):
            print(msg)

    next_ticket(actor.registry)  # Progress timer
