# AutoTAMP ([Website](https://yongchao98.github.io/MIT-REALM-AutoTAMP/))
Here we show the two examples on the single-agent environments: Chip Challenge and HouseWorld. The left codes and datasets are coming soon.

Paper Link: https://arxiv.org/pdf/2306.06531.pdf

<div align="center">
    <img src="Illustraton of three methods.png" alt="Main image" width="75%"/>
</div>

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

## Visualization
We have uploaded the AutoTAMP_plotting.ipynb and Example_results directory to give the visualization examples. During the experiments, myfile{i}.txt will be created to record the position/time waypoints, which are used for visualization when giving the environmental plots.

## Cite

@article{chen2023autotamp,
  title={AutoTAMP: Autoregressive Task and Motion Planning with LLMs as Translators and Checkers},
  author={Chen, Yongchao and Arkin, Jacob and Zhang, Yang and Roy, Nicholas and Fan, Chuchu},
  journal={arXiv preprint arXiv:2306.06531},
  year={2023}
}

## Recommended Work

[NL2TL: Transforming Natural Languages to Temporal Logics using Large Language Models](https://arxiv.org/pdf/2305.07766.pdf)

[Scalable Multi-Robot Collaboration with Large Language Models: Centralized or Decentralized Systems?](https://yongchao98.github.io/MIT-REALM-Multi-Robot/)
