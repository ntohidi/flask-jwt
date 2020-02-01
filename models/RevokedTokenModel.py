from app import db

revoked_tokens = db.revoked_tokens


class RevokedTokenModel:
    def __init__(self, jti):
        self.jti = jti

    def save(self):
        res = revoked_tokens.insert_one({'jti': self.jti})
        return res.acknowledged

    @staticmethod
    def is_jti_blacklisted(jti):
        jti = revoked_tokens.find_one({'jti': jti})
        return bool(jti)
