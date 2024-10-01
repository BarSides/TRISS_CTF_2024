import os
import random
import shutil
from random import randint
from uuid import uuid4

from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash
import argparse

from app import User, File, Base

names = tuple({'Trissabella', 'Trissabelle', 'Trissabeth', 'Trissale', 'Trissalee', 'Trissaline', 'Trissalyn', 'Trissamar',
         'Trissan', 'Trissandra', 'Trissanna', 'Trissanne', 'Trissar', 'Trissara', 'Trissea', 'Trissell', 'Trisselle',
         'Trissen', 'Trissenia', 'Trissia', 'Trissianne', 'Trissida', 'Trissiel', 'Trissina', 'Trissine', 'Trissley',
         'Trisslin', 'Trisslyn', 'Trissolee', 'Trisson', 'Trissony', 'Trissora', 'Trisstal', 'Trisstella', 'Trissten',
         'Trisstin', 'Tristana', 'Tristella', 'Beatriss'})


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("script")
    return parser.parse_args()


def init_db():
    script = args().script

    pg_host, pg_database = os.getenv("PG_HOST", "localhost"), os.getenv("PG_DATABASE", "database")
    engine = create_engine(f"postgresql://root:c52dd48ffac3436bb4efcfd4ddbd1db0@{pg_host}/{pg_database}")
    Sess = sessionmaker(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    login_user = "Beatriss"

    users = [User(username=n,
                  password=generate_password_hash(uuid4().hex if n != login_user else 'Triss2024'))
             for n in names]

    files = []

    while flag_username := names[random.randint(0, len(names))]:
        if flag_username != login_user:
            break

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
                            os.mkdir(f"./public/{user.id}/")
                            shutil.copy(script, f"public/{user.id}/{os.path.basename(script)}")
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
