import importlib
from typing import List, Dict, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

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


def add_job_id_to_data(data: Dict, id_key: str = 'id') -> List[Dict]:
    iiq_id = data.get(id_key)
    for item in data.get('data', []):
        item['job_id'] = iiq_id
    return data.get('data', [])


async def find_column_name_in_table(column_name: str, schema: str, table: str, db: AsyncSession) -> Optional[str]:
    """
    Check if a column exists in a specific table within a schema.

    :param column_name: The name of the column to check for.
    :param schema: The schema where the table is located.
    :param table: The table where the column should be checked.
    :param db: The asynchronous database session.
    :return: The column name if it exists, otherwise None.
    """
    query = text(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = :schema
          AND table_name = :table
          AND column_name = :column_name
        """
    )

    result = await db.execute(query, {'schema': schema, 'table': table, 'column_name': column_name})
    column = result.fetchone()
    return column[0] if column else None

