# Generated by Django 2.0.2 on 2018-03-21 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_panel', '0013_auto_20180321_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='status',
            field=models.SmallIntegerField(choices=[(1, 'Aktywny'), (2, 'Nieaktywny')], default=2, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='status',
            field=models.SmallIntegerField(choices=[(1, 'Opłacony'), (2, 'Do zapłaty')], default=2, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]