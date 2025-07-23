from flask import render_template, request, redirect, url_for, g, abort

class AdminController:
    """
    Controller generik untuk menangani operasi CRUD untuk resource apa pun.
    """
    def __init__(self, resource_class):
        self.resource = resource_class
        self.model = resource_class.model
        self.resource_name = self.model.__tablename__
        self.endpoint_prefix = f'admin.{self.resource_name}'

    def index(self):
        """Menampilkan halaman daftar (list) untuk sebuah resource."""
        items = g.db_session.query(self.model).all()
        return render_template(
            'admin/list.html', 
            items=items,
            resource_name=self.resource_name,
            endpoint_prefix=self.endpoint_prefix,
            list_display=self.resource.list_display,
            page_title=f"Daftar {self.resource_name.capitalize()}"
        )

    def create(self):
        """Menampilkan form untuk membuat item baru."""
        return render_template(
            'admin/form.html',
            form_schema=self.resource.form_schema,
            resource_name=self.resource_name,
            endpoint_prefix=self.endpoint_prefix,
            page_title=f"Buat {self.resource_name.capitalize()} Baru",
            item=None
        )
    
    def store(self):
        """Menyimpan item baru ke database."""
        item = self.model()
        for field in self.resource.form_schema:
            setattr(item, field['name'], request.form.get(field['name']))
        
        g.db_session.add(item)
        g.db_session.commit()
        return redirect(url_for(f'{self.endpoint_prefix}.index'))

    def edit(self, id):
        """Menampilkan form untuk mengedit item yang ada."""
        item = g.db_session.query(self.model).get(id)
        if not item:
            abort(404)
            
        return render_template(
            'admin/form.html',
            form_schema=self.resource.form_schema,
            item=item,
            resource_name=self.resource_name,
            endpoint_prefix=self.endpoint_prefix,
            page_title=f"Edit {self.resource_name.capitalize()}"
        )

    def update(self, id):
        """Memperbarui item yang ada di database."""
        item = g.db_session.query(self.model).get(id)
        if not item:
            abort(404)
            
        for field in self.resource.form_schema:
            setattr(item, field['name'], request.form.get(field['name']))
            
        g.db_session.commit()
        return redirect(url_for(f'{self.endpoint_prefix}.index'))

    def destroy(self, id):
        """Menghapus item dari database."""
        item = g.db_session.query(self.model).get(id)
        if item:
            g.db_session.delete(item)
            g.db_session.commit()
        return redirect(url_for(f'{self.endpoint_prefix}.index'))
