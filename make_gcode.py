#!/usr/bin/env python3
"""Creates a test.nc (test rectangle) file from a test.yaml config."""

from typing import Any

import __main__
import os
import pathlib
import sys
import yaml

class Error(Exception):
  pass

class ConfigKeyNotFoundError(Error):
  pass

class MissingKeyError(Error):
  pass

class TemplatePathNotFoundError(Error):
  pass

class UnexpectedConfigTypeError(Error):
  pass

class UnexpectedUnitsError(Error):
  pass

class YamlConfigDoesNotExistError(Error):
  pass

class YamlParseError(Error):
  pass


class Config:
  def __init__(self, yaml_path: pathlib.Path):
    'Makes a test box file.'
    if not yaml_path.exists():
      raise YamlConfigDoesNotExistError(
          '%s does not exist' % yaml_path)

    try:
      with yaml_path.open() as fin:
        self.data = yaml.safe_load(fin)
    except yaml.scanner.ScannerError as e:
      raise YamlParseError(e) from e

    for key, value in self.data.items():
      if isinstance(value, int):
        self.data[key] = float(value)

  def get(self, key: str, expected_type: Any) -> Any:
    """Gets a config value."""
    if key not in self.data:
      raise ConfigKeyNotFoundError(
          'Could not find needed config key: %s' % key)

    val = self.data[key]
    if not isinstance(val, expected_type):
      raise UnexpectedConfigTypeError(
          'Unexpected type for %s.  Excpeted a %s found a %s' % (
            key, expected_type, type(val)))

    return val


def make_test_box(yaml_path: pathlib.Path) -> None:
  'Main logic.'
  cfg = Config(yaml_path)
  template_path = pathlib.Path(cfg.get('template_path', str))
  units = cfg.get('units', str)
  if units == 'mm':
    cfg.data['unit_code'] = '21'
  elif units == 'inches':
    cfg.data['unit_code'] = '20'
  else:
    raise UnexpectedUnitsError('Unexpected units: %s.  Expected mm or inches' % units)

  if not template_path.exists():
    template_path = pathlib.Path(os.path.join(os.path.dirname(__main__.__file__), template_path))

  if not template_path.exists():
    raise TemplatePathNotFoundError('Did not find template path: %s' % template_path)

  template = template_path.read_text()
  try:
    output = template.format(**cfg.data)
  except KeyError as e:
    raise MissingKeyError('Missing template key: %s' % e) from e

  output_path = cfg.get('output_path', str)
  with open(output_path, 'w') as fout:
    fout.write(output)

  print('Wrote %s' % output_path)

def main():
  'Main entry point.'
  if len(sys.argv) != 2:
    sys.exit('Usage ./make_test_box.py test.yaml')

  try:
    make_test_box(pathlib.Path(sys.argv[1]))
  except Error as e:
    sys.exit(e)

if __name__ == '__main__':
  main()
