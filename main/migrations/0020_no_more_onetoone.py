# Generated by Django 3.1.2 on 2020-10-14 03:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_fix_topic_fk_on_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemnote',
            name='referencedTopic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='itemNoteReferencedTopic', to='main.topic'),
        ),
        migrations.AlterField(
            model_name='itempage',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='itemPages', to='main.item'),
        ),
        migrations.AlterField(
            model_name='itempage',
            name='volume',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='volumeItemPages', to='main.volume'),
        ),
        migrations.AlterField(
            model_name='pagemapping',
            name='volume',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='volume_page_mapping', to='main.volume'),
        ),
        migrations.AlterField(
            model_name='topicnote',
            name='referencedTopic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='topicNoteReferencedTopic', to='main.topic'),
        ),
    ]