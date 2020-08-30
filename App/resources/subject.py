from flask_restful import Resource, reqparse
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
from models.cluster import ClusterModel
from models.subject import SubjectModel
from models.assessment_category import AssessmentCategoryModel
from models.assessment_skill import AssessmentSkillModel

_subject_parser = reqparse.RequestParser()
_subject_parser.add_argument('subject_id', required=False, type=int,
                             store_missing=False)
_subject_parser.add_argument('subject_name', required=False, type=str,
                             store_missing=False)
_subject_parser.add_argument('subject_code', type=str, store_missing=False,
                             help="If active flag. Default 1.")
_subject_parser.add_argument('isactive', type=str, store_missing=False,
                             help="If depricated flag. Default 0.")

class SubjectList(Resource):
    @jwt_required
    def get(self):
        data = request.args
        subjects = SubjectModel.find_by_any(**data)
        if subjects:
            if not data.get("hierarchy", False):
                resp = []
                for subject in subjects:
                    resp.append(subject.json())
                return resp, 200
            else:
                subject_resp_out = []
                for subject in subjects:
                    subject_resp_in = subject.json()
                    subject_id = subject.id
                    data1 = {'subject_id': subject_id}
                    categories = AssessmentCategoryModel.find_assessment_category_by_any(**data1)
                    category_resp_out = []
                    for category in categories:
                        category_resp_in = category.json()
                        category_id = category.id
                        data2 = {'category_id': category_id}
                        skills = AssessmentSkillModel.find_assessment_skill_by_any(**data2)
                        skill_resp = []
                        for skill in skills:
                            skill_resp.append(skill.json())
                        category_resp_in["skill"] = skill_resp
                        category_resp_out.append(category_resp_in)
                    subject_resp_in["category"] = category_resp_out
                    subject_resp_out.append(subject_resp_in)
                return subject_resp_out


class Subject(Resource):
    @jwt_required
    def get(self):
        data = request.args
        subject_id = data.get("subject_id")
        subject_name = data.get("subject_name")
        subject_code = data.get("subject_code")
        print(data)
        subjects = None
        if subject_name:
            subject = SubjectModel.find_by_subject_name(subject_name)
        elif subject_id:
            subject = SubjectModel.find_by_subject_id(subject_id)
        elif subject_code:
            subject = SubjectModel.find_by_subject_code(subject_code)
        # else:
        #     subjects = SubjectModel.find_all_subject()
        # except:
        #     subjects = SubjectModel.find_all_subject()
        # if subjects:
        #     if not data.get("hierarchy", False):
        #         resp = []
        #         for subject in subjects:
        #             resp.append(subject.json())
        #         return resp, 200
        #     else:
        #         subject_resp_out = []
        #         for subject in subjects:
        #             subject_resp_in = subject.json()
        #             subject_name = subject.subject_name
        #             categories = AssessmentCategoryModel.find_by_subject_name(subject_name)
        #             category_resp_out = []
        #             for category in categories:
        #                 category_resp_in = category.json()
        #                 category_id = category.id
        #                 skills = AssessmentSkillModel.find_by_category_id(category_id)
        #                 skill_resp = []
        #                 for skill in skills:
        #                     skill_resp.append(skill.json())
        #                 category_resp_in["skill"] = skill_resp
        #                 category_resp_out.append(category_resp_in)
        #             subject_resp_in["category"] = category_resp_out
        #             subject_resp_out.append(subject_resp_in)
        #         return subject_resp_out
        if subject:
            return subject.json()
        return {'message': 'Subject not found'}, 404

    #     
    # 
    # @jwt_required
    # def post(self):
    #     claims = get_jwt_claims()
    #     if not claims['is_admin']:
    #         return {'message': 'Admin privilege required.'}, 401
    #     data = _subject_parser.parse_args()
    #     cluster_name = data["cluster_name"]
    #     if ClusterModel.find_by_cluster_name(cluster_name):
    #         return {
    #                    'message': f"A cluster with name '{cluster_name}' already exists."}, 400
    #     cluster = ClusterModel(**data)
    #     try:
    #         cluster.save_to_db()
    #     except Exception as e:
    #         return {
    #                    "message": f"An error occurred inserting the cluster. Error: {repr(e)}"}, 500
    #     return cluster.json(), 201
    # 
    # @jwt_required
    # def delete(self):
    #     claims = get_jwt_claims()
    #     if not claims['is_admin']:
    #         return {'message': 'Admin privilege required.'}, 401
    #     data = _subject_parser.parse_args()
    #     cluster_name = data["cluster_name"]
    #     cluster = ClusterModel.find_by_cluster_name(cluster_name)
    #     if cluster:
    #         cluster.delete_from_db()
    #         return {'message': 'Cluster deleted.'}
    #     return {'message': 'Cluster not found.'}, 404
    # 
    # @jwt_required
    # def put(self):
    #     claims = get_jwt_claims()
    #     if not claims['is_admin']:
    #         return {'message': 'Admin privilege required.'}, 401
    #     data = _subject_parser.parse_args()
    #     cluster_name = data["cluster_name"]
    #     cluster = ClusterModel.find_by_cluster_name(cluster_name)
    #     if cluster:
    #         cluster.set_attribute(data)
    #     else:
    #         cluster = ClusterModel(**data)
    #     cluster.save_to_db()
    #     return cluster.json()
