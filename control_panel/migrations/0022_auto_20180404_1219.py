# Generated by Django 2.0.2 on 2018-04-04 12:19

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('control_panel', '0021_auto_20180403_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='trainer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='groups', to='control_panel.Trainer', verbose_name='Instruktor'),
        ),
        migrations.AlterField(
            model_name='member',
            name='status',
            field=models.SmallIntegerField(choices=[(1, 'Aktywny'), (2, 'Nie  aktywny')], default=2, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='end_date',
            field=models.DateField(verbose_name='Data zakończenia'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='start_date',
            field=models.DateField(default=datetime.date(2018, 4, 4), verbose_name='Data rozpoczęcia'),
        ),
    ]