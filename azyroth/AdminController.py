from flask import render_template, request, redirect, url_for, g, abort, flash
from sqlalchemy import or_

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
        """Menampilkan halaman daftar dengan pencarian dan paginasi manual."""
        page = request.args.get('page', 1, type=int)
        per_page = 10 # Jumlah item per halaman
        search_query = request.args.get('q', '')
        
        query = g.db_session.query(self.model)

        if search_query and hasattr(self.resource, 'searchable_columns'):
            search_filters = []
            for col_name in self.resource.searchable_columns:
                column = getattr(self.model, col_name, None)
                if column:
                    search_filters.append(column.like(f"%{search_query}%"))
            if search_filters:
                query = query.filter(or_(*search_filters))

        # Logika paginasi manual
        total_items = query.count()
        items = query.limit(per_page).offset((page - 1) * per_page).all()
        total_pages = (total_items + per_page - 1) // per_page

        return render_template(
            'admin/list.html', 
            items=items,
            # Mengirim data paginasi ke template
            page=page,
            total_pages=total_pages,
            # Variabel lainnya
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
            item=None,
            page_title=f"Buat {self.resource_name.capitalize()} Baru",
            endpoint_prefix=self.endpoint_prefix
        )
    
    def store(self):
        """Menyimpan item baru ke database."""
        item = self.model()
        for field in self.resource.form_schema:
            setattr(item, field['name'], request.form.get(field['name']))
        
        g.db_session.add(item)
        g.db_session.commit()
        flash(f'{self.model.__name__} berhasil dibuat!', 'success')
        return redirect(url_for(f'{self.endpoint_prefix}_index'))

    def edit(self, id):
        """Menampilkan form untuk mengedit item yang ada."""
        item = g.db_session.query(self.model).get(id)
        if not item: abort(404)
        return render_template(
            'admin/form.html',
            form_schema=self.resource.form_schema,
            item=item,
            page_title=f"Edit {self.resource_name.capitalize()}",
            endpoint_prefix=self.endpoint_prefix
        )

    def update(self, id):
        """Memperbarui item yang ada di database."""
        item = g.db_session.query(self.model).get(id)
        if not item: abort(404)
        
        for field in self.resource.form_schema:
            setattr(item, field['name'], request.form.get(field['name']))
            
        g.db_session.commit()
        flash(f'{self.model.__name__} berhasil diperbarui!', 'success')
        return redirect(url_for(f'{self.endpoint_prefix}_index'))

    def destroy(self, id):
        """Menghapus item dari database."""
        item = g.db_session.query(self.model).get(id)
        if item:
            g.db_session.delete(item)
            g.db_session.commit()
            flash(f'{self.model.__name__} berhasil dihapus!', 'warning')
        return redirect(url_for(f'{self.endpoint_prefix}_index'))
