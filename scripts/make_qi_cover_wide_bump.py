# Qi cover with the wide camera bump's cutout (see make_wide_bump.py): same as make_qi_cover.py, plus the stock
# camera opening widened to the wide bump (user 2026-11-25). Writes model/wide-bump/qi-cover-wide-bump.stl (+ step/).
# Run from this folder: freecadcmd -c "exec(open('make_qi_cover_wide_bump.py').read())"
WIDE_BUMP = True
exec(open("make_qi_cover.py").read())
