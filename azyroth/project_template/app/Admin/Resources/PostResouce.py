from app.Models.Post import Post
from app.Models.User import User

class PostResource:
    model = Post
    list_display = ['id', 'title', 'user_id']
    searchable_columns = ['title', 'content']

    form_schema = [
        {'name': 'title', 'type': 'text', 'label': 'Judul Postingan'},
        {'name': 'content', 'type': 'textarea', 'label': 'Isi Konten'},
        {
            'name': 'user_id', 
            'type': 'relationship', 
            'label': 'Penulis',
            'model': User,
            'display_column': 'name'
        },
    ]
