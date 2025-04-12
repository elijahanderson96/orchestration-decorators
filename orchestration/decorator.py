import inspect
import logging
from functools import wraps
from typing import Optional


def Pipeline(schedule: str, active: bool = True):
    """Decorator that registers a class as a pipeline and collects metadata."""

    def decorator(cls):
        if not inspect.isclass(cls):
            raise TypeError('Pipeline decorator only works for classes.')

        # Store pipeline metadata
        cls._pipeline_metadata = {
            'module_name': cls.__module__,
            'pipeline_name': cls.__name__,
            'description': cls.__doc__ or '',
            'active': active,
            'cron_schedule': schedule
        }

        # Track all jobs in the pipeline
        cls._jobs = []
        cls._state = {}

        def get_metadata(self):
            """Returns collected metadata about the pipeline and its jobs."""
            return {
                'pipeline': self._pipeline_metadata,
                'jobs': [{
                    'job_name': job.__name__,
                    'execution_order': job._job_metadata['execution_order'],
                    'description': job._job_metadata['description']
                } for job in self._jobs]
            }

        def execute_job(self, job_name: str):
            """Execute a specific job in the pipeline with state sharing."""
            self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")

            # Initialize pipeline state
            if not hasattr(self, '_execution_state'):
                self._execution_state = {
                    'current_job': job_name,
                    'previous_jobs': []
                }
            else:
                self._execution_state['current_job'] = job_name

            try:
                for job in self._jobs:
                    if job.__name__ == job_name:
                        # Execute job and track execution
                        result = job(self)
                        self._execution_state['previous_jobs'].append({
                            'name': job_name,
                            'success': True,
                            'result': result
                        })
                        return result

                raise ValueError(f"Job {job_name} not found in pipeline")

            except Exception as e:
                self.logger.error(f"Job {job_name} failed: {str(e)}")
                self._execution_state['previous_jobs'].append({
                    'name': job_name,
                    'success': False,
                    'error': str(e)
                })
                raise

        cls.get_metadata = get_metadata
        cls.execute_job = execute_job

        # Register all jobs
        for name, method in cls.__dict__.items():
            if hasattr(method, 'register_job'):
                method.register_job(cls)

        return cls

    return decorator


def Job(execution_order: int, description: Optional[str] = None):
    """Decorator that registers a method as a pipeline job.
    
    The method docstring will be used as the job description if none provided.
    """

    def decorator(method):
        if not inspect.isfunction(method):
            raise TypeError('Job decorator only works for methods.')

        # Store job metadata
        method._job_metadata = {
            'execution_order': execution_order,
            'description': description or method.__doc__
        }

        @wraps(method)
        def wrapper(*args, **kwargs):
            return method(*args, **kwargs)

        # Store the original method and its metadata
        wrapper._original_method = method
        wrapper._job_metadata = method._job_metadata

        # This will be called when the class is created
        def register_job(cls):
            if not hasattr(cls, '_jobs'):
                cls._jobs = []
            cls._jobs.append(wrapper)
            cls._jobs.sort(key=lambda x: x._job_metadata['execution_order'])
            return cls

        # Attach the registration function to be called by the Pipeline decorator
        wrapper.register_job = register_job

        return wrapper

    return decorator
