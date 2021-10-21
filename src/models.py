from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    last_name = db.Column(db.String(10))
    user_name = db.Column(db.String(30), unique=True)
    #email = db.Column(db.String(80),nullable=False, unique=True)
    #password = db.Column(db.String(80),unique=False, nullable=False)
    favoritos = db.relationship("FavoritoUsuario", backref = "usuario", uselist = True)
    def serialize(self):
        return{
            "user_name": self.user_name,
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name
        }
class FavoritoUsuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(125), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("usuario.id"),nullable=False)
    __table_args__ = (db.UniqueConstraint(
        "user_id",
        "url",
        name = "unico_favorito_para_usuario"
    ),)
    
    def serialize(self):
        return{
            "usuario_id" : self.usuario_id,
            "url": self.url,
            "id" : self.id
        }
    
    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
            return true
        except Exception as error:
            db.session.rollback()
            return False    

    

  
