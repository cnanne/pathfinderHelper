# Generated by Django 2.2.12 on 2020-07-07 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0005_auto_20200706_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='hasBloodlines',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='class',
            name='hasDomains',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='class',
            name='hasSchools',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='spelllevel',
            name='classes',
            field=models.ManyToManyField(blank=True, default=None, to='player.Class'),
        ),
        migrations.AlterField(
            model_name='alignment',
            name='alignment',
            field=models.CharField(choices=[('NG', 'Neutral Good'), ('LG', 'Lawful Good'), ('CN', 'Chaotic Neutral'), ('NN', 'True Neutral'), ('LN', 'Lawful Neutral'), ('LE', 'Lawful Evil'), ('CG', 'Chaotic Good'), ('CE', 'Chaotic Evil'), ('NE', 'Neutral Evil')], max_length=2),
        ),
        migrations.AlterField(
            model_name='wearableitem',
            name='area',
            field=models.CharField(choices=[('HEAD', 'Head'), ('EYE', 'Eye'), ('FEET', 'Feet'), ('LEGS', 'Legs'), ('TORSO', 'Torso'), ('NECK', 'Neck')], max_length=50),
        ),
    ]
