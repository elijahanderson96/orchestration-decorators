from importlib.metadata import version, PackageNotFoundError

from .decorator import Pipeline, Job

__all__ = ['Pipeline', 'Job']

try:
    __version__ = version("orchestration")
except PackageNotFoundError:
    __version__ = "0.0.0"  # package not installed
