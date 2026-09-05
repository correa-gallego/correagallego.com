// V(x) = x^4 + a*x^2 — the canonical bistability normal form.
// a > 0 -> one basin (x=0) ; a < 0 -> two basins (x = +/- sqrt(-a/2))
const V  = (x, a) => x**4 + a*x**2;
const dV = (x, a) => 4*x**3 + 2*a*x;

const XMAX = 1.75, N = 76, TOP = 26, BOT = 104;

function panel(a, left, width) {
  const xs = Array.from({length: N+1}, (_, i) => -XMAX + (2*XMAX*i)/N);
  const vs = xs.map(x => V(x, a));
  const lo = Math.min(...vs), hi = Math.max(...vs);
  const sx = x => left + ((x + XMAX)/(2*XMAX))*width;
  const sy = v => BOT - ((v - lo)/(hi - lo))*(BOT - TOP);
  const d = xs.map((x,i) => `${i?'L':'M'}${sx(x).toFixed(1)},${sy(vs[i]).toFixed(1)}`).join(' ');
  const mins = [];
  for (let i = 1; i <= N; i++) {
    if (dV(xs[i-1],a) < 0 && dV(xs[i],a) >= 0) {
      let lo2 = xs[i-1], hi2 = xs[i];
      for (let k = 0; k < 80; k++) { const m = (lo2+hi2)/2; if (dV(m,a) < 0) lo2 = m; else hi2 = m; }
      const x0 = (lo2+hi2)/2;
      mins.push({ x:+x0.toFixed(4), cx:+sx(x0).toFixed(1), curveY:+sy(V(x0,a)).toFixed(1) });
    }
  }
  return { d, mins };
}

for (const [name, a, left] of [['A  a=+1.0  one basin', 1.0, 18], ['B  a=-2.0  two basins', -2.0, 182]]) {
  const p = panel(a, left, 140);
  console.log('=== ' + name + ' ===');
  console.log(p.d);
  console.log('minima -> ' + JSON.stringify(p.mins));
  console.log('');
}
