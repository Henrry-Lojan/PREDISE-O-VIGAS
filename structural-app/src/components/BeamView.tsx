
import React from 'react';

interface BeamViewProps {
    b: number;
    h: number;
    rec: number;
    numNeg: number;
    numPos: number;
    fiNeg: number;
    fiPos: number;
    fiEst: number;
}

const BeamView: React.FC<BeamViewProps> = ({
    b, h, rec, numNeg, numPos, fiNeg, fiPos, fiEst
}) => {
    // Scaling section to fit nicely in the card
    const maxWidth = 280;
    const maxHeight = 340;
    const scale = Math.min(maxWidth / b, maxHeight / h);

    const sw = b * scale;
    const sh = h * scale;

    // Center padding
    const ox = (maxWidth - sw) / 2 + 30; // Shifted for labels
    const oy = (maxHeight - sh) / 2 + 20;

    const rec_px = rec * scale;
    const fi_est_px = (fiEst / 10) * scale;

    // Rebar rendering
    const renderRebars = (num: number, fi: number, y: number, color: string) => {
        const bars = [];
        const r = (fi / 10) * scale / 2;
        const innerWidth = sw - 2 * rec_px - 2 * fi_est_px;
        const spacing = num > 1 ? innerWidth / (num - 1) : 0;
        const startX = ox + rec_px + fi_est_px;

        for (let i = 0; i < num; i++) {
            const cx = num > 1 ? startX + i * spacing : ox + sw / 2;
            bars.push(
                <g key={`bar-${y}-${i}`}>
                    {/* Metallic gradient effect */}
                    <defs>
                        <radialGradient id={`grad-${color}`} cx="30%" cy="30%" r="50%">
                            <stop offset="0%" stopColor="#fff" stopOpacity="0.4" />
                            <stop offset="100%" stopColor={color} />
                        </radialGradient>
                    </defs>
                    <circle
                        cx={cx}
                        cy={y}
                        r={Math.max(r, 2)}
                        fill={`url(#grad-${color})`}
                        stroke="rgba(0,0,0,0.3)"
                        strokeWidth="0.5"
                    />
                </g>
            );
        }
        return bars;
    };

    return (
        <div className="flex flex-col items-center justify-center p-6 bg-slate-900/40 rounded-2xl border border-white/5 glass shadow-2xl relative overflow-hidden">
            <div className="absolute top-0 right-0 p-4">
                <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest bg-slate-800/50 px-2 py-1 rounded">Scale 1:{(1 / scale).toFixed(1)}</div>
            </div>

            <h3 className="text-slate-400 mb-8 font-semibold uppercase tracking-widest text-xs flex items-center gap-2">
                <span className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" />
                Detalle de Refuerzo Transversal
            </h3>

            <div className="relative w-full max-w-[360px] h-[400px]">
                <svg viewBox="0 0 400 400" className="w-full h-full drop-shadow-2xl">
                    {/* Dimension Lines - Height */}
                    <line x1={ox - 25} y1={oy} x2={ox - 25} y2={oy + sh} stroke="#475569" strokeWidth="1" strokeDasharray="2,2" />
                    <path d={`M ${ox - 30} ${oy} L ${ox - 20} ${oy}`} stroke="#475569" strokeWidth="1" />
                    <path d={`M ${ox - 30} ${oy + sh} L ${ox - 20} ${oy + sh}`} stroke="#475569" strokeWidth="1" />
                    <text
                        x={ox - 35}
                        y={oy + sh / 2}
                        fill="#94a3b8"
                        fontSize="12"
                        textAnchor="middle"
                        transform={`rotate(-90, ${ox - 35}, ${oy + sh / 2})`}
                        className="font-mono font-bold"
                    >
                        h = {h} cm
                    </text>

                    {/* Dimension Lines - Width */}
                    <line x1={ox} y1={oy + sh + 25} x2={ox + sw} y2={oy + sh + 25} stroke="#475569" strokeWidth="1" strokeDasharray="2,2" />
                    <path d={`M ${ox} ${oy + sh + 30} L ${ox} ${oy + sh + 20}`} stroke="#475569" strokeWidth="1" />
                    <path d={`M ${ox + sw} ${oy + sh + 30} L ${ox + sw} ${oy + sh + 20}`} stroke="#475569" strokeWidth="1" />
                    <text
                        x={ox + sw / 2}
                        y={oy + sh + 45}
                        fill="#94a3b8"
                        fontSize="12"
                        textAnchor="middle"
                        className="font-mono font-bold"
                    >
                        b = {b} cm
                    </text>

                    {/* Main Concrete Section */}
                    <rect
                        x={ox}
                        y={oy}
                        width={sw}
                        height={sh}
                        rx="2"
                        fill="#1e293b"
                        stroke="#334155"
                        strokeWidth="2"
                    />
                    {/* Concrete Texture/Grain (Subtle) */}
                    <rect x={ox + 2} y={oy + 2} width={sw - 4} height={sh - 4} fill="url(#concrete-pattern)" opacity="0.1" />

                    {/* Stirrup (Estribo) */}
                    <rect
                        x={ox + rec_px}
                        y={oy + rec_px}
                        width={sw - 2 * rec_px}
                        height={sh - 2 * rec_px}
                        rx="4"
                        fill="none"
                        stroke="#f59e0b"
                        strokeWidth={Math.max(fi_est_px, 1.5)}
                        className="drop-shadow-[0_0_2px_rgba(245,158,11,0.5)]"
                    />
                    {/* Stirrup Hooks (Stylized) */}
                    <path
                        d={`M ${ox + rec_px + 8} ${oy + rec_px} L ${ox + rec_px} ${oy + rec_px} L ${ox + rec_px} ${oy + rec_px + 8} M ${ox + rec_px} ${oy + rec_px} L ${ox + rec_px + 6} ${oy + rec_px + 6}`}
                        stroke="#f59e0b"
                        strokeWidth={Math.max(fi_est_px, 1.5)}
                        fill="none"
                    />

                    {/* Negative Bars (Top) */}
                    {renderRebars(numNeg, fiNeg, oy + rec_px + fi_est_px + (fiNeg / 20) * scale, '#ef4444')}

                    {/* Positive Bars (Bottom) */}
                    {renderRebars(numPos, fiPos, oy + sh - rec_px - fi_est_px - (fiPos / 20) * scale, '#10b981')}

                    {/* Patterns */}
                    <defs>
                        <pattern id="concrete-pattern" width="10" height="10" patternUnits="userSpaceOnUse">
                            <circle cx="2" cy="2" r="0.5" fill="#fff" />
                            <circle cx="8" cy="7" r="0.5" fill="#fff" />
                        </pattern>
                    </defs>
                </svg>
            </div>

            <div className="w-full grid grid-cols-2 gap-3 mt-4">
                <div className="flex items-center gap-2 p-2 rounded-lg bg-red-500/5 border border-red-500/10">
                    <div className="w-1.5 h-1.5 rounded-full bg-red-500" />
                    <span className="text-[10px] text-slate-400 font-bold uppercase tracking-tight">Acero As(−)</span>
                    <span className="text-[10px] text-white font-mono ml-auto">{numNeg}Φ{fiNeg}mm</span>
                </div>
                <div className="flex items-center gap-2 p-2 rounded-lg bg-emerald-500/5 border border-emerald-500/10">
                    <div className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                    <span className="text-[10px] text-slate-400 font-bold uppercase tracking-tight">Acero As(+)</span>
                    <span className="text-[10px] text-white font-mono ml-auto">{numPos}Φ{fiPos}mm</span>
                </div>
                <div className="flex items-center gap-2 p-2 rounded-lg bg-amber-500/5 border border-amber-500/10 col-span-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-amber-500" />
                    <span className="text-[10px] text-slate-400 font-bold uppercase tracking-tight">Estribo</span>
                    <span className="text-[10px] text-white font-mono ml-auto">Φ{fiEst}mm @ variab.</span>
                </div>
            </div>
        </div>
    );
};

export default BeamView;
