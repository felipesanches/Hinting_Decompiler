## Hinting Decompiler

This code re-uses the parser developed by Dalton Maag's vttLib.
We could at some point in the future submit the VTT decompilation routines as a pull request to the vttLib project, but for now I'll continue working for a while in this repo as an experimental project.

This is a decompiler that regenerates VTT Talk high-level script based on the low-level hinting bytecode in a font file. I'd love to make it generate VTT Talk from ttfautohint output, but that's a more challenging goal that I am not really sure we can easily achieve. Anyway... this is the result of a quick one day sprint, so it surely can improve. Feel free to send pull request.

The code is licensed under the MIT license just like the Dalton Maag's upstream project.

Happy Hacking,
Felipe "juca" Sanches
