from flask import request
from flask_accepts import accepts
from flask_restplus import Namespace, Resource

from app.api.interface import QueryParams
from app.models import DSCR
from app.service import DataService
from app.utils import get_eager_query

def api_factory(schemas):
    api = Namespace('DSCR', description='Baltimore City district court criminal cases')

    dscr_schema = schemas['DSCR']
    dscr_schema_full = schemas['DSCRFull']
    dscr_schema_results = schemas['DSCRResults']

    @api.route('/dscr')
    class DSCRResource(Resource):
        '''DSCR'''

        @accepts(schema=QueryParams, api=api)
        @api.marshal_with(dscr_schema_results)
        def post(self):
            '''Get a list of Baltimore City district court criminal cases'''

            return DataService.fetch_rows_orm('dscr', request.parsed_obj)

    @api.route('/dscr/<string:case_number>')
    class DSCRResourceCaseNumber(Resource):
        '''DSCR by case number'''

        @accepts(dict(name='case_number', type=str), api=api)
        @api.marshal_with(dscr_schema)
        def get(self, case_number):
            return DSCR.query.filter(DSCR.case_number == case_number).one()

    @api.route('/dscr/<string:case_number>/full')
    class DSCRResourceCaseNumberFull(Resource):
        '''DSCR full case details by case number'''

        @accepts(dict(name='case_number', type=str), api=api)
        @api.marshal_with(dscr_schema_full)
        def get(self, case_number):
            return get_eager_query(DSCR).filter(DSCR.case_number == case_number).one()

    return api
