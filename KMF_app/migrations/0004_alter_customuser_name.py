# Generated by Django 4.2.7 on 2023-11-30 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KMF_app', '0003_alter_customuser_groups_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
