# -*- coding: utf-8 -*-
"""This file contains the Spotlight searched terms plugin in Plaso."""

from plaso.events import plist_event
from plaso.parsers import plist
from plaso.parsers.plist_plugins import interface


__author__ = 'Joaquin Moreno Garijo (Joaquin.MorenoGarijo.2013@live.rhul.ac.uk)'


class SpotlightPlugin(interface.PlistPlugin):
  """Basic plugin to extract Spotlight."""

  NAME = 'plist_spotlight'
  DESCRIPTION = u'Parser for Spotlight plist files.'

  PLIST_PATH = 'com.apple.spotlight.plist'
  PLIST_KEYS = frozenset(['UserShortcuts'])

  # Generated events:
  # name of the item: searched term.
  #   PATH: path of the program associated to the term.
  #   LAST_USED: last time when it was executed.
  #   DISPLAY_NAME: the display name of the program associated.

  def GetEntries(self, parser_mediator, match=None, **unused_kwargs):
    """Extracts relevant Spotlight entries.

    Args:
      parser_mediator: A parser mediator object (instance of ParserMediator).
      match: Optional dictionary containing keys extracted from PLIST_KEYS.
             The default is None.
    """
    for search_text, data in match['UserShortcuts'].iteritems():
      description = (
          u'Spotlight term searched "{0:s}" associate to {1:s} '
          u'({2:s})').format(search_text, data['DISPLAY_NAME'], data['PATH'])
      event_object = plist_event.PlistEvent(
          u'/UserShortcuts', search_text, data['LAST_USED'], description)
      parser_mediator.ProduceEvent(event_object)


plist.PlistParser.RegisterPlugin(SpotlightPlugin)
