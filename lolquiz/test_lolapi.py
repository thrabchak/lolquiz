import pytest
import json
import test_utils

from lolapi import LolApi
    
class TestLolApi:

  def setup(self):
    self.fs = test_utils.MockFileSystemService()
    self.api = test_utils.MockRiotApiService()
    self.api = LolApi(self.fs, self.api)

  def test_getLocalVersion(self):
    self.fs.valueMap[LolApi.REALM_FILE] = '{"dd":"1"}'
    assert self.api.getLocalVersion() == "1"

  def test_downloadDataFiles(self):
    self.api.downloadDataFiles()
    assert self.fs.valueMap["realm.json"] == test_utils.sanitizeSampleJson(test_utils.SAMPLE_REALM_JSON)
    assert self.fs.valueMap["champion.json"] == test_utils.sanitizeSampleJson(test_utils.SAMPLE_CHAMPION_JSON)
    assert self.fs.valueMap["summoner_spell.json"] == test_utils.sanitizeSampleJson(test_utils.SAMPLE_SUMMONER_SPELL_JSON)

  def test_getSummonerSpells(self):
    self.api.downloadDataFiles()
    spells = self.api.getSummonerSpells()
    assert len(spells) == 1
    assert spells[0].getName() == "Barrier"
    assert spells[0].getCooldownString() == "3 mins 0 secs"

  def test_getChampions(self):
    self.api.downloadDataFiles()
    champs = self.api.getChampions()
    assert len(champs) == 1
    assert champs[0].getName() == "Cho'Gath"

@pytest.mark.skip(reason="File/Web dependencies")
class TestLolApiFullServices:

  def setup(self):
    self.api = LolApi()    

  def test_getServerVersion(self):
    serverVersion = self.api.getServerVersion()
    print(serverVersion)

  def test_downloadDataFiles(self):
    self.api.downloadDataFiles()

  def test_getLocalVersion(self):
    localVersion = self.api.getLocalVersion()
    print(localVersion)

  def test_getSummonerSpells(self):
    spells = self.api.getSummonerSpells()
    print(spells)

    spellNames = []
    for spell in spells:
      spellNames.append(spell.getName())

    assert "Barrier" in spellNames
    assert "Flash" in spellNames
    assert "Teleport" in spellNames
    assert "Mark" not in spellNames
