from uuid import uuid4
from typing import List, Type
from genworlds.events.abstracts.action import AbstractAction

from genworlds.worlds.abstracts.world import AbstractWorld
from genworlds.worlds.abstracts.world_entity import AbstractWorldEntity
from genworlds.agents.abstracts.agent import AbstractAgent
from genworlds.objects.abstracts.object import AbstractObject

from newsagents.world.custom_actions import (
    WorldSendsAvailableEntities,
    WorldSendsAvailableActionSchemas,
    UpdateAgentAvailableEntities,
    UpdateAgentAvailableActionSchemas
)


class CustomWorld(AbstractWorld):
    def __init__(
        self,
        name: str,
        description: str,
        agents: List[AbstractAgent] = [],
        objects: List[AbstractObject] = [],
        actions: List[Type[AbstractAction]] = [],
        id: str = None,
    ):

        # availability = all entities
        get_available_entities = WorldSendsAvailableEntities(host_object=self)
        get_available_action_schemas = WorldSendsAvailableActionSchemas(
            host_object=self
        )
        actions.append(get_available_entities)
        actions.append(get_available_action_schemas)
        actions.append(UpdateAgentAvailableEntities(host_object=self))
        actions.append(UpdateAgentAvailableActionSchemas(host_object=self))

        super().__init__(
            id=id,
            name=name,
            description=description,
            agents=agents,
            objects=objects,
            actions=actions,
            get_available_entities=get_available_entities,
            get_available_action_schemas=get_available_action_schemas,
        )
