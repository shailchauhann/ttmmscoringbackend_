# Generated by Django 4.1.5 on 2023-01-25 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ttmmscoringapi', '0012_startup_isfunded'),
    ]

    operations = [
        migrations.CreateModel(
            name='PortalControl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('control_name', models.CharField(blank=True, max_length=30, null=True)),
                ('control_status', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='startup',
            name='done',
        ),
        migrations.RemoveField(
            model_name='startup',
            name='showinvestor',
        ),
        migrations.RemoveField(
            model_name='startup',
            name='showprogress',
        ),
        migrations.AddField(
            model_name='startup',
            name='bid_overview',
            field=models.TextField(blank=True, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='startup',
            name='current',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
