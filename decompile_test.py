#!/usr/bin/env python
import re

def source_cleanup(source_input):
  def stripcomments(text):
    return re.sub('//.*?\n|/\*.*?\*/', '', text, flags=re.S)

  lines = stripcomments(source_input).split('\n')
  result = [line.strip() for line in lines if line.strip() != ""]
  return "\n".join(result)

def cleanup_test():
  source_input = """
/* VTTTalk Unicode 0x21 (!) */
/* ACT generated Fri Aug 10 10:55:26 2018 */

/* Auto-Hinting Light */

/* ***Settings*** */
/* ModeHinting = LightLatin */
/* ToAnchorBottom = true */


/* CVT 2 16 */
/* CVT 13 19 */
/* Min and Max */
ResYAnchor(13,19)       /* min, CVT */
ResYAnchor(2,16)        /* max, CVT */

/* CVTs - beginning */
/* CVTs - end */


/* YDir: Stroke #0 */
ResYDist(13,7) /*perpendicular to the stroke*/

Smooth()


"""
  cleaned = source_cleanup(source_input)
  assert cleaned == """
ResYAnchor(13,19)
ResYAnchor(2,16)
ResYDist(13,7)
Smooth()
""".strip()

import unittest
from fontTools.ttLib import TTFont
from decompile import (get_glyph_talk,
                       decompile_glyph_bytecode)

#def test_decompiler():
#    from decompile import (get_glyph_talk,
#                           decompile_glyph_bytecode)
#    font = TTFont("data/OpenSans-BoldItalic_VTT.ttf")
#    glyph_order = font.getGlyphOrder()
#    for glyph_name in glyph_order:
#        original_vtt_talk = get_glyph_talk(font, glyph_name)
#        decompiled = decompile_glyph_bytecode(font, glyph_name)
#        assert decompiled == source_cleanup(original_vtt_talk)


class TestPreReqs(unittest.TestCase):
  ...

def create_test(font, glyph_name):
  def do_test_expected(self):
    original_vtt_talk = get_glyph_talk(font, glyph_name)
    decompiled = decompile_glyph_bytecode(font, glyph_name)
    self.assertEqual(decompiled, source_cleanup(original_vtt_talk))
  return do_test_expected

font = TTFont("data/OpenSans-BoldItalic_VTT.ttf")
for glyph_name in font.getGlyphOrder():
  if glyph_name in font["TSI3"].glyphPrograms:
    test_method = create_test(font, glyph_name)
    test_method.__name__ = 'test_decompile_{0}'.format(glyph_name)
    setattr(TestPreReqs, test_method.__name__, test_method)

if __name__ == '__main__':
    unittest.main()
