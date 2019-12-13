"""
Initializes the orchestrator
"""
import sys
import os
sys.path.insert(1, os.getcwd()+"/../orchestrator")
sys.path.insert(2, os.getcwd()+"/../orchestrator/designPatterns")
from orchestrator import Orchestrator
if __name__ == "__main__":
	orchestrator = Orchestrator("flaskexample/flaskexample",5000,
                                5000,2, 4,
                                "cpu usage",{"strategy":"no scaling"})