# Generated by Django 4.2.9 on 2024-05-01 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_country_alter_company_creator_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='origin_country',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.PROTECT, to='home.country'),
        ),
    ]
