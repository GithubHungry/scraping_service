# Generated by Django 3.0.7 on 2020-06-10 16:08

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0002_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', jsonfield.fields.JSONField(default=dict)),
                ('timestamp', models.DateField(auto_now_add=True)),
            ],
        ),
    ]