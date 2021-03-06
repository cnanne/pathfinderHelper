# Generated by Django 2.2.12 on 2020-07-02 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='hp',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='alignment',
            name='alignment',
            field=models.CharField(choices=[('CE', 'Chaotic Evil'), ('LN', 'Lawful Neutral'), ('NE', 'Neutral Evil'), ('CG', 'Chaotic Good'), ('LG', 'Lawful Good'), ('NG', 'Neutral Good'), ('LE', 'Lawful Evil'), ('CN', 'Chaotic Neutral'), ('NN', 'True Neutral')], max_length=2),
        ),
        migrations.AlterField(
            model_name='wearableitem',
            name='area',
            field=models.CharField(choices=[('NECK', 'Neck'), ('EYE', 'Eye'), ('FEET', 'Feet'), ('TORSO', 'Torso'), ('HEAD', 'Head'), ('LEGS', 'Legs')], max_length=50),
        ),
    ]
