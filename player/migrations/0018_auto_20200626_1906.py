# Generated by Django 2.2.12 on 2020-06-26 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0017_auto_20200626_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alignment',
            name='alignment',
            field=models.CharField(choices=[('CE', 'Chaotic Evil'), ('LN', 'Lawful Neutral'), ('NG', 'Neutral Good'), ('LG', 'Lawful Good'), ('LE', 'Lawful Evil'), ('CG', 'Chaotic Good'), ('NE', 'Neutral Evil'), ('CN', 'Chaotic Neutral'), ('NN', 'True Neutral')], max_length=2),
        ),
        migrations.AlterField(
            model_name='pc',
            name='race',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='player.SelectedRace'),
        ),
        migrations.AlterField(
            model_name='wearableitem',
            name='area',
            field=models.CharField(choices=[('NECK', 'Neck'), ('EYE', 'Eye'), ('HEAD', 'Head'), ('TORSO', 'Torso'), ('FEET', 'Feet'), ('LEGS', 'Legs')], max_length=50),
        ),
        migrations.AlterField(
            model_name='wieldableitem',
            name='area',
            field=models.CharField(choices=[('1H', 'One Handed'), ('2H', 'Two Handed')], max_length=2),
        ),
    ]