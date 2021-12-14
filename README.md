This project contains the custom code to train DMC agents on Keezen. The folder structur could be copied over a RLCard project. Just register the keezen environment in the __init__.py.  
  
The folder structure:  

`/examples/experiments/dmc_keezen_result/keezenexpid7` -> experiment folder with a generated model and a processed.csv with tournament results against randomly playing agents.  
`/rlcard/envs/keezen.py` -> the keezen environment  
`/rlcard/games/keezen/agent.py` -> rule-based agent  
`/rlcard/games/keezen/board.py`  
`/rlcard/games/keezen/card.py`  
`/rlcard/games/keezen/cardop.py`  
`/rlcard/games/keezen/game.py` -> game implementation that uses other classes, like Board, Card, Move, Player, etc.  
`/rlcard/games/keezen/keezengameadapter.py` -> adapter class to adapt the keezen game to the RLCard environment  
`/rlcard/games/keezen/move.py`  
`/rlcard/games/keezen/player.py`  
`/rlcard/games/keezen/rules.py`  
  
The project operated with the following scripts (in the examples directory):  

`create_graph_rnd.py` -> Picks the last generated model and start a tournament against randomly playing agents.  
`create_graph_values.py` -> Generates a graph with the results of tournament values.  
`evaluate_keezen_man.py` -> Manual analyzer. Observe a game of four trained models.  
`evaluate_keezen_rb.py` -> Run tournaments of trained models against rule-based agents.  
`evaluate_keezen_rnd` -> Runs tournaments of trained models against randomly playing agents.  
`evaluate_keezen_versions.py` -> Run tournament between two versions of trained models.  
`run_dmc_keezen.py` ->Train DMC on Keezen.  
