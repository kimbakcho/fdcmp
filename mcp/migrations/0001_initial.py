# Generated by Django 4.1.7 on 2023-03-28 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EventHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventCode', models.CharField(max_length=100)),
                ('eventName', models.CharField(max_length=100)),
                ('updateTime', models.DateTimeField(auto_now_add=True)),
                ('eqpId', models.IntegerField()),
                ('eqpCode', models.CharField(max_length=100)),
                ('eqpName', models.CharField(max_length=100)),
                ('eqpModuleId', models.IntegerField()),
                ('eqpModuleName', models.CharField(max_length=100)),
            ],
        ),
    ]

    def apply(self, project_state, schema_editor, collect_sql=False):

        return super().apply(project_state, schema_editor, collect_sql)

