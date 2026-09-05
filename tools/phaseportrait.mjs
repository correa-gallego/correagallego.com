// Phase portraits of  dx/dt = mu*x - x^3 ,  dy/dt = -y
//   mu < 0 : one stable node at the origin        (assembly converges)
//   mu > 0 : stable nodes at (+/-sqrt(mu), 0), saddle at origin,
//            separatrix x = 0                     (arrival order decides)
// Same family, one parameter — as in the landscape figure it replaces.
// y relaxes more slowly than x, so trajectories sweep along the slow manifold
// instead of running straight at the attractor.
const f = (x, y, mu) => [mu*x - x**3, -0.3*y];

const D = 1.7;                                   // domain half-width
const BOX = 120, TOP = 28;                       // plot box in SVG units
const panels = [{ mu: -0.8, left: 34 }, { mu: 1.0, left: 196 }];
const sx = (x, left) => left + ((x + D)/(2*D))*BOX;
const sy = y => TOP + ((D - y)/(2*D))*BOX;
const r1 = n => Math.round(n*10)/10;

function rk4(x, y, mu, h) {
  const [a1,b1] = f(x, y, mu);
  const [a2,b2] = f(x + h*a1/2, y + h*b1/2, mu);
  const [a3,b3] = f(x + h*a2/2, y + h*b2/2, mu);
  const [a4,b4] = f(x + h*a3,   y + h*b3,   mu);
  return [x + h*(a1+2*a2+2*a3+a4)/6, y + h*(b1+2*b2+2*b3+b4)/6];
}

function trajectory(x0, y0, mu) {
  const pts = [[x0, y0]];
  let x = x0, y = y0;
  for (let i = 0; i < 1600; i++) {
    [x, y] = rk4(x, y, mu, 0.02);
    if (Math.abs(x) > D*1.2 || Math.abs(y) > D*1.2) break;
    if (i % 9 === 0) pts.push([x, y]);
    const [dx, dy] = f(x, y, mu);
    if (Math.hypot(dx, dy) < 0.012) break;            // settled on an attractor
  }
  return pts;
}

// evenly spaced starting points around the perimeter of the domain
const starts = (mu) => {
  const s = [];
  for (let k = 0; k < 10; k++) {
    const t = (k + 0.5)/10 * 2*Math.PI;
    let x = 1.42*Math.cos(t), y = 1.42*Math.sin(t);
    if (Math.abs(x) < 0.12) x += x >= 0 ? 0.18 : -0.18;   // never start on the separatrix
    s.push([x, y]);
  }
  return s;
};

function arrowAt(pts, frac, left) {
  const i = Math.max(1, Math.min(pts.length - 1, Math.round(pts.length*frac)));
  const [x1,y1] = pts[i-1], [x2,y2] = pts[i];
  const px = sx(x2,left), py = sy(y2);
  const ang = Math.atan2(sy(y2)-sy(y1), sx(x2,left)-sx(x1,left));
  const L = 4.6, W = 0.42;
  const p = (a) => `${r1(px - L*Math.cos(ang+a))},${r1(py - L*Math.sin(ang+a))}`;
  return `M${p(-W)} L${r1(px)},${r1(py)} L${p(W)}`;
}

let out = [];
for (const { mu, left } of panels) {
  // vector field on a 5x5 grid
  const field = [];
  for (let i = 0; i < 5; i++) for (let j = 0; j < 5; j++) {
    const x = -1.28 + i*0.64, y = -1.28 + j*0.64;
    const [dx, dy] = f(x, y, mu);
    const m = Math.hypot(dx, dy); if (m < 1e-6) continue;
    const ux = dx/m, uy = dy/m, L = 0.19;
    const ax = sx(x - ux*L, left), ay = sy(y - uy*L);
    const bx = sx(x + ux*L, left), by = sy(y + uy*L);
    const ang = Math.atan2(by-ay, bx-ax), H = 2.6, W = 0.5;
    field.push(`M${r1(ax)},${r1(ay)} L${r1(bx)},${r1(by)}` +
      ` M${r1(bx - H*Math.cos(ang-W))},${r1(by - H*Math.sin(ang-W))} L${r1(bx)},${r1(by)}` +
      ` L${r1(bx - H*Math.cos(ang+W))},${r1(by - H*Math.sin(ang+W))}`);
  }
  const trajs = [], heads = [], dots = [];
  for (const [x0, y0] of starts(mu)) {
    const p = trajectory(x0, y0, mu);
    if (p.length < 4) continue;
    trajs.push('M' + p.map(([x,y]) => `${r1(sx(x,left))},${r1(sy(y))}`).join(' L'));
    heads.push(arrowAt(p, 0.34, left));
    dots.push(`<circle class="fig__start" cx="${r1(sx(x0,left))}" cy="${r1(sy(y0))}" r="1.9" />`);
  }
  out.push({ mu, left, field, trajs, heads, dots });
}
console.log(JSON.stringify(out.map(o => ({
  mu:o.mu, left:o.left, nField:o.field.length, nTraj:o.trajs.length,
  field:o.field, trajs:o.trajs, heads:o.heads, dots:o.dots
})), null, 0));
