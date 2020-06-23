# Generated by Django 2.2.12 on 2020-06-23 00:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0009_auto_20200623_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alignment',
            name='alignment',
            field=models.CharField(choices=[('CG', 'Chaotic Good'), ('LG', 'Lawful Good'), ('NN', 'True Neutral'), ('LN', 'Lawful Neutral'), ('LE', 'Lawful Evil'), ('CN', 'Chaotic Neutral'), ('NG', 'Neutral Good'), ('CE', 'Chaotic Evil'), ('NE', 'Neutral Evil')], max_length=2),
        ),
        migrations.AlterField(
            model_name='pc',
            name='race',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='player.SelectedRace'),
        ),
    ]