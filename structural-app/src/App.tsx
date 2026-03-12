
import React, { useState, useEffect } from 'react';

const App: React.FC = () => {
  // --- STATE FOR INPUTS (Exact default values from HTML) ---
  const [inputs, setInputs] = useState({
    L1: 3.96, L2: 6.75, L3: 4.56, L4: 4.20,
    pisos: 2, He: 3.40, uso: 'Vivienda',
    Cm: 0.7028, Cv: 0.20,
    zonaS: 'Alta', fc: 210, fy: 4200,
    b: 30, rec: 2.5, hdef: 33,
    fi_neg: 16, fi_pos: 16, fi_est: 10, bcol: 30
  });

  const [res, setRes] = useState<any>(null);

  // --- REACTION ENGINE (Exact formulas from original HTML script) ---
  useEffect(() => {
    const { L1, L2, L3, L4, Cm, Cv, fc, fy, b, rec, hdef, fi_neg, fi_pos, fi_est, bcol, zonaS } = inputs;

    const Lv = Math.max(L1, L2, L3, L4);
    const Lt = (L3 + L4) / 2;
    const Cu = 1.2 * Cm + 1.6 * Cv;
    const Mdis = Cu * Lt * Math.pow(Lv - 0.3, 2) / 8 * 0.65 * 0.85 * 1.1;
    const hmin = Math.ceil(Math.pow(Mdis * 100000 / 0.145 / fc / b, 0.5) + rec);
    const h = hdef;
    const rel = h / b;
    const relOK = rel >= 1.1 && rel <= 1.6;
    const d = h - rec - fi_est / 10 - fi_neg / 20;
    const dp = h - d;
    const Asmin = 14 * b * d / fy;
    const pb = 0.85 * 0.85 * fc / fy * (6100 / (6100 + fy));
    const pmax = (zonaS === 'Alta') ? 0.5 * pb : 0.75 * pb;

    // Negativo
    const Ab_neg = 0.785 * Math.pow(fi_neg / 10, 2);
    const Asreq_neg = 30 * Mdis / d;
    const num_neg_base = Math.max(Math.floor(Asmin / Ab_neg), 2);
    const num_neg_adic = Math.floor((Asreq_neg - num_neg_base * Ab_neg) / Ab_neg) + 1;
    const num_neg = num_neg_base + num_neg_adic;
    const Astot_neg = num_neg * Ab_neg;
    const cuant_neg = Astot_neg / (b * h);
    const sep_neg = (b - 2 * rec - 2 - num_neg * fi_neg / 10) / (num_neg - 1);
    const sepOK_neg = sep_neg > Math.max(fi_neg / 10, 2.54);
    const a = Astot_neg * fy / (0.85 * fc * b);
    const Mres = 0.9 * (Astot_neg * fy * (d - a / 2)) / 100000;
    const DC = Mdis / Mres;

    // Positivo
    const Ab_pos = 0.785 * Math.pow(fi_pos / 10, 2);
    const Asreq_pos = 0.67 * Astot_neg;
    const num_pos = Math.floor(Asreq_pos / Ab_pos);
    const Astot_pos = num_pos * Ab_pos;
    const cuant_pos = Astot_pos / (b * h);
    const cuantOK_pos = cuant_pos <= pmax && cuant_pos >= (Asmin / (b * h));
    const Mpr_neg = 1.25 * Astot_neg * fy * (d - 1.25 * Astot_neg * fy / 1.7 / fc / b) / 100000;
    const Mpr_pos = 1.25 * Astot_pos * fy * (d - 1.25 * Astot_pos * fy / 1.7 / fc / b) / 100000;

    // Cortante
    const Vug = (2 * Lv - Lt) * Lt * Cu / 4;
    const Vum = (Mpr_neg + Mpr_pos) / (Lv - bcol / 100 - fi_est / 25);
    const Vu = Vug + Vum;
    const Vc = 0.53 * Math.sqrt(fc) * b * d / 1000;
    const Vs = (Vu - 0.75 * Vc) / 0.75;
    const Ab_est = 0.7854 * Math.pow(fi_est / 10, 2);
    const s_calc = b * Ab_est * 2 * fy / Vs / 1000;
    const smax_prot = Math.ceil(Math.min(d / 4, 6 * fi_neg / 10, 10, s_calc));
    const Zprot = 2 * h;
    const Zcentral = (Lv - bcol / 100 - Zprot / 50) * 100;
    const smax_cent = Math.ceil(Math.min(d / 2, 8 * fi_neg / 10, 15));
    const s_adopt_prot = Math.min(s_calc, smax_prot);
    const s_adopt_cent = Math.min(s_calc, smax_cent);
    const Lmax_voladizo = Math.pow(2 * Mres / Cu, 0.333);

    setRes({
      Lv, Lt, Cu, Mdis, hmin, h, rel, relOK, d, dp, Asmin, pb, pmax, DC,
      Ab_neg, Asreq_neg, num_neg, num_neg_base, num_neg_adic, Astot_neg, cuant_neg, sep_neg, sepOK_neg, Mres, Mpr_neg,
      Ab_pos, Asreq_pos, num_pos, Astot_pos, cuant_pos, cuantOK_pos, Mpr_pos,
      Vug, Vum, Vu, Vc, Vs, Ab_est, s_calc, smax_prot, smax_cent, s_adopt_prot, s_adopt_cent, Zprot, Zcentral,
      a, Lmax_voladizo
    });
  }, [inputs]);

  const update = (f: string, v: any) => setInputs(prev => ({ ...prev, [f]: v }));
  const handleNum = (f: string, e: any) => update(f, parseFloat(e.target.value) || 0);

  if (!res) return null;

  return (
    <div className="layout-container">
      {/* HEADER */}
      <header className="main-header">
        <div className="logo-box">⬛</div>
        <div className="header-text">
          <h1>DISEÑO DE VIGAS DE HORMIGÓN ARMADO</h1>
          <span>Cálculo estructural reactivo — actualización en tiempo real</span>
        </div>
        <div className="normative">ACI 318 · NEC</div>
      </header>

      <div className="main-layout">
        {/* SIDEBAR INPUTS */}
        <aside className="sidebar">
          <div className="sidebar-scroll custom-scrollbar">
            <div className="section-title">
              <div className="dot cian"></div>
              <h2>DATOS DE ENTRADA</h2>
              <div className="live-status"><div className="pulse"></div> EN VIVO</div>
            </div>

            <div className="input-category">
              <div className="cat-title">◈ DATOS ARQUITECTÓNICOS</div>
              <InputRow label="Longitud en eje x (L1)" unit="m" value={inputs.L1} onChange={(e) => handleNum('L1', e)} />
              <InputRow label="Longitud en eje x (L2)" unit="m" value={inputs.L2} onChange={(e) => handleNum('L2', e)} />
              <InputRow label="Longitud en eje y (L3)" unit="m" value={inputs.L3} onChange={(e) => handleNum('L3', e)} />
              <InputRow label="Longitud en eje y (L4)" unit="m" value={inputs.L4} onChange={(e) => handleNum('L4', e)} />
              <InputRow label="Número de pisos (N°)" unit="u" value={inputs.pisos} onChange={(e) => handleNum('pisos', e)} />
              <InputRow label="Altura entrepiso" unit="m" value={inputs.He} onChange={(e) => handleNum('He', e)} />
              <SelectRow label="Uso" value={inputs.uso} options={['Vivienda', 'Oficina', 'Pesada', 'Otro']} onChange={(e) => update('uso', e.target.value)} />
            </div>

            <div className="input-category">
              <div className="cat-title orange">◈ CARGAS</div>
              <InputRow label="Carga muerta (Cm)" unit="t/m²" value={inputs.Cm} step="0.001" onChange={(e) => handleNum('Cm', e)} />
              <InputRow label="Carga viva (Cv)" unit="t/m²" value={inputs.Cv} onChange={(e) => handleNum('Cv', e)} />
              <div className="static-row">
                <label className="cian-label">Cu</label>
                <div className="val-box">
                  <span className="big-val cian">{res.Cu.toFixed(2)}</span>
                  <span className="unit">t/m²</span>
                </div>
              </div>
            </div>

            <div className="input-category">
              <div className="cat-title amber">◈ MATERIALES Y SISMICIDAD</div>
              <SelectRow label="Zona sísmica" value={inputs.zonaS} options={['Alta', 'Media', 'Baja']} onChange={(e) => update('zonaS', e.target.value)} />
              <InputRow label="Resistencia concreto (f'c)" unit="kg/cm²" value={inputs.fc} onChange={(e) => handleNum('fc', e)} />
              <InputRow label="Resistencia acero (fy)" unit="kg/cm²" value={inputs.fy} onChange={(e) => handleNum('fy', e)} />
            </div>

            <div className="input-category">
              <div className="cat-title lime">◈ SECCIÓN DE VIGA</div>
              <InputRow label="Ancho viga (b)" unit="cm" value={inputs.b} onChange={(e) => handleNum('b', e)} />
              <InputRow label="Recubrimiento (rec)" unit="cm" value={inputs.rec} onChange={(e) => handleNum('rec', e)} />
              <div className="input-row-special">
                <label>Altura definida (hdef)</label>
                <div className="wrap">
                  <input type="number" value={inputs.hdef} onChange={(e) => handleNum('hdef', e)} />
                  <span className="unit">cm</span>
                </div>
                <div className={`badge ${inputs.hdef >= res.hmin ? 'ok' : 'no'}`}>
                  {inputs.hdef >= res.hmin ? `≥ ${res.hmin} ✓` : `< ${res.hmin} ✗`}
                </div>
              </div>
            </div>

            <div className="input-category">
              <div className="cat-title orange">◈ ACERO NEGATIVO As(−)</div>
              <InputRow label="Diám. varilla (Øl)" unit="mm" value={inputs.fi_neg} onChange={(e) => handleNum('fi_neg', e)} />
            </div>

            <div className="input-category">
              <div className="cat-title lime">◈ ACERO POSITIVO As(+)</div>
              <InputRow label="Diám. varilla (Øl)" unit="mm" value={inputs.fi_pos} onChange={(e) => handleNum('fi_pos', e)} />
            </div>

            <div className="input-category">
              <div className="cat-title amber">◈ ESTRIBOS</div>
              <InputRow label="Diám. estribo (Øv)" unit="mm" value={inputs.fi_est} onChange={(e) => handleNum('fi_est', e)} />
              <InputRow label="Ancho columna (Bc)" unit="cm" value={inputs.bcol} onChange={(e) => handleNum('bcol', e)} />
            </div>
          </div>
        </aside>

        {/* DASHBOARD RESULTS */}
        <main className="dashboard custom-scrollbar">
          <div className="dashboard-grid">

            {/* BOX 1: SECCIÓN TRANSVERSAL */}
            <div className="card span-vertical">
              <div className="card-header">▸ Sección Transversal</div>
              <div className="card-body center">
                <BeamGraphics b={inputs.b} h={inputs.hdef} nNeg={res.num_neg} nPos={res.num_pos} fN={inputs.fi_neg} fP={inputs.fi_pos} />
                <div className="divider"></div>
                <div className={`dc-box ${res.DC <= 1 ? 'ok' : 'no'}`}>
                  <div className="dc-val">{res.DC.toFixed(4)}</div>
                  <div className="dc-lbl">DEMANDA / CAPACIDAD</div>
                </div>
                <div className="divider"></div>
                <div className="metric-list full-width">
                  <MetricRow label="Longitud viga mayor luz (Lv)" val={res.Lv.toFixed(2)} unit="m" accent="cian" />
                  <MetricRow label="Longitud viga transversal (Lt)" val={res.Lt.toFixed(2)} unit="m" accent="cian" />
                  <MetricRow label="Altura mínima (hmin)" val={res.hmin} unit="cm" accent="cian" />
                  <div className="sep"></div>
                  <MetricRow label="Relación h/b" val={res.rel.toFixed(2)} status={res.relOK} />
                  <MetricRow label="Peralte efectivo (d)" val={res.d.toFixed(1)} unit="cm" />
                  <MetricRow label="Recub. compresión (d')" val={res.dp.toFixed(1)} unit="cm" />
                  <MetricRow label="Carga mayorada (Cu)" val={res.Cu.toFixed(2)} unit="t/m²" />
                  <div className="sep"></div>
                  <MetricRow label="Momento diseño (Demanda)" val={res.Mdis.toFixed(2)} unit="t·m" accent="cian" />
                  <MetricRow label="Momento resistente (Capacidad)" val={res.Mres.toFixed(2)} unit="t·m" accent="orange" />
                </div>
              </div>
            </div>

            {/* BOX 2: CARGAS Y MOMENTOS */}
            <div className="card">
              <div className="card-header">▸ Cargas y Momentos</div>
              <div className="card-body">
                <MetricRow label="Acero mínimo (Asmin)" val={res.Asmin.toFixed(2)} unit="cm²" />
                <div className="sep"></div>
                <MetricRow label="Cuantía balanceada (pb)" val={res.pb.toFixed(6)} />
                <MetricRow label="Cuantía máxima (pmax)" val={res.pmax.toFixed(6)} />
                <MetricRow label="Bloque compresión (a)" val={res.a.toFixed(2)} unit="cm" />
                <MetricRow label="Long. máx. voladizo" val={res.Lmax_voladizo.toFixed(2)} unit="m" />
              </div>
            </div>

            {/* BOX 3: CORTANTE */}
            <div className="card">
              <div className="card-header red-dot">▸ Cortante</div>
              <div className="card-body">
                <MetricRow label="Cortante gravedad (Vug)" val={res.Vug.toFixed(2)} unit="t" />
                <MetricRow label="Cortante sismo (Vum)" val={res.Vum.toFixed(2)} unit="t" />
                <MetricRow label="Cortante total (Vu)" val={res.Vu.toFixed(2)} unit="t" accent="orange" />
                <MetricRow label="Cortante concreto (Vc)" val={res.Vc.toFixed(2)} unit="t" />
                <MetricRow label="Cortante acero (Vs)" val={res.Vs.toFixed(2)} unit="t" />
                <div className="sep"></div>
                <MetricRow label="Diám. estribo (Øv)" val={inputs.fi_est} unit="mm" />
                <MetricRow label="Área varilla estribo" val={res.Ab_est.toFixed(2)} unit="cm²" />
                <MetricRow label="Separación calculada (s)" val={res.s_calc.toFixed(2)} unit="cm" />
                <MetricRow label="Sep. máx. zona protegida" val={res.smax_prot} unit="cm" />
                <MetricRow label="Sep. máx. zona central" val={res.smax_cent} unit="cm" />
                <div className="sep"></div>
                <MetricRow label="s adoptado prot." val={res.s_adopt_prot.toFixed(1)} unit="cm" accent="cian-bg" />
                <MetricRow label="s adoptado cent." val={res.s_adopt_cent.toFixed(1)} unit="cm" accent="cian-bg" />
                <MetricRow label="Longitud zona protegida" val={res.Zprot} unit="cm" />
                <MetricRow label="Longitud zona central" val={res.Zcentral.toFixed(0)} unit="cm" />
              </div>
            </div>

            {/* BOX 4: ACERO NEGATIVO */}
            <div className="card">
              <div className="card-header orange-txt">▸ Acero As(−) Negativo</div>
              <div className="card-body">
                <MetricRow label="Diám. varilla long. (Øl)" val={inputs.fi_neg} unit="mm" />
                <MetricRow label="Área varilla (Ab)" val={res.Ab_neg.toFixed(2)} unit="cm²" />
                <MetricRow label="Acero requerido" val={res.Asreq_neg.toFixed(2)} unit="cm²" accent="orange" />
                <MetricRow label="N° varillas (base+adic.)" val={`${res.num_neg_base} base + ${res.num_neg_adic} adic.`} small />
                <MetricRow label="N° varillas total" val={res.num_neg} unit="u" accent="cian" />
                <MetricRow label="Área acero total" val={res.Astot_neg.toFixed(2)} unit="cm²" accent="cian" />
                <MetricRow label="Cuantía (p)" val={res.cuant_neg.toFixed(6)} status={res.cuant_neg <= res.pmax && res.cuant_neg >= (res.Asmin / (inputs.b * inputs.hdef))} />
                <MetricRow label="Separación varillas" val={res.sep_neg.toFixed(2)} unit="cm" status={res.sepOK_neg} />
                <MetricRow label="Momento probable (−)" val={res.Mpr_neg.toFixed(2)} unit="t·m" />
              </div>
            </div>

            {/* BOX 5: ACERO POSITIVO */}
            <div className="card">
              <div className="card-header lime-txt">▸ Acero As(+) Positivo</div>
              <div className="card-body">
                <MetricRow label="Diám. varilla long. (Øl)" val={inputs.fi_pos} unit="mm" />
                <MetricRow label="Área varilla (Ab)" val={res.Ab_pos.toFixed(2)} unit="cm²" />
                <MetricRow label="Acero requerido" val={res.Asreq_pos.toFixed(2)} unit="cm²" />
                <MetricRow label="N° varillas calculado" val={res.num_pos} unit="u" accent="cian" />
                <MetricRow label="N° varillas total" val={res.num_pos} unit="u" />
                <MetricRow label="Área acero total" val={res.Astot_pos.toFixed(2)} unit="cm²" accent="cian" />
                <MetricRow label="Cuantía (p)" val={res.cuant_pos.toFixed(6)} status={res.cuantOK_pos} />
                <MetricRow label="Momento probable (+)" val={res.Mpr_pos.toFixed(2)} unit="t·m" />
              </div>
            </div>

            {/* BOX 6: VERIFICACIONES */}
            <div className="card span-horizontal">
              <div className="card-header">▸ Verificaciones</div>
              <div className="card-body">
                <div className="checks-grid">
                  <CheckItem label="D/C Demanda/Capacidad" val={res.DC.toFixed(4)} ok={res.DC <= 1} />
                  <CheckItem label="Relación h/b sección" val={res.rel.toFixed(2)} ok={res.relOK} />
                  <CheckItem label="Cuantía acero negativo (−)" val={res.cuant_neg.toFixed(6)} ok={res.cuant_neg <= res.pmax && res.cuant_neg >= (res.Asmin / (inputs.b * inputs.hdef))} />
                  <CheckItem label="Cuantía acero positivo (+)" val={res.cuant_pos.toFixed(6)} ok={res.cuantOK_pos} />
                  <CheckItem label="Separación barras neg." val={res.sep_neg.toFixed(2) + ' cm'} ok={res.sepOK_neg} />
                  <CheckItem label="s adoptado prot. = MIN(s, smax)" val={res.s_adopt_prot.toFixed(1) + ' cm'} ok={true} />
                  <CheckItem label="s adoptado cent. = MIN(s, smax)" val={res.s_adopt_cent.toFixed(1) + ' cm'} ok={true} />
                </div>
              </div>
            </div>

          </div>
        </main>
      </div>
    </div>
  );
};

// --- HELPER COMPONENTS ---

const InputRow = ({ label, unit, value, onChange, step = "0.01" }: any) => (
  <div className="input-row">
    <label>{label}</label>
    <div className="wrap">
      <input type="number" step={step} value={value} onChange={onChange} />
      <span className="unit">{unit}</span>
    </div>
  </div>
);

const SelectRow = ({ label, value, options, onChange }: any) => (
  <div className="input-row">
    <label>{label}</label>
    <div className="wrap">
      <select value={value} onChange={onChange}>
        {options.map((o: any) => <option key={o} value={o}>{o}</option>)}
      </select>
    </div>
  </div>
);

const MetricRow = ({ label, val, unit, accent, small, status }: any) => (
  <div className="metric-row">
    <span className="m-lbl">{label}</span>
    <div className="m-val-wrap">
      <span className={`m-val ${accent ? accent : ''} ${small ? 'small' : ''}`}>
        {val}
      </span>
      {unit && <span className="m-unit">{unit}</span>}
      {status !== undefined && <span className={`m-status ${status ? 'ok' : 'no'}`}>{status ? 'OK' : 'NO'}</span>}
    </div>
  </div>
);

const CheckItem = ({ label, val, ok }: any) => (
  <div className="check-item">
    <span className="c-lbl">{label}</span>
    <div className="c-res">
      <span className="c-val">{val}</span>
      <span className={`c-status ${ok ? 'ok' : 'no'}`}>{ok ? 'OK' : 'NO'}</span>
    </div>
  </div>
);

const BeamGraphics = ({ b, h, nNeg, nPos, fN, fP }: any) => {
  const CW = 140, CH = 198;
  const scale = Math.min(CW / b, CH / h);
  const sw = b * scale, sh = h * scale;
  const sx = 60 + (CW - sw) / 2, sy = 15 + (CH - sh) / 2;
  const rpx = 2.5 * scale;
  const stx = sx + rpx, sty = sy + rpx;
  const stw = sw - 2 * rpx, sth = sh - 2 * rpx;

  const barPos = (n: number, x0: number, w: number, r: number) => {
    if (n <= 0) return [];
    if (n === 1) return [x0 + w / 2];
    const res = [x0 + r, x0 + w - r];
    for (let i = 1; i < Math.min(n, 10) - 1; i++) res.push((x0 + r) + (w - 2 * r) * i / (Math.min(n, 10) - 1));
    return res;
  };

  const rN = Math.min((fN / 10) * scale * 0.45, 7);
  const rP = Math.min((fP / 10) * scale * 0.45, 7);

  return (
    <svg width="220" height="230" viewBox="0 0 260 270">
      <defs>
        <pattern id="grid-hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <line x1="0" y1="0" x2="0" y2="6" stroke="rgba(0,242,255,0.05)" strokeWidth="1" />
        </pattern>
      </defs>
      <rect x={sx + 1} y={sy + 1} width={sw - 2} height={sh - 2} fill="url(#grid-hatch)" />
      <rect x={sx} y={sy} width={sw} height={sh} fill="none" stroke="#2D3748" strokeWidth="2" />
      <rect x={stx} y={sty} width={stw} height={sth} fill="none" stroke="#FFB830" strokeWidth="2.5" />

      {barPos(nNeg, stx, stw, rN).map((x, i) => <circle key={i} cx={x} cy={sty + rN + 1} r={rN} fill="#FF6B35" stroke="#FF9060" strokeWidth="0.5" />)}
      {barPos(nPos, stx, stw, rP).map((x, i) => <circle key={i} cx={x} cy={sty + sth - rP - 1} r={rP} fill="#7FFF6B" stroke="#AAFFAA" strokeWidth="0.5" />)}

      <g className="svg-labels">
        <line x1={sx} y1={sy + sh + 20} x2={sx + sw} y2={sy + sh + 20} stroke="#4A5568" />
        <text x={sx + sw / 2} y={sy + sh + 35} textAnchor="middle" fill="var(--accent)">{b} cm</text>
        <line x1={sx + sw + 20} y1={sy} x2={sx + sw + 20} y2={sy + sh} stroke="#4A5568" />
        <text x={sx + sw + 40} y={sy + sh / 2} textAnchor="middle" fill="var(--accent)" transform={`rotate(90, ${sx + sw + 40}, ${sy + sh / 2})`}>{h} cm</text>
      </g>
    </svg>
  );
};

export default App;
