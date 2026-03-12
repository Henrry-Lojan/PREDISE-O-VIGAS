
/**
 * Reactive Structural Engine — ACI 318 / NEC
 * Formulas exactly as provided by the user.
 */

export interface BeamInputs {
    L1: number;
    L2: number;
    L3: number;
    L4: number;
    pisos: number;
    He: number;
    uso: string;
    Cm: number;
    Cv: number;
    zonaS: 'Alta' | 'Media' | 'Baja';
    fc: number;
    fy: number;
    b: number;
    rec: number;
    hdef: number;
    fi_neg: number;
    fi_pos: number;
    fi_est: number;
    bcol: number;
}

export interface BeamResults {
    Lv: number;
    Lt: number;
    Cu: number;
    Mdis: number;
    hmin: number;
    h: number;
    rel: number;
    relOK: boolean;
    d: number;
    dp: number;
    Asmin: number;
    pb: number;
    pmax: number;
    DC: number;
    // Negativo
    Ab_neg: number;
    Asreq_neg: number;
    num_neg: number;
    num_neg_base: number;
    num_neg_adic: number;
    Astot_neg: number;
    cuant_neg: number;
    sep_neg: number;
    sepOK_neg: boolean;
    Mres: number;
    Mpr_neg: number;
    // Positivo
    Ab_pos: number;
    Asreq_pos: number;
    num_pos: number;
    Astot_pos: number;
    cuant_pos: number;
    cuantOK_pos: boolean;
    Mpr_pos: number;
    // Cortante
    Vug: number;
    Vum: number;
    Vu: number;
    Vc: number;
    Vs: number;
    Ab_est: number;
    s_calc: number;
    smax_prot: number;
    smax_cent: number;
    s_adopt_prot: number;
    s_adopt_cent: number;
    Zprot: number;
    Zcentral: number;
    a: number; // Block compression depth
    Lmax_voladizo: number;
}

export const calculateBeam = (inputs: BeamInputs): BeamResults => {
    const {
        L1, L2, L3, L4, pisos, He, uso, Cm, Cv,
        zonaS, fc, fy, b, rec, hdef, fi_neg, fi_pos, fi_est, bcol
    } = inputs;

    // GEOMETRY
    const Lv = Math.max(L1, L2, L3, L4);
    const Lt = (L3 + L4) / 2;

    // Carga última
    const Cu = 1.2 * Cm + 1.6 * Cv;

    // Momento de diseño
    const Mdis = Cu * Lt * Math.pow(Lv - 0.3, 2) / 8 * 0.65 * 0.85 * 1.1;

    // h mínimo
    const hmin = Math.ceil(Math.sqrt(Mdis * 100000 / 0.145 / fc / b) + rec);

    // Definitive h
    const h = hdef;

    // Relación h/b
    const rel = h / b;
    const relOK = rel >= 1.1 && rel <= 1.6;

    // d efectivo y d'
    const d = h - rec - fi_est / 10 - fi_neg / 20;
    const dp = h - d;

    // Asmin
    const Asmin = 14 * b * d / fy;

    // pb y pmax
    const pb = 0.85 * 0.85 * fc / fy * (6100 / (6100 + fy));
    const pmax = (zonaS === 'Alta') ? 0.5 * pb : 0.75 * pb;

    // ACERO NEGATIVO
    const Ab_neg = 0.785 * Math.pow(fi_neg / 10, 2);
    const Asreq_neg = 30 * Mdis / d;
    const num_neg_base = Math.max(Math.floor(Asmin / Ab_neg), 2);
    const num_neg_adic = Math.floor((Asreq_neg - num_neg_base * Ab_neg) / Ab_neg) + 1;
    const num_neg = num_neg_base + num_neg_adic;
    const Astot_neg = num_neg * Ab_neg;
    const cuant_neg = Astot_neg / (b * h);
    const sep_neg = (b - 2 * rec - 2 - num_neg * fi_neg / 10) / (num_neg - 1);
    const sepOK_neg = sep_neg > Math.max(fi_neg / 10, 2.54);

    // Mres (resistencia)
    const a = Astot_neg * fy / (0.85 * fc * b);
    const Mres = 0.9 * (Astot_neg * fy * (d - a / 2)) / 100000;

    // D/C
    const DC = Mdis / Mres;

    // ACERO POSITIVO
    const Ab_pos = 0.785 * Math.pow(fi_pos / 10, 2);
    const Asreq_pos = 0.67 * Astot_neg;
    const num_pos = Math.floor(Asreq_pos / Ab_pos);
    const Astot_pos = num_pos * Ab_pos;
    const cuant_pos = Astot_pos / (b * h);
    const cuantOK_pos = cuant_pos <= pmax && cuant_pos >= (Asmin / (b * h));

    // Mpr negativo y positivo
    const Mpr_neg = 1.25 * Astot_neg * fy * (d - 1.25 * Astot_neg * fy / 1.7 / fc / b) / 100000;
    const Mpr_pos = 1.25 * Astot_pos * fy * (d - 1.25 * Astot_pos * fy / 1.7 / fc / b) / 100000;

    // CORTANTE
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

    return {
        Lv, Lt, Cu, Mdis, hmin, h, rel, relOK, d, dp, Asmin, pb, pmax, DC,
        Ab_neg, Asreq_neg, num_neg, num_neg_base, num_neg_adic, Astot_neg, cuant_neg, sep_neg, sepOK_neg, Mres, Mpr_neg,
        Ab_pos, Asreq_pos, num_pos, Astot_pos, cuant_pos, cuantOK_pos, Mpr_pos,
        Vug, Vum, Vu, Vc, Vs, Ab_est, s_calc, smax_prot, smax_cent, s_adopt_prot, s_adopt_cent, Zprot, Zcentral,
        a, Lmax_voladizo
    };
};
