import json, pathlib
d = json.load(open('portrait.json'))
A, B = d[0], d[1]

def block(p, sep=None):
    s = []
    s.append('              <g class="fig__field">')
    for a in p['field']: s.append(f'                <path d="{a}" />')
    s.append('              </g>')
    if sep: s.append(f'              <path class="fig__sep" d="{sep}" />')
    for t in p['trajs']: s.append(f'              <path class="fig__line" pathLength="1" d="{t}" />')
    s.append('              <g class="fig__head">')
    for h in p['heads']: s.append(f'                <path d="{h}" />')
    s.append('              </g>')
    s.append('              <g class="fig__start">')
    for c in p['dots']:
        s.append('                ' + c.replace(' class="fig__start"', ''))
    s.append('              </g>')
    return '\n'.join(s)

svg = f'''          <svg class="fig" viewBox="0 0 340 226" role="img" aria-labelledby="fig-title">
            <title id="fig-title">
              Two phase portraits of community assembly. On the left a single attractor, which
              every starting point flows to, so the outcome does not depend on the order the
              members arrive. On the right two attractors on either side of a separatrix running
              through an unstable saddle, so the starting point — that is, the arrival order —
              fixes which of the two the community reaches.
            </title>

            <g>
              <path class="fig__axis" d="M34,28 V148 H154 M34,28 L31.5,32 M34,28 L36.5,32 M154,148 L150,145.5 M154,148 L150,150.5" />
{block(A)}
              <circle class="fig__node fig__node--solid" cx="94" cy="88" r="5.5" />
              <text class="fig__label" x="94" y="170" text-anchor="middle">convergent</text>
              <text class="fig__sublabel" x="94" y="185" text-anchor="middle">one attractor</text>
            </g>

            <g>
              <rect class="fig__basin" x="196" y="30" width="60" height="120" />
              <rect class="fig__basin fig__basin--alt" x="256" y="30" width="60" height="120" />
              <path class="fig__axis" d="M196,28 V148 H316 M196,28 L193.5,32 M196,28 L198.5,32 M316,148 L312,145.5 M316,148 L312,150.5" />
{block(B, sep="M256,28 V148")}
              <circle class="fig__node" cx="256" cy="88" r="4.5" />
              <circle class="fig__node fig__node--solid" cx="220.7" cy="88" r="5.5" />
              <circle class="fig__node fig__node--solid" cx="291.3" cy="88" r="5.5" />
              <text class="fig__label" x="256" y="170" text-anchor="middle">contingent</text>
              <text class="fig__sublabel" x="256" y="185" text-anchor="middle">two attractors, one saddle</text>
            </g>

            <text class="fig__sublabel" x="170" y="210" text-anchor="middle">community composition, two of many axes</text>
          </svg>
'''
p = pathlib.Path('/Users/scorrea/Documents/correagallego.com/src/pages/index.astro')
s = p.read_text()
start = s.index('          <svg class="fig"')
end = s.index('</svg>', start) + len('</svg>\n')
s = s[:start] + svg + s[end:]

CAP_OLD_START = s.index('          <figcaption class="fig__caption">')
CAP_OLD_END = s.index('</figcaption>', CAP_OLD_START) + len('</figcaption>')
CAP = '''          <figcaption class="fig__caption">
            Trajectories in community state space, each starting from a different arrival order
            (dots); arrows give the direction of flow. Left, one attractor, reached from every
            start. Right, two attractors either side of a separatrix (dashed) through an unstable
            saddle (open circle): where the community starts fixes which one it reaches.
            Schematic; the axes are two of many.
          </figcaption>'''
s = s[:CAP_OLD_START] + CAP + s[CAP_OLD_END:]
p.write_text(s)
print('figure + caption installed')
