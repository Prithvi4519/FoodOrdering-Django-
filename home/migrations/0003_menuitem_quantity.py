# Generated by Django 4.1.5 on 2025-02-26 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_menuitem_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
