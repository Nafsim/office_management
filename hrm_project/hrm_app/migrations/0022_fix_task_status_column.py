from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("hrm_app", "0021_alter_task_color"),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE hrm_app_task DROP COLUMN status;",
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]