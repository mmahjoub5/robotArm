
from typing import Literal
from typing import List, Dict, AnyStr
from abc import ABC, abstractmethod
from jinja2 import Environment, FileSystemLoader
from  shared.models import *
import os 
class LLMResponseManager(ABC):
    """
        Add history from LLM to the manager.
        
        :role: SYSTEM, USER, ASSITANT.
    """
    @abstractmethod
    def add_response(self, role: str, content: str) -> None:
        pass
    """
        Returns history of LLMs chat
    """
    
    @abstractmethod
    def get_responses(self) -> List[str]:
        pass
    
    """
        Allow indexing into the history list to retrieve an Interaction object.
        
        :param index: The index of the desired interaction.
        :return: The Interaction object at the specified index.
    """
    @abstractmethod
    def __getitem__(self, index:int) -> Dict[str, str]:
        pass

class InMemoryResponseManager(LLMResponseManager):
    def __init__(self):
        """Initialize an empty dict to store responses."""
        self.messages: List[Dict[str, str]] = []  # prompt and response pair, if multiple choices then a list  
        

    def add_response(self, **kwargs):
        role = kwargs.get("role")
        if not role in ["system", "user", "assistant"]:
            raise ValueError(f"Role in correct type: VALID TYPES: [system, user, assistant] give {role}")
        
        self.messages.append({"role": role, "content": kwargs['content']})
    
    def get_responses(self) -> List[Dict[str, str]]:
        return self.messages
    
    def __getitem__(self, index):
        """Common method to retrieve a specific item by index."""
        if 0 <= index < len(self.messages):
            return self.messages[index]
        else:
            raise IndexError("Response index out of range.")

class Autogen_InMemoryResponseManager(LLMResponseManager):
    def __init__(self):
        """Initialize an empty dict to store responses."""
        self.messages: List[Dict[str, str]] = []  # prompt and response pair, if multiple choices then a list  
    def add_response(self, **kwargs):
        self.messages.append({"name": kwargs['name'], "content": kwargs['content']})
        
    def get_responses(self) -> List[Dict[str, str]]:
        return self.messages
    
    def __getitem__(self, index):
        """Common method to retrieve a specific item by index."""
        if 0 <= index < len(self.messages):
            return self.messages[index]
        else:
            raise IndexError("Response index out of range.")


def format_robot_capabilities(robot_capabilities:RobotCapabilities):
    pass



    
def templateManager(environment:Enviroment,tasks:List, robot_type:str, robot_capabilities:RobotCapabilities,goal:GoalSpecifications,  **kwargs):
    # load template 
    # Define the directory containing your templates

    # Adjust this to your directory structure
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(script_dir, "templates")

    env = Environment(loader=FileSystemLoader(template_dir))


    # Update the lists by appending index + string
    updated_robot_tasks = [f"task name: {control}" for i, control in enumerate(tasks)]
   

    
    # Load the ChatGPT prompt template
    template = env.get_template("summarizeEnvironment.jinja2")
    # Define data for rendering
    data = {
        "position":environment.Position,
        "obstacles": environment.obstacles,
        "tasks": updated_robot_tasks,
        "robot_type": robot_type,
        "robot_capabilities": robot_capabilities.model_dump(),
        "example_one": kwargs.get("example_one"),
        "example_two": kwargs.get("example_two"),
        "goal": goal.model_dump(),
        **kwargs
    }

    prompt = template.render(data)
    return prompt

def reprompt_template(error:str):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(script_dir, "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("reprompt_gpt.jinja2") 
    data = {
        "error" : error
    }
    prompt = template.render(data)
    return prompt


    