from player.models import *

def createPlayerPart1(request, pc, createPlayerPart1Form):
    pc.name = createPlayerPart1Form.characterName
    pc.photo = createPlayerPart1Form.photo
    abilities = Abilities()
    abilities.dexterity = createPlayerPart1Form.dex
    abilities.strength = createPlayerPart1Form.str
    abilities.constitution = createPlayerPart1Form.con
    abilities.wisdom = createPlayerPart1Form.wis
    abilities.intelligence = createPlayerPart1Form.int
    abilities.charisma = createPlayerPart1Form.cha
    abilities.name = pc.name
    race = Race.objects.get(name=createPlayerPart1Form.race)
    pc.abilities = abilities
    selectedRace = SelectedRace()
    selectedRace.race = race
    if "half" not in race.name:
        selectedRace.appliedAbilities = race.abilities
    pc.race = race
