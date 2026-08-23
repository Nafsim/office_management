import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrm_project.settings')
django.setup()

from hrm_app.models import Document

# Update existing documents that don't have document_type set
docs_without_type = Document.objects.filter(document_type__isnull=True) | Document.objects.filter(document_type='')
count = docs_without_type.count()

print(f'Found {count} documents without document_type')

for doc in docs_without_type:
    doc.document_type = 'office'
    doc.save()
    print(f'Updated: {doc.name}')

print('Done!')
