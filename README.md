# Orchestration System

A Python package for creating and managing ETL pipelines through decorators.

## Overview

The Orchestration System allows users to define pipelines and jobs using simple Python decorators. 
The system handles metadata management, scheduling, and execution monitoring through a web interface.

## Features

- **Pipeline Management**: Define and schedule complete ETL workflows
- **Job Sequencing**: Control execution order of jobs within pipelines
- **Monitoring**: Track job execution history and resource usage
- **Git Integration**: Automatic cloning of pipeline repositories

## Installation

```bash
pip install orchestration-system
```

## Usage

### Defining Pipelines

```python
from orchestration.decorators import Pipeline, Job

@Pipeline(schedule="0 * * * *", active=True)
class MyETLPipeline:
    """Example pipeline for data processing"""
    
    @Job(execution_order=1)
    def extract_data(self):
        """Extract data from source"""
        pass
        
    @Job(execution_order=2)
    def transform_data(self):
        """Transform extracted data"""
        pass
```

**Key Features:**
- The class docstring automatically becomes the pipeline description
- Method docstrings automatically become job descriptions
- No need to duplicate descriptions in decorator parameters
- Keep documentation and implementation in one place
```

### Configuration

Create a `config.yaml` file in your project root:

```yaml
pipelines:
  - repo: "https://github.com/user/pipeline-repo.git"
    branch: "main"
    module_path: "pipelines.my_pipeline"
    class_name: "MyETLPipeline"
```

## Database Schema

The system uses PostgreSQL to store:
- Pipeline definitions and schedules
- Job configurations and execution order
- Historical execution data and metrics

See [migrations/initial_schema.sql](database/initial_schema.sql) for full schema details.

## Web Interface

The system includes a web-based dashboard for:
- Pipeline monitoring and control
- Execution history visualization
- Resource usage tracking

## Development

### Requirements

- Python 3.8+
- PostgreSQL 12+
- Redis (for task queue)

### Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up database:
   ```bash
   psql -f database/initial_schema.sql
   ```
