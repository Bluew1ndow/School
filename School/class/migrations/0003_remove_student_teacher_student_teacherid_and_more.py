# Generated by Django 5.0.1 on 2024-01-22 20:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('class', '0002_rename_parent_guardian_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='teacher',
        ),
        migrations.AddField(
            model_name='student',
            name='teacherId',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='class.teacher'),
        ),
        migrations.AlterField(
            model_name='student',
            name='guardianId',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='class.guardian'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='subjectId',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='class.subject'),
        ),
    ]