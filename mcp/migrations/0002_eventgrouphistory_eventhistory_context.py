# Generated by Django 4.1.7 on 2023-03-29 01:11

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mcp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventGroupHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startEventCode', models.CharField(max_length=100)),
                ('startEventName', models.CharField(max_length=100)),
                ('startEventTime', models.DateTimeField(auto_now_add=True)),
                ('startContext', djongo.models.fields.JSONField()),
                ('endEventCode', models.CharField(max_length=100)),
                ('endEventName', models.CharField(max_length=100)),
                ('endEventTime', models.DateTimeField(auto_now_add=True)),
                ('endContext', djongo.models.fields.JSONField()),
                ('eqpModuleId', models.IntegerField()),
                ('eqpModuleName', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='eventhistory',
            name='context',
            field=djongo.models.fields.JSONField(),
            preserve_default=False,
        ),
    ]

