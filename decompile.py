from parser import AssemblyParser, ParseException

from fontTools.ttLib import (TTFont, TTLibError)
from fontTools.ttLib.tables.ttProgram import Program
#from fontTools.ttLib.tables._g_l_y_f import (
#    USE_MY_METRICS, ROUND_XY_TO_GRID, UNSCALED_COMPONENT_OFFSET,
#    SCALED_COMPONENT_OFFSET,
#)

#VTT_TABLES = ["TSI0", "TSI1", "TSI2", "TSI3", "TSI5"]


class VTTLibError(TTLibError):
    pass


def tokenize(data, parseAll=True):
    return AssemblyParser.parseString(data, parseAll=parseAll)

def get_glyph_assembly(font, name):
    return get_vtt_program(font, name, is_glyph=True)


def get_glyph_talk(font, name):
    return get_vtt_program(font, name, is_talk=True, is_glyph=True)


def get_vtt_program(font, name, is_talk=False, is_glyph=False):
    tag = "TSI3" if is_talk else "TSI1"
    if tag not in font:
        raise VTTLibError("%s table not found" % tag)
    try:
        if is_glyph:
            data = font[tag].glyphPrograms[name]
        else:
            data = font[tag].extraPrograms[name]
    except KeyError:
        raise KeyError(
            "%s program missing from %s: '%s'" % (
                "Glyph" if is_glyph else "Extra", tag, name))
    return data.replace("\r", "\n")

AXIS_NAME = {
  '0': "Y",
  '1': "X"
}

REF_POINT = {
  '0': "2",
  '1': "1"
}

def pattern_match_vtttalk(tokens):
  vttalk = []
  axis = "X"
  refPt = {"1": None, "2": None}
  IP = 0
  while IP < len(tokens):
    cmd = tokens[IP]
    IP += 1
    mnemonic = cmd[0]
    operands = cmd[1:]
    if mnemonic == "SVTCA":
      axis = AXIS_NAME[operands[0]]

    elif mnemonic == "CALL" and len(operands) == 3 and operands[2] == 114:
      a, b, _ = operands
      vttalk.append('Res{}Anchor({},{})'.format(axis, a, b))
      # side-effect:
      refPt["2"] = a

    elif mnemonic == "SHP" and len(operands) == 2:
      refpt_id, pt = operands
      vttalk.append('{}Shift({},{})'.format(axis, refPt[REF_POINT[refpt_id]], pt))

    elif mnemonic == "SRP1" and len(operands) == 1:
      refPt["1"] = operands[0]

    elif mnemonic == "SRP2" and len(operands) == 1:
      refPt["2"] = operands[0]

    elif mnemonic == "IUP" and operands[0] == '0' and tokens[IP][0] == "IUP" and tokens[IP][1] == '1':
        vttalk.append('Smooth()')
        IP += 1

    else:
      vttalk.append('ASM("{} {}")'.format(mnemonic, " ".join(map(str, operands))))

  return "\n".join(vttalk)

def decompile_instructions(font):
    if "glyf" not in font:
        raise VTTLibError("Missing 'glyf' table; not a TrueType font")

    glyph_order = font.getGlyphOrder()
    glyf_table = font['glyf']
    for glyph_name in glyph_order:
        if glyph_name == "X":
            data = get_glyph_assembly(font, glyph_name)
            data = data.strip()
            tokens = tokenize(data)
            vtttalk = pattern_match_vtttalk(tokens)
            print("== {} ==\n{}\n".format(glyph_name, data))
            # print("== TOKENS ==\n{}\n".format("\n".join(map(str, tokens))))
            print("== VTT Talk ==\n{}\n".format(vtttalk))

def vtt_decompile(infile, outfile):
    font = TTFont(infile)

    decompile_instructions(font)
    #font.save(outfile)

import sys
if len(sys.argv) != 2:
  sys.exit("usage: {} infile.ttf".format(sys.argv[0]))

infile = sys.argv[1]
outfile = sys.argv[1] + ".out"
vtt_decompile(infile, outfile)
print ("done")
