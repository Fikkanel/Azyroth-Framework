import os
import shutil
import subprocess
import click
import importlib
import inspect

# --- FUNGSI UTAMA CLI ---

@click.group()
def main_cli():
    """Azyroth Framework Command Line Interface."""
    pass

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

        if click.confirm("Do you want to initialize a new Git repository?", default=True):
            try:
                subprocess.run(["git", "init"], cwd=dest_dir, check=True, capture_output=True)
                click.echo("✅ Git repository initialized.")
            except (subprocess.CalledProcessError, FileNotFoundError):
                click.echo("Warning: 'git init' failed. Is Git installed and in your PATH?", err=True)

        click.echo(f"\n🎉 Project '{project_name}' created successfully!")
        click.echo(f"   Navigate to your project: cd {project_name}")
        click.echo("   Next steps: setup your .env file, create a database, and run 'azyroth db migrate'.")

    except Exception as e:
        click.echo(f"Error creating project: {e}", err=True)

@main_cli.command()
def inspire():
    """Displays an inspiring quote."""
    click.echo("Simplicity is the ultimate sophistication. - Leonardo da Vinci")

# --- PERINTAH-PERINTAH GENERATOR ---

@main_cli.command("make:controller")
@click.argument('name')
def make_controller(name):
    """Creates a new controller file."""
    if not name.endswith('Controller'):
        class_name = f"{name.capitalize()}Controller"
    else:
        class_name = name.capitalize()

    controller_path = os.path.join(os.getcwd(), 'app', 'Http', 'Controllers', f"{class_name}.py")

    if os.path.exists(controller_path):
        click.echo(f"Error: Controller '{class_name}' already exists.", err=True)
        return

    template = f"""from flask import request, render_template

class {class_name}:
    
    def index(self):
        # Your logic here
        return "Hello from {class_name}!"
"""
    
    try:
        with open(controller_path, 'w') as f:
            f.write(template)
        click.echo(f"✅ Controller '{class_name}' created successfully.")
    except Exception as e:
        click.echo(f"Error creating controller: {e}", err=True)

# --- GRUP PERINTAH DATABASE ---

@main_cli.group()
def db():
    """Database related commands (migrate, seed)."""
    pass

def _run_alembic_command(message, is_migration):
    """Fungsi helper untuk menjalankan perintah alembic."""
    command = ["alembic"]
    if is_migration:
        command.extend(["revision", "--autogenerate", "-m", message])
        click.echo(f"Generating new migration with message: {message}")
    else:
        command.extend(["upgrade", "head"])
        click.echo("Running database migrations...")
    
    try:
        subprocess.run(command, check=True)
    except FileNotFoundError:
        click.echo("Error: 'alembic' command not found. Is it installed in your venv?", err=True)
    except subprocess.CalledProcessError:
        click.echo(f"Alembic command failed. See error output above.", err=True)

@db.command("migrate")
@click.option('--message', '-m', help="Revision message for a new migration file.")
def db_migrate(message):
    """Runs database migrations or generates a new migration file."""
    _run_alembic_command(message, is_migration=bool(message))

# --- PERBAIKAN: Tambahkan alias 'make:migration' ---
@main_cli.command("make:migration")
@click.argument('message')
def make_migration(message):
    """[Alias] Creates a new migration file."""
    _run_alembic_command(message, is_migration=True)


@db.command("seed")
@click.option('--class', 'seeder_class', help="The specific seeder class to run.")
def db_seed(seeder_class):
    """Seeds the database with initial data from seeder files."""
    try:
        # Menambahkan path proyek saat ini agar import bootstrap berhasil
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
    except ImportError as e:
        click.echo(f"Import Error: {e}. Make sure you are in an Azyroth project root and venv is active.", err=True)
    except Exception as e:
        click.echo(f"An error occurred: {e}", err=True)

if __name__ == '__main__':
    main_cli()
