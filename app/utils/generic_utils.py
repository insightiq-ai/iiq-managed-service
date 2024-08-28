import importlib

from app.utils.constants import PROFESSIONAL_WORK_PLATFORM_IDS


def get_method_from_method_path_string(method_path: str):
    # Split the path into module and function components
    module_name, _, method_name = method_path.rpartition('.')

    try:
        # Import the module dynamically
        if module_name:
            module = importlib.import_module(module_name)
            return getattr(module, method_name)
        else:
            return eval(method_name)

    except ImportError:
        print(f"Module {module_name} not found")
    except AttributeError:
        print(f"Method {method_name} not found in module {module_name}")


def is_professional_platform(work_platform_id: str) -> bool:
    return work_platform_id in PROFESSIONAL_WORK_PLATFORM_IDS
