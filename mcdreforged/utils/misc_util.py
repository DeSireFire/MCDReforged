"""
Misc tool collection
"""
import importlib.machinery
import importlib.util
import sys
import threading
from typing import List, Any, Callable, Tuple

from mcdreforged.plugin.version import Version
from mcdreforged.rtext import RTextBase


def start_thread(func: Callable, args: Tuple, name: str or None = None):
	thread = threading.Thread(target=func, args=args, name=name)
	thread.setDaemon(True)
	thread.start()
	return thread


def load_source(path: str, name=None):
	if name is None:
		name = path.replace('/', '_').replace('\\', '_').replace('.', '_')
	spec = importlib.util.spec_from_file_location(name, path)
	module = importlib.util.module_from_spec(spec)
	sys.modules[name] = module
	spec.loader.exec_module(module)
	return module


def unique_list(lst: List[Any]) -> List[Any]:
	ret = list(set(lst))
	ret.sort(key=lst.index)
	return ret


def get_all_base_class(cls):
	if cls is object:
		return []
	ret = [cls]
	for base in cls.__bases__:
		ret.extend(get_all_base_class(base))
	return unique_list(ret)


def version_compare(v1: str, v2: str) -> int:
	version1 = Version(v1, allow_wildcard=False)
	version2 = Version(v2, allow_wildcard=False)
	return version1.compare_to(version2)


def print_text_to_console(logger, text):
	for line in RTextBase.from_any(text).to_colored_text().splitlines():
		logger.info(line)
