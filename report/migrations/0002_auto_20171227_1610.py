# Generated by Django 2.0 on 2017-12-27 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appdaily',
            name='bugid',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='appdaily',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='appdaily',
            name='describe',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='appdaily',
            name='person',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='appdaily',
            name='priority',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='appdaily',
            name='project',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='appdaily',
            name='remake',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='appdaily',
            name='reopen',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='appdaily',
            name='reopen_reason',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='appdaily',
            name='solution',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='appdaily',
            name='solution_reason',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='appdaily',
            name='work_type',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
