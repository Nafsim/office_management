import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrm_project.settings')
django.setup()

from hrm_app.models import Document

# Check all documents and their types
docs = Document.objects.all()
print(f'Total documents: {docs.count()}')
print('\nDocument types:')
for doc_type in ['office', 'employee', 'generated', 'request']:
    count = docs.filter(document_type=doc_type).count()
    print(f'  {doc_type}: {count}')

print('\nAll documents:')
for doc in docs:
    print(f'  {doc.name} - type: {doc.document_type}')
