import json
import random

from agents.generation_agent import generation_agent
from agents.evolution_agent.depth import createConstraintsPrompt, createDeepenPrompt, createConcretizingPrompt, createReasoningPrompt
from agents.evolution_agent.breadth import createBreadthPrompt
from configuration import CONFIGURATION

def evolve_dataset(dataset):
	current_dataset = dataset
	for i in range(CONFIGURATION["evolution_depth"]):
		evolved_dataset = []	
		for dataset_row in current_dataset:
			dataset_row = json.dumps([dataset_row])
			evol_prompts = []
			evol_prompts.append(createConstraintsPrompt(dataset_row))
			evol_prompts.append(createDeepenPrompt(dataset_row))
			evol_prompts.append(createConcretizingPrompt(dataset_row))
			evol_prompts.append(createReasoningPrompt(dataset_row))
			evol_prompts.append(createBreadthPrompt(dataset_row))

			selected_evol_prompt = random.choice(evol_prompts)
			evolved_dataset_row = generation_agent(selected_evol_prompt, system_prompt="Always return the same schema as the input dataset no matter what so that it can be parsed later.")
			evolved_dataset.extend(evolved_dataset_row)
		dataset.extend(evolved_dataset)
		current_dataset = evolved_dataset
	return dataset



	




