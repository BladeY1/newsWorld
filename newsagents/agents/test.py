import unittest
from newsagents.agents.custom_agent_state import CustomAgentState
from newsagents.agents.custom_state_manager import CustomStateManager

class TestCustomStateManager(unittest.TestCase):
    def test_state_initialization(self):
        # Create an initial state object
        initial_state = CustomAgentState(
            id="example_id",
            description="example_description",
            name="example_name",
            host_world_prompt="example_host_world_prompt",
            memory_ignored_event_types=set(),
            wakeup_event_types=set(),
            action_schema_chains=[],
            goals=[],
            plan=[],
            last_retrieved_memory="",
            other_thoughts_filled_parameters={},
            available_action_schemas={},
            available_entities=[],
            is_asleep=False,
            current_action_chain=[],
            emotion={"happiness": 0.0, "sadness": 0.0, "anger": 0.0},
            attitude={"optimism": 0.0, "pessimism": 0.0, "neutrality": 0.0}
        )
        
        # Initialize the custom state manager with the initial state
        state_manager = CustomStateManager(initial_state)
        
        # Check if state's emotion and attitude dictionaries are initialized as expected
        expected_emotion = {"happiness": 0.0, "sadness": 0.0, "anger": 0.0}
        expected_attitude = {"optimism": 0.0, "pessimism": 0.0, "neutrality": 0.0}
        
        # Assert the initialized values
        self.assertEqual(state_manager.state.emotion, expected_emotion)
        self.assertEqual(state_manager.state.attitude, expected_attitude)
        
        # Print out the initialized state for verification
        print("Initialized State:")
        print(state_manager.state.model_dump_json(indent=2))

if __name__ == '__main__':
    unittest.main()
