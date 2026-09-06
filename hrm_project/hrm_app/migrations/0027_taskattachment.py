from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('hrm_app', '0026_taskimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='task_attachments/')),
                ('kind', models.CharField(choices=[('image', 'Image'), ('document', 'Document')], max_length=10)),
                ('explanation', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='hrm_app.task')),
            ],
            options={
                'ordering': ['created_at', 'id'],
            },
        ),
    ]
