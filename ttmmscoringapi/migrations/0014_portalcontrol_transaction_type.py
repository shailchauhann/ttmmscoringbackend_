# Generated by Django 4.1.5 on 2023-01-25 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ttmmscoringapi', '0013_portalcontrol_remove_startup_done_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='portalcontrol',
            name='transaction_type',
            field=models.CharField(blank=True, choices=[('beforebidding', '0'), ('bidding', '1'), ('afterbidding', '2')], max_length=20, null=True),
        ),
    ]
