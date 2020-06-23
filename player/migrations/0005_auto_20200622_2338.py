# Generated by Django 2.2.12 on 2020-06-22 23:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0004_auto_20200622_2207'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('alignment', models.CharField(choices=[('LN', 'Lawful Neutral'), ('NG', 'Neutral Good'), ('NE', 'Neutral Evil'), ('CE', 'Chaotic Evil'), ('CG', 'Chaotic Good'), ('LG', 'Lawful Good'), ('LE', 'Lawful Evil'), ('CN', 'Chaotic Neutral'), ('NN', 'True Neutral')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True)),
                ('photo', models.ImageField(null=True, upload_to='')),
                ('hitDie', models.CharField(max_length=6)),
                ('ranks', models.IntegerField()),
                ('alignment', models.ManyToManyField(to='player.Alignment')),
                ('classSkills', models.ManyToManyField(blank=True, to='player.Skill')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameField(
            model_name='race',
            old_name='specialAbilities',
            new_name='raceSpecialAbilities',
        ),
        migrations.AddField(
            model_name='effect',
            name='attackBonus',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='effect',
            name='damage',
            field=models.CharField(default='None', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='effect',
            name='extraDamage',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='item',
            name='effects',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='player.Effect'),
        ),
        migrations.AddField(
            model_name='item',
            name='masterwork',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='material',
            field=models.CharField(default='Normal', max_length=100),
        ),
        migrations.AddField(
            model_name='race',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='race',
            name='photo',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='specialabilities',
            name='description',
            field=models.TextField(default=' '),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pc',
            name='race',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='player.SelectedRace'),
        ),
        migrations.AlterField(
            model_name='weapon',
            name='blunt',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='weapon',
            name='pierce',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='weapon',
            name='slash',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='wieldableitem',
            name='area',
            field=models.CharField(choices=[('1H', 'One Handed'), ('2H', 'Two Handed')], max_length=2),
        ),
        migrations.CreateModel(
            name='ClassLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField()),
                ('bab1', models.IntegerField()),
                ('bab2', models.IntegerField()),
                ('bab3', models.IntegerField()),
                ('bab4', models.IntegerField()),
                ('fort', models.IntegerField()),
                ('ref', models.IntegerField()),
                ('will', models.IntegerField()),
                ('gameClass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.Class')),
                ('specialAbilities', models.ManyToManyField(blank=True, null=True, to='player.SpecialAbilities')),
            ],
        ),
        migrations.AddField(
            model_name='pc',
            name='alignment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='player.Alignment'),
        ),
    ]
