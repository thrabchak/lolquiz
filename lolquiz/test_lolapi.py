import pytest
import json
import test_utils

from lolapi import LolApi
    
class TestLolApi:

  def setup(self):
    self.fs = test_utils.MockFileSystemService()
    self.api = test_utils.MockRiotApiService()

  def test_getLocalVersion(self):
    self.fs.valueMap[LolApi.REALM_FILE] = '{"dd":"1"}'
    lolapi = LolApi(self.fs, self.api)
    assert lolapi.getLocalVersion() == "1"

  def test_downloadDataFiles(self):
    lolapi = LolApi(self.fs, self.api)
    lolapi.downloadDataFiles()
    assert self.fs.valueMap["realm.json"] == test_utils.sanitizeSampleJson(test_utils.SAMPLE_REALM_JSON)
    assert self.fs.valueMap["champion.json"] == test_utils.sanitizeSampleJson(test_utils.SAMPLE_CHAMPION_JSON)
    assert self.fs.valueMap["summoner_spell.json"] == test_utils.sanitizeSampleJson(test_utils.SAMPLE_SUMMONER_SPELL_JSON)

  def test_getSummonerSpells(self):
    lolapi = LolApi(self.fs, self.api)
    lolapi.downloadDataFiles()
    spells = lolapi.getSummonerSpells()
    assert len(spells) == 1
    assert spells[0].getName() == "Barrier"
    assert spells[0].getCooldownString() == "3 mins 0 secs"

@pytest.mark.skip(reason="File/Web dependencies")
class TestLolApiFullServices:

  def test_getServerVersion(self):
    lolapi = LolApi()
    serverVersion = lolapi.getServerVersion()
    print(serverVersion)

  def test_downloadDataFiles(self):
    lolapi = LolApi()
    lolapi.downloadDataFiles()

  def test_getLocalVersion(self):
    lolapi = LolApi()
    localVersion = lolapi.getLocalVersion()
    print(localVersion)

  def test_getSummonerSpells(self):
    lolapi = LolApi()
    spells = lolapi.getSummonerSpells()
    print(spells)

    spellNames = []
    for spell in spells:
      spellNames.append(spell.getName())

    assert "Barrier" in spellNames
    assert "Flash" in spellNames
    assert "Teleport" in spellNames
    assert "Mark" not in spellNames
