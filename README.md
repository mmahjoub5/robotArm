# robotArm
# Robotic Task Execution System

This project allows you to control a **6-DOF robotic arm** using **task execution commands**. It leverages **Webots** for robot simulation, **RabbitMQ** for task messaging, and **GPT** for generating tasks.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Overview

This system:
- Accepts tasks from the **high-level controller** (GPT).
- Executes these tasks on the robot (simulated using **Webots**).
- Communicates tasks asynchronously using **RabbitMQ**.

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/robotic-task-execution.git
cd robotic-task-execution 
```



### 2. Install Requirements
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```


### 3. Download and Run RabbitMQ & MongoDB
```bash
docker pull rabbitmq:management
docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:management
```
```bash
docker pull mongo
docker run -d -p 27017:27017 mongo
```

### 4. Install Webots 
Install Webots from here [WEBOTS DOWNLOAD](https://cyberbotics.com/doc/guide/installation-procedure), and make sure it’s added to your system PATH.


## Usage

### Run Server 

```bash
uvicorn ipr_worlds.backend.app.main:app --reload
```


