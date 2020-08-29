from flask_restful import Resource, reqparse
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity, \
    jwt_optional, fresh_jwt_required
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from flask import request
from werkzeug.security import safe_str_cmp
from hashlib import md5
# from blacklist import BLACKLIST
from models.assessment_result import AssessmentResultModel
from models.student import StudentModel

_assessment_result_parser = reqparse.RequestParser()
_assessment_result_parser.add_argument('result_id', type=int,
                                       store_missing=False)
_assessment_result_parser.add_argument('attempt_id', type=int,
                                       store_missing=False)
_assessment_result_parser.add_argument('student_id', type=int,
                                       store_missing=False)
_assessment_result_parser.add_argument('student_name', type=str,
                                       store_missing=False)
_assessment_result_parser.add_argument('subject_id', type=int,
                                       store_missing=False)
_assessment_result_parser.add_argument('subject_name', type=str,
                                       store_missing=False)
_assessment_result_parser.add_argument('category_id', type=int,
                                       store_missing=False)
_assessment_result_parser.add_argument('category_name', type=str,
                                       store_missing=False)
_assessment_result_parser.add_argument('skill_id', type=int,
                                       store_missing=False)
_assessment_result_parser.add_argument('skill_name', type=str,
                                       store_missing=False)
_assessment_result_parser.add_argument('period_id', type=int,
                                       store_missing=False)
_assessment_result_parser.add_argument('year', type=int, store_missing=False)
_assessment_result_parser.add_argument('month', type=int, store_missing=False)
_assessment_result_parser.add_argument('day', type=int, store_missing=False)
_assessment_result_parser.add_argument('session', type=str,
                                       store_missing=False)
_assessment_result_parser.add_argument('score', type=int, store_missing=False)
_assessment_result_parser.add_argument('full_score', type=str,
                                       store_missing=False)
_assessment_result_parser.add_argument('grade', type=str, store_missing=False)
_assessment_result_parser.add_argument('creation_date', type=str,
                                       store_missing=False)
_assessment_result_parser.add_argument('modified_date', type=str,
                                       store_missing=False)
_assessment_result_parser.add_argument('modified_by', type=str,
                                       store_missing=False)

class AssessmentResultList(Resource):

    @jwt_required
    def get(self):
        data = request.args
        results = AssessmentResultModel.find_assessment_result_by_any(**data)
        if results:
            resp = []
            for result in results:
                resp.append(result.json())
            return resp
        else:
            {'message': 'Results not found'}, 404


class AssessmentResult(Resource):
    @jwt_required
    def get(self):
        data = request.args
        # data = data.to_dict(flat=False)
        # data = _assessment_result_parser.parse_args()
        print(data)
        print(data.keys())
        if 'result_id' in data.keys():
            assessment_result = AssessmentResultModel.find_by_result_id(
                data['result_id'])
            if assessment_result:
                return assessment_result.json()
            else:
                return {'message': "Assessment result id not found"}, 404
        #
        #
        # student_ids = []
        # if 'kalika_kendra_id' in data.keys():
        #     try:
        #         students = StudentModel.find_by_student_kalika_kendra_id(data["kalika_kendra_id"])
        #         if students:
        #             for student in students:
        #                 student_ids.append(student.id)
        #         print(student_ids)
        #     except:
        #         return {'message': 'No students found'}, 404
        # elif 'cluster_id' in data.keys():
        #     try:
        #         students = StudentModel.find_by_student_cluster_id(data["cluster_id"])
        #         if students:
        #             for student in students:
        #                 student_ids.append(student.id)
        #         print(student_ids)
        #     except:
        #         return {'message': 'No students found'}, 404
        # elif 'kalika_kendra_name' in data.keys():
        #     try:
        #         students = StudentModel.find_by_student_kalika_kendra_name(
        #             data["kalika_kendra_name"])
        #         if students:
        #             for student in students:
        #                 student_ids.append(student.id)
        #         print(student_ids)
        #     except:
        #         return {'message': 'No students found'}, 404
        # elif 'cluster_name' in data.keys():
        #     try:
        #         students = StudentModel.find_by_student_cluster_name(
        #             data["cluster_name"])
        #         if students:
        #             for student in students:
        #                 student_ids.append(student.id)
        #         print(student_ids)
        #     except:
        #         return {'message': 'No students found'}, 404
        #
        # if student_ids:
        #     assessment_result = AssessmentResultModel.find_by_student_ids(
        #         student_ids)
        #     if assessment_result:
        #         return assessment_result.json()
        #     else:
        #         return {'message': "Assessment result not found"}, 404
        #
        # if 'subject_name' in data.keys() or 'student_name' in data.keys() or 'category_name' in data.keys() or 'skill_name' in data.keys():
        #     payload = {}
        #     if 'subject_name' in data.keys():
        #         payload['subject_name'] = data['subject_name']
        #     if 'student_name' in data.keys():
        #         payload['student_name'] = data['student_name']
        #     if 'category_name' in data.keys():
        #         payload['category_name'] = data['category_name']
        #     if 'skill_name' in data.keys():
        #         payload['skill_name'] = data['skill_name']
        #     assessment_results = AssessmentResultModel.find_assessment_result_by_any_name(
        #         **payload)
        #     if assessment_results:
        #         resp = []
        #         for result in assessment_results:
        #             resp.append(result.json())
        #         return resp, 200
        #     else:
        #         return {'message': 'No result found for the input'}, 404
        # else:
        #     # print(data)
        #     assessment_results = AssessmentResultModel.find_assessment_result_by_any(
        #         **data)
        #     if assessment_results:
        #         resp = []
        #         for result in assessment_results:
        #             resp.append(result.json())
        #         return resp, 200
        #     return {'message': 'Assessment result not found'}, 404

    @jwt_required
    def post(self):
        data = _assessment_result_parser.parse_args()
        assessment_results = AssessmentResultModel.find_assessment_result_by_any(
            **data)
        if assessment_results:
            return {'message':
                        f"Assessment result already exists with the details provided."}, 400
        if 'student_id' not in data.keys() or 'subject_id' not in data.keys() \
                or 'category_id' not in data.keys() \
                or 'skill_id' not in data.keys() \
                or 'period_id' not in data.keys():
            return {'message':
                        f"Not all mandatory columns(Student Id, Subject Id, Skill Id, Period Id and Category ID) provided."}, 401
        claims = get_jwt_claims()
        dt = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        data["modified_by"] = claims["email"]
        data["creation_date"] = dt
        data["modified_date"] = dt
        assessment_result = AssessmentResultModel(**data)
        try:
            assessment_result.save_to_db()
        except Exception as e:
            return {"message":
                        f"An error occurred inserting the assessment result details. Error: {repr(e)}"}, 500
        return assessment_result.json(), 201

    @jwt_required
    def delete(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        data = _assessment_result_parser.parse_args()
        assessment_results = AssessmentResultModel.find_assessment_result_by_any(
            **data)
        if assessment_results:
            for assessment_result in assessment_results:
                assessment_result.delete_from_db()
            return {
                'message': f"Assessment results deleted. Rows deleted: {len(assessment_results)}"}
        return {'message': 'Assessment results not found.'}, 404

    @jwt_required
    def put(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        data = _assessment_result_parser.parse_args()
        try:
            assessment_result_id = data["result_id"]
            assessment_result = AssessmentResultModel.find_by_result_id(
                assessment_result_id)
            if assessment_result:
                dt = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
                data["modified_date"] = dt
                data["modified_by"] = claims["email"]
                assessment_result.set_attribute(data)
                assessment_result.save_to_db()
            return assessment_result.json()
        except Exception as e:
            return {
                       'message': f"Assesment result could not be found. {repr(e)}"}, 404