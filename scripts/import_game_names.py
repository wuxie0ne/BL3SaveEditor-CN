#!/usr/bin/env python3
"""Update name translations from matched English/Chinese Unreal locres pairs.

Pairs must come from the same game resource and version. The script never reads
or modifies a game installation, and leaves curated categories and effects alone.
"""
import argparse
import collections
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'BL3SaveEditor/Localization/zh-CN/GameNames.json'
SOURCES = {
    'travel': ROOT / 'BL3Tools/GameData/Mappings/fast_travel_to_name.json',
    'names': ROOT / 'BL3Tools/GameData/Items/Mappings/part_name_mapping.json',
    'prefixes': ROOT / 'BL3Tools/GameData/Items/Mappings/prefix_name_mapping.json',
}
MAGIC = bytes.fromhex('0e147475674a03fc4a15909dc3377f1b')


def read_locres(path):
    data = path.read_bytes()
    if data[:16] != MAGIC or data[16] not in (1, 2, 3):
        raise ValueError(f'{path}: unsupported locres format')
    version = data[16]

    def integer(offset):
        return struct.unpack_from('<i', data, offset)[0], offset + 4

    def string(offset):
        size, offset = integer(offset)
        if size == 0:
            return '', offset
        length = size if size > 0 else -size * 2
        raw = data[offset:offset + length]
        if len(raw) != length:
            raise ValueError(f'{path}: truncated string')
        value = raw[:-1].decode('utf-8') if size > 0 else raw[:-2].decode('utf-16-le')
        return value, offset + length

    offset = struct.unpack_from('<q', data, 17)[0]
    count, offset = integer(offset)
    strings = []
    for _ in range(count):
        value, offset = string(offset)
        strings.append(value)
        if version >= 2:
            _, offset = integer(offset)

    offset = 25
    if version >= 2:
        _, offset = integer(offset)
    count, offset = integer(offset)
    result = {}
    for _ in range(count):
        if version >= 2:
            _, offset = integer(offset)
        namespace, offset = string(offset)
        key_count, offset = integer(offset)
        for _ in range(key_count):
            if version >= 2:
                _, offset = integer(offset)
            key, offset = string(offset)
            source_hash, offset = integer(offset)
            index, offset = integer(offset)
            result[(namespace, key, source_hash)] = strings[index] if index >= 0 else ''
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pair', nargs=2, type=Path, action='append', required=True,
                        metavar=('EN_LOCRES', 'ZH_LOCRES'))
    parser.add_argument('--output', type=Path, required=True,
                        help='candidate JSON to review before replacing the project table')
    args = parser.parse_args()
    translations = collections.defaultdict(set)
    for en_path, zh_path in args.pair:
        english, chinese = read_locres(en_path), read_locres(zh_path)
        for key in english.keys() & chinese.keys():
            en, zh = english[key], chinese[key]
            if en and zh.strip() and en != zh:
                translations[en].add(zh)
    data = json.loads(OUTPUT.read_text(encoding='utf-8'))
    for section, path in SOURCES.items():
        values = set(json.loads(path.read_text(encoding='utf-8')).values())
        unique = {name: next(iter(translations[name])) for name in sorted(values)
                  if len(translations[name]) == 1}
        ambiguous = sum(len(translations[name]) > 1 for name in values)
        data[section] = unique
        print(f'{section}: {len(unique)} unique, {ambiguous} ambiguous, '
              f'{len(values) - len(unique) - ambiguous} unmatched')
    args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
