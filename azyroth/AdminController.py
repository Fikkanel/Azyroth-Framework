# Ganti hanya fungsi index() di dalam AdminController

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

    # --- PERBAIKAN LOGIKA PAGINASI DI SINI ---
    total_items = query.count()
    items = query.limit(per_page).offset((page - 1) * per_page).all()
    
    # Menghitung total halaman untuk ditampilkan di view
    total_pages = (total_items + per_page - 1) // per_page

    return render_template(
        'admin/list.html', 
        items=items,
        # Mengirim data paginasi ke template
        page=page,
        total_pages=total_pages,
        # Sisa variabel tetap sama
        resource_name=self.resource_name,
        endpoint_prefix=self.endpoint_prefix,
        list_display=self.resource.list_display,
        page_title=f"Daftar {self.resource_name.capitalize()}"
    )
