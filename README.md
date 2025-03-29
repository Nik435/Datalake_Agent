# Reducing Computational Costs in NL2SQL Through Agentic Selective Data Access

## Overview
This code is part of the bachelor’s thesis Reducing Computational Costs in NL2SQL Through Agentic Selective Data Access by Dominik Jehle.
It was used to evaluate the Datalake Agent, an agent designed to reduce the number of input tokens required in TableQA using NL2SQL.

Abstract:
In this bachelor’s thesis, the impact of large database convolutes on NL2SQL methods
is explored. Processing such tasks on vast amounts of data requires a Large Language
Model (LLM) to handle large quantities of information, resulting into long prompts
and wherefore high process costs. To address this challenge, I introduce the Datalake
Agent an agent designed to assist an LLM by efficiently accessing large datasets.
Through a communication loop, the LLM can selectively request only the necessary
information to solve Table Question Answering tasks. The Datalake Agent provides
this information, significantly reducing the transfer of redundant data. For evaluation,
I implemented a database convolute consisting of 23 databases, including datasets
from RelBench populated with real-world-like data. The model leveraging the
Datalake Agent is tested on 100 Table Question Answering tasks and demonstrated
slightly improved performance on larger database sets compared to a direct solver
approach. The key advantage of the Datalake Agent is its ability to reduce the
required input information by up to 87%, leading to substantial cost reductions for
NL2SQL methods.

## How the Code is Organized
The code contains a the datalake agent a database connection layer (dbContext) and api service for the open Ai api.\
There are two ways to use the code:
1. Evaluation on 100 TableQA tasks.
2. Using the chat service to test custom questions.

## Getting Started

### Setup:
1. Install miniconda
2. Create conda environment with the environment file in root of repository:  
```bash
    conda env create -f environment.yml
```
3. The databases have to be included as a folder next to the datalake agent
4. An api key must be stored in a openAiSettings.json next to the datalake agent
5. The evaluation can be startet in main.py

### Include Databases
For evaluation, databases are needed.
There are two types of databases.
There are 18 simulated databases without any data and 5 real databases.\
The simulated databases and their descriptions can be found in:\
https://github.com/Nik435/databases


## External Databases from RelBench
The simulated databases must be extended by 5 RelBench databases\
Needed are:
1. avito.sqlite
2. stack.sqlite
3. trial.sqlite (must be renamed to clinicalTrial.sqlite )
4. hm.sqlite (must be renamed to hmShop.sqlite)
5. f1.sqlite (must be renamed to formula1.sqlite)
The databases must included into the databases folder\
The databases can be found on: https://relbench.stanford.edu/ \
The descriptions from RelBench their used in the dBdescription.json

Citation: Joshua Robinson, Rishabh Ranjan, Weihua Hu, Kexin Huang, Jiaqi Han, Alejandro
Dobles, Matthias Fey, Jan E. Lenssen, Yiwen Yuan, Zecheng Zhang, Xinwei He,
and Jure Leskovec. RelBench: A Benchmark for Deep Learning on Relational
Databases. Advances in Neural Information Processing Systems, 37:21330–21341,
December 2024. URL https://proceedings.neurips.cc/paper_files/paper/
2024/hash/25cd345233c65fac1fec0ce61d0f7836-Abstract-Datasets_and_
Benchmarks_Track.html

## API Key
The openAiSettings.json format is:\
{\
    "api_key": "[Api Key]",\
    "model": "gpt-4o-mini"\
}

### ChatService
To use the chat service the following code must not be commented out\
    chatAgent = ChatAgent(apiServiceChatAgent)\
    chatService = ChatService(chatAgent)\
    chatService.startChat()

### Evaluation
To use the evaluation the following code must not be commented out\
    chatAgent = ChatAgent(apiServiceChatAgent)\
    directSolver = DirectPromptSolver(apiServiceDP)\
    evaluation = Evaluation(chatAgent, directSolver)\
    evaluation.start()