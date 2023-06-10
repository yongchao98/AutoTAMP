# AutoTAMP
Here we show the two examples on the single-agent environments: Chip Challenge and HouseWorld. The left codes and datasets are coming soon.

## Requirements
Please install the Gurobi optimizer by following the instructions on the official website https://www.gurobi.com/products/gurobi-optimizer/
You might be eligible for a free academic license https://www.gurobi.com/academia/academic-program-and-licenses/

Then install the following Python packages.
```
pip install numpy matplotlib pypoman openai re random time copy
```

Then you need to get your OpenAI key from https://beta.openai.com/
Put that OpenAI key starting 'sk-' into the openai_func.py, line9

## Usage
Run the autotamp_single_agent.py to test the AutoTAMP method (with/without checkers). From line7 to line11, set up the parameters for syntactic check, semantic check, domain, your working path dir, and model choice. Then run the script:

```
python autotamp_single_agent.py
```

For testing the Task Planning method, also set up the parameters for domain, your working path dir, and model choice. Then run the script:

```
python llm_task_plan.py
```

The experimental results will appear in the dir experiment_result.
