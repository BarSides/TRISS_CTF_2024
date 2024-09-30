import os
import random
import shutil
from random import randint
from uuid import uuid4

from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash


from app import User, File, Base

names = tuple({'Trissabella', 'Trissabelle', 'Trissabeth', 'Trissale', 'Trissalee', 'Trissaline', 'Trissalyn', 'Trissamar',
         'Trissan', 'Trissandra', 'Trissanna', 'Trissanne', 'Trissar', 'Trissara', 'Trissea', 'Trissell', 'Trisselle',
         'Trissen', 'Trissenia', 'Trissia', 'Trissianne', 'Trissida', 'Trissiel', 'Trissina', 'Trissine', 'Trissley',
         'Trisslin', 'Trisslyn', 'Trissolee', 'Trisson', 'Trissony', 'Trissora', 'Trisstal', 'Trisstella', 'Trissten',
         'Trisstin', 'Tristana', 'Tristella'})


def init_db():
    pg_host, pg_database = os.getenv("PG_HOST", "localhost"), os.getenv("PG_DATABASE", "database")
    engine = create_engine(f"postgresql://root:c52dd48ffac3436bb4efcfd4ddbd1db0@{pg_host}/{pg_database}")
    Sess = sessionmaker(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    users = [User(username=n,
                  password=generate_password_hash(uuid4().hex if n != 'Trisson' else 'password'))
             for n in names]

    files = []

    flag_username = names[random.randint(0, len(names))]

    with Sess() as session:
        try:
            session.execute(delete(User))
            session.add_all(users)
            session.flush()
            user: User
            for user in users:
                if user.username == flag_username:
                    for n in range(randint(90, 100)):
                        if n == 50:
                            fname = "solveme.py"
                            os.mkdir(f"public/{user.id}/")
                            shutil.copy("./recursive_py/solveme.py", f"public/{user.id}/solveme.py")
                        else:
                            fname = f"{uuid4().hex}.txt"
                        files.append(File(user_id=user.id, filename=fname))
                else:
                    for n in range(randint(90, 100)):
                        files.append(File(user_id=user.id, filename=f"{uuid4().hex}.txt"))
            session.add_all(files)
            session.commit()
        finally:
            session.rollback()


if __name__ == "__main__":
    init_db()
