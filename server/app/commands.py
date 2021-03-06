import json
import click
from flask.cli import with_appcontext

@click.command()
@with_appcontext
def print_schema():
    from graphql.utils import schema_printer
    from app import graphql_service
    schema = graphql_service.get_schema()
    schema_str = schema_printer.print_schema(schema)
    with open('schema.graphql', 'w') as schemafile:
        schemafile.write(schema_str)

@click.command()
@with_appcontext
def print_swagger_spec():
    from flask_restplus import Swagger
    from app import app, rest_api
    with app.test_request_context(), open('swagger.json', 'w') as specfile:
        spec = Swagger(rest_api.api).as_dict()
        specfile.write(
            json.dumps(
                spec,
                sort_keys=True,
                indent=4,
                separators=(',', ': ')
            )
        )
