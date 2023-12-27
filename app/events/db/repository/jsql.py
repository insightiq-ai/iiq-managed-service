from typing import Optional, Dict

import jinja2


class Jsql:
    jenv = jinja2.Environment(autoescape=False)
    jenv.globals["comma"] = ","

    def render(self, template: str, params: Optional[Dict] = None):
        return self.jenv.from_string(template).render(**params)


jsql = Jsql()
