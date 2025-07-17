import os
import shutil
import click

# Fungsi untuk membuat path absolut di dalam proyek
def make_path(project_root, *args):
    return os.path.join(project_root, *args)

@click.group()
def main_cli():
    """Azyroth Framework Command Line Interface."""
    pass

# ... (kode untuk perintah 'new' dan 'inspire' tetap sama) ...
@main_cli.command()
@click.argument('project_name')
def new(project_name):
    """Creates a new Azyroth project."""
    source_dir = os.path.join(os.path.dirname(__file__), 'project_template')
    dest_dir = os.path.join(os.getcwd(), project_name)

    if os.path.exists(dest_dir):
        click.echo(f"Error: Directory '{project_name}' already exists.", err=True)
        return

    try:
        shutil.copytree(source_dir, dest_dir)
        click.echo(f"✅ Project '{project_name}' created successfully!")
        click.echo(f"Navigate to your project: cd {project_name}")
        click.echo("Then run 'pip install -r requirements.txt' to get started.")
    except Exception as e:
        click.echo(f"Error creating project: {e}", err=True)

@main_cli.command()
def inspire():
    """Displays an inspiring quote."""
    click.echo("Simplicity is the ultimate sophistication. - Leonardo da Vinci")


# -- TAMBAHKAN PERINTAH BARU DI SINI --
@main_cli.command("make:controller")
@click.argument('name')
def make_controller(name):
    """Creates a new controller file."""
    
    # Pastikan nama controller diakhiri dengan 'Controller'
    if not name.endswith('Controller'):
        class_name = f"{name.capitalize()}Controller"
    else:
        class_name = name.capitalize()

    # Tentukan path tempat file akan dibuat
    # Perintah ini harus dijalankan dari root direktori proyek aplikasi
    controller_path = make_path(os.getcwd(), 'app', 'Http', 'Controllers', f"{class_name}.py")

    if os.path.exists(controller_path):
        click.echo(f"Error: Controller '{class_name}' already exists.", err=True)
        return

    # Template dasar untuk file controller
    template = f"""from flask import request, render_template

class {class_name}:
    
    def index(self):
        # Your logic here
        return "Hello from {class_name}!"

    # Tambahkan metode lain sesuai kebutuhan
    # def create(self):
    #     pass
    #
    # def store(self):
    #     pass
    #
    # def show(self, id):
    #     pass
    #
    # def edit(self, id):
    #     pass
    #
    # def update(self, id):
    #     pass
    #
    # def destroy(self, id):
    #     pass
"""
    
    try:
        with open(controller_path, 'w') as f:
            f.write(template)
        click.echo(f"✅ Controller '{class_name}' created successfully at '{controller_path}'")
    except Exception as e:
        click.echo(f"Error creating controller: {e}", err=True)


if __name__ == '__main__':
    main_cli()