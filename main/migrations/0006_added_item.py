# Generated by Django 3.1.2 on 2020-10-06 02:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_added_topic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('dateAdded', models.DateField(verbose_name='added on date')),
                ('dateUpdated', models.DateField(verbose_name='updated on date')),
                ('topicId', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='items', to='main.topic')),
            ],
            options={
                'db_table': 'item',
            },
        ),
    ]