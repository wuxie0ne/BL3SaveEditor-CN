import json
import unittest
from collections import Counter
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
LOCALIZATION = ROOT / 'BL3SaveEditor/Localization/zh-CN/GameNames.json'


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key: ' + key)
        result[key] = value
    return result


def read_json(path):
    with path.open(encoding='utf-8') as source:
        return json.load(source, object_pairs_hook=unique_object)


class GameNameDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.names = read_json(LOCALIZATION)

    def test_translations_match_existing_source_names(self):
        sources = {
            'travel': 'BL3Tools/GameData/Mappings/fast_travel_to_name.json',
            'names': 'BL3Tools/GameData/Items/Mappings/part_name_mapping.json',
            'prefixes': 'BL3Tools/GameData/Items/Mappings/prefix_name_mapping.json',
        }
        for section, filename in sources.items():
            with self.subTest(section=section):
                source = read_json(ROOT / filename)
                self.assertFalse(set(self.names[section]) - set(source.values()))
                self.assertTrue(all(value.strip() for value in self.names[section].values()))

    def test_effects_have_unambiguous_existing_part_identifiers(self):
        paths = read_json(ROOT / 'BL3Tools/GameData/Items/Mappings/valid_part_database.json')
        short_names = Counter(path.rsplit('.', 1)[-1] for path in paths)
        for identifier, text in self.names['partEffects'].items():
            with self.subTest(identifier=identifier):
                self.assertEqual(short_names[identifier], 1)
                self.assertTrue(identifier.startswith('GPart_'))
                self.assertTrue(text.strip())
                self.assertNotIn('$VALUE$', text)
                self.assertNotIn('[endgame]', text)

    def test_embedded_resource_is_declared(self):
        project = ET.parse(ROOT / 'BL3SaveEditor/BL3SaveEditor.csproj')
        ns = {'m': 'http://schemas.microsoft.com/developer/msbuild/2003'}
        resources = project.findall('.//m:EmbeddedResource', ns)
        matches = [x for x in resources if x.get('Include') == r'Localization\zh-CN\GameNames.json']
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].find('m:LogicalName', ns).text,
                         'BL3SaveEditor.Localization.GameNames.json')


if __name__ == '__main__':
    unittest.main()
