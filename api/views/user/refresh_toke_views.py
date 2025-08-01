from flask_restful import Resource
from api import api
from ...schemas.user import login_schema
from flask import request, make_response, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from datetime import timedelta


class RefreshTokenList(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """
        Serve para gerar um novo token, qundo token anterior é vencido
        ---
        tags: [Login]
        parameters:
          - name: Authorization
            in: header
            required: true
            description: Token de refresh no formato 'Bearer <token>'
            type: string
        responses:
          200:
            description: Novo token gerado com sucesso
          400:
            description: Erro de validação
          401:
            description: Token inválido ou ausente             
        """
        user_token = get_jwt_identity()
        access_token = create_access_token(
            identity=user_token,
            expires_delta=timedelta(seconds=100)
        )
        refresh_token = create_refresh_token(
            identity=user_token
        )

        return make_response({
            'access_token':access_token,
            'refresh_token':refresh_token
        }, 200)



api.add_resource(RefreshTokenList, '/token/refresh')
