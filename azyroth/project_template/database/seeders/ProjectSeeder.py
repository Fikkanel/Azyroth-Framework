from app.Models.Project import Project
from flask import g

class ProjectSeeder:
    def run(self):
        session = g.db_session
        
        if session.query(Project).count() == 0:
            projects_data = [
                {
                    'title': 'Proyek Portfolio Pertama',
                    'description': 'Deskripsi singkat tentang proyek pertama yang dibuat dengan Azyroth.',
                    'project_link': '#'
                },
                {
                    'title': 'Proyek Klien Kedua',
                    'description': 'Sistem manajemen untuk klien yang dibangun menggunakan Azyroth.',
                    'project_link': '#'
                }
            ]

            for data in projects_data:
                project = Project(**data)
                session.add(project)

            session.commit()
            print("Project seeder has been run.")
