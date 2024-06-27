from flask_restx import fields,Model

me_model = Model(
    "me_model",
    {        
        'public_id': fields.Integer(attribute='id'),
        "admin": fields.Boolean,
        "token_expires_at": fields.String,
        "username":fields.String
    },
)

user_model = Model(
    "user_model",
    {        
        'public_id': fields.Integer(attribute='id'),
        "admin": fields.Boolean,
        "username":fields.String
    },
)

all_users_list = Model("all_users_list", {
    'users': fields.List(fields.Nested(user_model))
})     