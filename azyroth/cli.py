import os
import shutil
import subprocess
import click
import importlib
import inspect
import multiprocessing
import time

# --- FUNGSI UTAMA DAN GRUP CLI ---

@click.group()
def main_cli():
    """Azyroth Framework Command Line Interface."""
    pass

# --- FUNGSI HELPER ---

def _create_from_template(name, template_path_parts, template_content):
    """Fungsi helper untuk membuat file dari template (misal: controller, model)."""
    file_path = os.path.join(os.getcwd(), *template_path_parts)
    
    if os.path.exists(file_path):
        click.echo(f"Error: File '{os.path.basename(file_path)}' already exists.", err=True)
        return
    
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(template_content)
        click.echo(f"✅ {name} created successfully at: {file_path}")
    except Exception as e:
        click.echo(f"Error creating {name.lower()}: {e}", err=True)

# --- PERINTAH-PERINTAH UTAMA ---

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
        
        env_example_path = os.path.join(dest_dir, '.env.example')
        env_path = os.path.join(dest_dir, '.env')
        if os.path.exists(env_example_path):
            os.rename(env_example_path, env_path)
            click.echo("✅ .env.example renamed to .env")

        if click.confirm("Initialize a new Git repository?", default=True):
            try:
                subprocess.run(["git", "init"], cwd=dest_dir, check=True, capture_output=True)
                click.echo("✅ Git repository initialized.")
            except (subprocess.CalledProcessError, FileNotFoundError):
                click.echo("Warning: 'git init' failed. Is Git installed?", err=True)

        click.echo(f"\n🎉 Project '{project_name}' created successfully!")
        click.echo(f"   Navigate to your project: cd {project_name}")
        click.echo("   Next steps: setup .env, create database, and run 'azyroth db migrate'.")

    except Exception as e:
        click.echo(f"Error creating project: {e}", err=True)

@main_cli.command()
def inspire():
    """Displays an inspiring quote."""
    click.echo("Simplicity is the ultimate sophistication. - Leonardo da Vinci")

# --- FUNGSI UNTUK MENJALANKAN SERVER DAN TUNNEL ---

def _start_flask_server(host, port):
    """Fungsi untuk menjalankan server Flask."""
    try:
        import sys
        sys.path.insert(0, os.getcwd())
        from public.index import app
        app.run(host=host, port=port)
    except ImportError:
        click.echo("Error: Could not find the application. Are you in a project root?", err=True)

def _start_localtunnel(port):
    """Fungsi untuk menjalankan Localtunnel."""
    click.echo("Starting Localtunnel...")
    try:
        lt_process = subprocess.Popen(
            ["lt", "--port", str(port)], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True
        )
        for line in iter(lt_process.stdout.readline, ''):
            if "your url is:" in line:
                public_url = line.split(":")[-1].strip()
                click.echo("✅ Localtunnel established.")
                click.echo(f"   Public URL: {public_url}")
                break
        lt_process.wait()
    except FileNotFoundError:
        click.echo("Error: 'lt' command not found. Please install Localtunnel with 'npm install -g localtunnel'", err=True)
    except Exception as e:
        click.echo(f"An error occurred with Localtunnel: {e}", err=True)

# --- PERINTAH SERVE YANG DIPERBARUI ---

@main_cli.command()
@click.option('--host', default='127.0.0.1', help='The interface to bind to.')
@click.option('--port', default=5000, help='The port to bind to.')
@click.option('--public', is_flag=True, help='Expose the server to the internet using Localtunnel.')
def serve(host, port, public):
    """Runs the Azyroth development server."""
    if not public:
        click.echo(f"🚀 Starting Azyroth server on http://{host}:{port}")
        _start_flask_server(host, port)
        return

    flask_process = multiprocessing.Process(target=_start_flask_server, args=(host, port))
    lt_process = multiprocessing.Process(target=_start_localtunnel, args=(port,))

    try:
        click.echo(f"🚀 Starting Azyroth server on http://{host}:{port}")
        flask_process.start()
        time.sleep(2) 
        lt_process.start()
        flask_process.join()
        lt_process.join()
    except KeyboardInterrupt:
        click.echo("\nStopping servers...")
    finally:
        if flask_process.is_alive():
            flask_process.terminate()
        if lt_process.is_alive():
            lt_process.terminate()
        click.echo("Servers stopped.")

# --- PERINTAH-PERINTAH GENERATOR ---

@main_cli.command("make:controller")
@click.argument('name')
def make_controller(name):
    """Creates a new controller file."""
    class_name = name.capitalize() if name.endswith('Controller') else f"{name.capitalize()}Controller"
    file_name = f"{class_name}.py"
    template = f"""from flask import request, render_template

class {class_name}:
    
    def index(self):
        # Your logic here
        return "Hello from {class_name}!"
"""
    _create_from_template("Controller", ['app', 'Http', 'Controllers', file_name], template)

@main_cli.command("make:model")
@click.argument('name')
def make_model(name):
    """Creates a new SQLAlchemy model file."""
    class_name = name.capitalize()
    file_name = f"{class_name}.py"
    template = f"""from sqlalchemy import Column, Integer, String
from app.Models.User import Base # Ganti 'User' jika Base ada di file lain

class {class_name}(Base):
    __tablename__ = '{class_name.lower()}s'

    id = Column(Integer, primary_key=True)
    # name = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<{class_name}(id={{self.id}})>"
"""
    _create_from_template("Model", ['app', 'Models', file_name], template)

# --- GRUP PERINTAH DATABASE ---
@main_cli.group()
def db():
    """Database related commands (migrate, seed)."""
    pass

def _run_alembic_command(message):
    """Fungsi helper untuk menjalankan perintah alembic."""
    command = ["alembic"]
    if message:
        command.extend(["revision", "--autogenerate", "-m", message])
        click.echo(f"Generating new migration with message: '{message}'")
    else:
        command.extend(["upgrade", "head"])
        click.echo("Running database migrations...")
    
    try:
        subprocess.run(command, check=True)
    except FileNotFoundError:
        click.echo("Error: 'alembic' command not found. Is it installed?", err=True)
    except subprocess.CalledProcessError:
        click.echo(f"Alembic command failed.", err=True)

@db.command("migrate")
@click.option('--message', '-m', help="Message for a new migration file.")
def db_migrate(message):
    """Runs all migrations or creates a new one if a message is provided."""
    _run_alembic_command(message)

@main_cli.command("make:migration")
@click.argument('message')
def make_migration(message):
    """[Alias] Creates a new migration file."""
    _run_alembic_command(message)

@db.command("seed")
@click.option('--class', 'seeder_class', help="The specific seeder class to run.")
def db_seed(seeder_class):
    """Seeds the database with initial data."""
    try:
        import sys
        sys.path.insert(0, os.getcwd())
        from bootstrap.app import create_app
        app = create_app()
        with app.app_context():
            seeder_path = os.path.join(os.getcwd(), 'database', 'seeders')
            if not os.path.exists(seeder_path):
                click.echo("Error: 'database/seeders' directory not found.", err=True)
                return

            if seeder_class:
                module_name = f"database.seeders.{seeder_class}"
                mod = importlib.import_module(module_name)
                seeder = getattr(mod, seeder_class)()
                seeder.run()
                click.echo(f"Seeder '{seeder_class}' completed.")
            else:
                for filename in os.listdir(seeder_path):
                    if filename.endswith('.py') and not filename.startswith('__'):
                        module_name = f"database.seeders.{filename[:-3]}"
                        mod = importlib.import_module(module_name)
                        for name, obj in inspect.getmembers(mod, inspect.isclass):
                            if hasattr(obj, 'run') and name != 'Base':
                                click.echo(f"Running seeder: {name}")
                                seeder = obj()
                                seeder.run()
        click.echo("Database seeding completed.")
    except Exception as e:
        click.echo(f"An error occurred: {e}", err=True)

if __name__ == '__main__':
    main_cli()
