from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrm_app', '0025_alter_payrolladjustment_adjustment_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='task_images/')),
                ('explanation', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='hrm_app.task')),
            ],
            options={
                'ordering': ['created_at', 'id'],
            },
        ),
    ]