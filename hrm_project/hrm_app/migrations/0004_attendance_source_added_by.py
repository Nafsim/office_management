from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrm_app', '0003_payrolladjustment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='source',
            field=models.CharField(choices=[('web', 'Web'), ('manual', 'Manual'), ('sync', 'Sync')], default='web', max_length=10),
        ),
        migrations.AddField(
            model_name='attendance',
            name='added_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attendance_added', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late'), ('Half Day', 'Half Day'), ('Holiday', 'Holiday'), ('Leave', 'Leave')], default='Present', max_length=20),
        ),
    ]
