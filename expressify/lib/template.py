import os
from typing import Dict, Any, Optional, List
import jinja2


class TemplateEngine:
    """
    Template engine interface for expressify
    """
    def __init__(self, templates_dir: str = 'templates'):
        self.templates_dir = templates_dir
        
    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Render a template with context data
        """
        raise NotImplementedError("Template engine must implement render method")


class Jinja2Engine(TemplateEngine):
    """
    Jinja2 template engine implementation
    """
    def __init__(self, templates_dir: str = 'templates', **options):
        super().__init__(templates_dir)
        
        # Default options for Jinja2
        self.options = {
            'autoescape': True,
            'extensions': [],
            'trim_blocks': True,
            'lstrip_blocks': True
        }
        
        # Update with user options
        self.options.update(options)
        
        # Create Jinja2 environment
        self.env = self._create_environment()
        
    def _create_environment(self) -> jinja2.Environment:
        """
        Create Jinja2 environment
        """
        # Ensure template directory exists
        if not os.path.exists(self.templates_dir):
            os.makedirs(self.templates_dir)
            
        # Create loader and environment
        loader = jinja2.FileSystemLoader(self.templates_dir)
        env = jinja2.Environment(
            loader=loader,
            autoescape=self.options['autoescape'],
            extensions=self.options['extensions'],
            trim_blocks=self.options['trim_blocks'],
            lstrip_blocks=self.options['lstrip_blocks']
        )
        
        return env
        
    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Render a template with context data
        """
        template = self.env.get_template(template_name)
        return template.render(**context)


# Default engine instance
default_engine = None


def create_engine(engine_type: str = 'jinja2', templates_dir: str = 'templates', **options) -> TemplateEngine:
    """
    Create and configure a template engine
    """
    global default_engine
    
    if engine_type == 'jinja2':
        engine = Jinja2Engine(templates_dir, **options)
    else:
        raise ValueError(f"Unsupported template engine: {engine_type}")
        
    # Set as default if not already set
    if default_engine is None:
        default_engine = engine
        
    return engine


def get_default_engine() -> Optional[TemplateEngine]:
    """
    Get the default template engine
    """
    return default_engine 