from jinja2 import Environment, FileSystemLoader
import os

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")

env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=False,  # HTML 不做 auto escape to avoid breaking HTML tags
)

def render_template(name: str, **kwargs) -> str:
    template = env.get_template(name)
    return template.render(**kwargs).strip()
