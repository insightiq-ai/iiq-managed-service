from typing import List, Dict, Optional

from sqlalchemy import text
from sqlalchemy.orm import declarative_base

from app.events.db.deps import AsyncDataStore
from app.events.db.repository.jsql import jsql

Base = declarative_base()
metadata = Base.metadata


class BaseTemplatedRepository:

    def chunker(self, n, iterable):
        import itertools
        it = iter(iterable)
        while True:
            chunk = tuple(itertools.islice(it, n))
            if not chunk:
                return
            yield chunk

    async def db_commit(self, ds: AsyncDataStore):
        await ds.db.commit()

    async def sql(self, ds: AsyncDataStore, query, row, **kwargs):
        if row:
            query = text(jsql.render(query, kwargs))
            await ds.db.execute(query, row)

    async def sqlmany(self, ds: AsyncDataStore, query, rows, **kwargs):
        if rows:
            query = text(jsql.render(query, kwargs))

            chunks = self.chunker(100, rows)
            for chunk in chunks:
                await ds.db.execute(query, chunk)

    async def insert_one(self, ds: AsyncDataStore, table: str, data: Dict, schema: Optional[str] = None):
        if not data:
            return
        columns = list(data.keys())
        query_template = '''
            INSERT INTO {% if schema %}{{schema}}.{% endif %}{{ table }} 
            ({% for col in cols %}{{ col }}{{ comma if not loop.last }}{% endfor %}) 
            VALUES ({% for col in cols %}:{{ col }}{{ comma if not loop.last }}{% endfor %})
        '''
        await self.sql(ds=ds, query=query_template, cols=columns, table=table, schema=schema, row=data)

    async def insert_batch(self, ds: AsyncDataStore, table: str, data: List[Dict], schema: Optional[str] = None):
        if not data:
            return
        row = data[0]
        columns = list(row.keys())

        query_template = '''
            INSERT INTO {% if schema %}{{schema}}.{% endif %}{{ table }} 
            ({% for col in cols %}{{ col }}{{ comma if not loop.last }}{% endfor %}) 
            VALUES ({% for col in cols %}:{{ col }}{{ comma if not loop.last }}{% endfor %})
        '''
        await self.sqlmany(ds=ds, query=query_template, rows=data, cols=columns, table=table, schema=schema)

    async def upsert_one(self, ds: AsyncDataStore, table: str, data: Dict, unique_key: Optional[str] = None,
                         schema: Optional[str] = None):
        if not data:
            return
        columns_set: set = set(data.keys())
        if not await self.validate_unique_key(unique_key=unique_key, columns_set=columns_set):
            return await self.insert_one(ds=ds, table=table, data=data, schema=schema)

        columns = list(columns_set)
        query_template = '''
            INSERT INTO {% if schema %}{{schema}}.{% endif %}{{ table }} 
            ({% for col in cols %}{{ col }}{{ comma if not loop.last }}{% endfor %}) 
            VALUES ({% for col in cols %}:{{ col }}{{ comma if not loop.last }}{% endfor %}) 
            ON CONFLICT ({{unique_key}}) DO UPDATE SET 
            {% for col in cols %}{{ col }}=EXCLUDED.{{col}}{{ comma if not loop.last }}{% endfor %}
        '''
        await self.sql(ds=ds, query=query_template, cols=columns, unique_key=unique_key,
                       table=table, schema=schema, row=data)

    async def upsert_batch(self, ds: AsyncDataStore, table: str, data: List[Dict], unique_key: str,
                           schema: Optional[str] = None):
        if not data:
            return
        row = data[0]
        columns_set: set = set(row.keys())

        if not await self.validate_unique_key(unique_key=unique_key, columns_set=columns_set):
            return await self.insert_batch(ds=ds, table=table, data=data, schema=schema)

        columns = list(columns_set)

        query_template = '''
                    INSERT INTO {% if schema %}{{schema}}.{% endif %}{{ table }} 
                    ({% for col in cols %}{{ col }}{{ comma if not loop.last }}{% endfor %}) 
                    VALUES ({% for col in cols %}:{{ col }}{{ comma if not loop.last }}{% endfor %}) 
                    ON CONFLICT ({{unique_key}}) DO UPDATE SET 
                    {% for col in cols %}{{ col }}=EXCLUDED.{{col}}{{ comma if not loop.last }}{% endfor %} 
                '''
        await self.sqlmany(ds=ds, query=query_template, rows=data, cols=columns, unique_key=unique_key,
                           table=table, schema=schema)

    async def validate_unique_key(self, unique_key: str, columns_set: set):
        if not unique_key:
            return False

        for key in unique_key.split(','):
            if key.strip() not in columns_set:
                return False

        return True


base_templated_repository: BaseTemplatedRepository = BaseTemplatedRepository()
