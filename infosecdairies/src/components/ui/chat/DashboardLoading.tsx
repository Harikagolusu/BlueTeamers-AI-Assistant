import React, { useEffect, useState } from 'react';
import { ShieldCheck, Cpu, Lock } from 'lucide-react';

const BOOT_LOG = [
  "BIOS POST............................ [ OK ]",
  "Loading BTeamOS kernel............... [ OK ]",
  "Mounting course knowledge base...... [ OK ]",
  "Spawning agent daemons.............. [ OK ]",
  "Knowledge Assistant.................. [ OK ]",
  "Learning Coach....................... [ OK ]",
  "Lab Mentor........................... [ OK ]",
  "SOC Analyst.......................... [ OK ]",
  "Investigation Agent.................. [ OK ]",
  "Threat Intelligence.................. [ OK ]",
  "Assessment Coach..................... [ OK ]",
  "Handshake verified................... [ OK ]",
  "Agent network synchronized.......... [ OK ]",
  "Ready. Awaiting operator input.",
];

const PARTICLES = Array.from({ length: 18 }, (_, i) => ({
  left: `${(i * 47) % 100}%`,
  delay: `${(i % 6) * 0.8}s`,
  duration: `${5 + (i % 4)}s`,
  size: i % 3 === 0 ? '3px' : '2px',
  opacity: 0.25 + (i % 5) * 0.1,
}));

export const DashboardLoading: React.FC = () => {
  const [logCount, setLogCount] = useState(1);
  const [percent, setPercent] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      setLogCount((c) => Math.min(c + 1, BOOT_LOG.length));
    }, 380);
    return () => clearInterval(id);
  }, []);

  useEffect(() => {
    const id = setInterval(() => {
      setPercent((p) => {
        if (p >= 100) return 100;
        return p + Math.ceil(Math.random() * 6);
      });
    }, 180);
    return () => clearInterval(id);
  }, []);

  return (
    <div className="relative flex flex-col items-center justify-center w-full h-full min-h-[calc(100dvh-4rem)] overflow-hidden bg-background">
      {/* Layered background */}
      <div
        className="absolute inset-0"
        style={{
          backgroundImage:
            'linear-gradient(rgba(0,214,193,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(0,214,193,0.05) 1px, transparent 1px)',
          backgroundSize: '44px 44px',
          maskImage: 'radial-gradient(ellipse 90% 80% at 50% 45%, black 20%, transparent 78%)',
          WebkitMaskImage: 'radial-gradient(ellipse 90% 80% at 50% 45%, black 20%, transparent 78%)',
        }}
      >
        <div className="absolute inset-0 animate-grid-move" style={{ backgroundImage: 'linear-gradient(rgba(0,214,193,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(0,214,193,0.05) 1px, transparent 1px)', backgroundSize: '44px 44px' }} />
      </div>
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_60%_50%_at_50%_40%,rgba(0,214,193,0.06),transparent_70%)]" />
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,transparent_55%,rgba(0,0,0,0.55))]" />

      {/* Ambient orbs */}
      <div className="absolute -top-24 left-1/4 w-96 h-96 bg-primary/8 rounded-full blur-[160px] animate-orb" />
      <div className="absolute bottom-0 right-1/5 w-[26rem] h-[26rem] bg-secondary/6 rounded-full blur-[160px] animate-orb" style={{ animationDelay: '3s' }} />

      {/* Rising particles */}
      {PARTICLES.map((p, i) => (
        <div
          key={i}
          className="absolute bottom-0 rounded-full bg-primary/40 animate-particle-rise pointer-events-none"
          style={{ left: p.left, width: p.size, height: p.size, animationDelay: p.delay, animationDuration: p.duration, opacity: p.opacity }}
        />
      ))}

      {/* Top HUD bar */}
      <div className="absolute top-0 left-0 right-0 z-40 flex items-center justify-between px-5 sm:px-8 py-4">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-secondary animate-pulse-glow" />
          <span className="text-[10px] font-mono tracking-[0.25em] text-zinc-400 uppercase">System Secure</span>
        </div>
        <div className="hidden sm:flex items-center gap-2 text-[10px] font-mono tracking-[0.25em] text-zinc-500 uppercase">
          <Lock className="w-3 h-3" />
          Encrypted Channel · AES-256
        </div>
        <div className="text-[10px] font-mono tracking-[0.25em] text-primary/80 uppercase">
          {String(percent).padStart(3, '0')}%
        </div>
      </div>

      {/* Side HUD rails */}
      <div className="absolute left-5 sm:left-8 top-1/2 -translate-y-1/2 hidden md:flex flex-col items-center gap-3 z-40">
        {Array.from({ length: 7 }).map((_, i) => (
          <span key={i} className={`w-1 h-1 rounded-full ${i < Math.ceil((logCount / BOOT_LOG.length) * 7) ? 'bg-primary' : 'bg-zinc-700'}`} />
        ))}
        <span className="text-[9px] font-mono tracking-widest text-zinc-500 uppercase -rotate-90 origin-center mt-2 whitespace-nowrap">Agents</span>
      </div>
      <div className="absolute right-5 sm:right-8 top-1/2 -translate-y-1/2 hidden md:flex flex-col items-center gap-3 z-40">
        <span className="text-[9px] font-mono tracking-widest text-zinc-500 uppercase rotate-90 origin-center mb-2 whitespace-nowrap">Kernel</span>
        {Array.from({ length: 7 }).map((_, i) => (
          <span key={i} className={`w-1 h-1 rounded-full ${i < Math.ceil((logCount / BOOT_LOG.length) * 7) ? 'bg-zinc-400' : 'bg-zinc-700'}`} />
        ))}
      </div>

      {/* Center: radar + content */}
      <div className="relative z-30 flex flex-col items-center animate-fade-up px-4">
        {/* Radar assembly */}
        <div className="relative w-52 h-52 sm:w-64 sm:h-64">
          {/* Outer glow ring */}
          <div className="absolute inset-[-14px] rounded-full border border-primary/10" />
          <div className="absolute inset-[-7px] rounded-full border border-primary/15" />

          {/* Tick marks */}
          {Array.from({ length: 60 }).map((_, i) => (
            <div
              key={i}
              className="absolute left-1/2 top-1/2"
              style={{ transform: `rotate(${i * 6}deg) translateY(-122px)`, width: i % 5 === 0 ? '2px' : '1px', height: i % 5 === 0 ? '10px' : '5px', background: i % 5 === 0 ? 'rgba(0,214,193,0.5)' : 'rgba(0,214,193,0.18)', position: 'absolute' }}
            />
          ))}
          {Array.from({ length: 12 }).map((_, i) => (
            <div
              key={`t${i}`}
              className="absolute left-1/2 top-1/2"
              style={{ transform: `rotate(${i * 30}deg) translateY(-104px)`, position: 'absolute' }}
            >
              <span className="block w-0.5 h-3.5 bg-primary/60" style={{ marginLeft: '-1px' }} />
            </div>
          ))}

          {/* Concentric rings */}
          <div className="absolute inset-0 rounded-full border border-primary/15" />
          <div className="absolute inset-[26%] rounded-full border border-primary/20" />
          <div className="absolute inset-[48%] rounded-full border border-primary/30" />
          <div className="absolute inset-0 rounded-full border border-primary/10 animate-ring" />
          <div className="absolute inset-0 rounded-full border border-primary/20 animate-ring" style={{ animationDelay: '0.9s' }} />

          {/* Crosshairs */}
          <div className="absolute left-1/2 top-0 bottom-0 w-px bg-primary/12" />
          <div className="absolute top-1/2 left-0 right-0 h-px bg-primary/12" />

          {/* Sweep */}
          <div className="absolute inset-0 rounded-full overflow-hidden">
            <div className="absolute inset-0 animate-radar">
              <div
                className="absolute top-1/2 left-1/2 w-1/2 h-1/2 origin-top-left"
                style={{ background: 'conic-gradient(from 0deg at 50% 50%, transparent 0deg, transparent 275deg, rgba(0,214,193,0.30) 335deg, transparent 360deg)' }}
              />
            </div>
          </div>

          {/* Blips */}
          <div className="absolute top-[26%] left-[32%] w-2 h-2 rounded-full bg-secondary shadow-[0_0_10px_rgba(130,203,21,0.9)] animate-pulse-glow" />
          <div className="absolute top-[60%] left-[66%] w-1.5 h-1.5 rounded-full bg-primary shadow-[0_0_8px_rgba(0,214,193,0.9)] animate-pulse-glow" style={{ animationDelay: '0.6s' }} />
          <div className="absolute top-[72%] left-[38%] w-1.5 h-1.5 rounded-full bg-secondary/70 shadow-[0_0_8px_rgba(130,203,21,0.7)] animate-pulse-glow" style={{ animationDelay: '1.2s' }} />

          {/* Core */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="relative w-16 h-16 sm:w-[4.5rem] sm:h-[4.5rem] rounded-2xl bg-gradient-to-br from-primary/20 via-[#0a0f1a] to-[#05070d] border border-primary/40 flex items-center justify-center shadow-[0_0_40px_rgba(0,214,193,0.25)] animate-flash-core">
              <ShieldCheck className="w-8 h-8 sm:w-9 sm:h-9 text-primary" />
              <span className="absolute inset-1 rounded-xl border border-primary/15" />
            </div>
          </div>

          {/* Orbiting satellites */}
          <div className="absolute inset-0 animate-spin-slow">
            <div className="absolute top-1/2 left-1/2 -ml-1 -mt-1 w-2 h-2 rounded-full bg-primary shadow-[0_0_10px_rgba(0,214,193,0.9)]" />
            <div className="absolute top-1/2 left-1/2 w-1 h-1 rounded-full bg-secondary shadow-[0_0_8px_rgba(130,203,21,0.8)] -ml-0.5 -mt-0.5" style={{ marginLeft: '0', marginTop: '0' }} />
          </div>
        </div>

        {/* Agents orbiting around the radar */}

        {/* Title */}
        <div className="flex flex-col items-center mt-6 mb-5">
          <div className="flex items-center gap-2.5">
            <span className="h-px w-8 sm:w-12 bg-gradient-to-r from-transparent to-primary/60" />
            <span className="text-2xl sm:text-3xl font-bold tracking-tight bg-gradient-to-b from-white to-white/60 bg-clip-text text-transparent">
              BlueTeamers <span className="text-primary">AI</span>
            </span>
            <span className="h-px w-8 sm:w-12 bg-gradient-to-l from-transparent to-primary/60" />
          </div>
          <p className="text-[11px] sm:text-xs font-mono text-zinc-500 mt-2 tracking-[0.3em] uppercase">
            Initializing Agent Network
          </p>
        </div>

        {/* Progress bar */}
        <div className="w-64 sm:w-80">
          <div className="flex items-center justify-between mb-1.5">
            <span className="text-[9px] font-mono tracking-widest text-zinc-500 uppercase">Loading</span>
            <span className="text-[9px] font-mono tracking-widest text-primary">{Math.min(percent, 100)}%</span>
          </div>
          <div className="h-1 rounded-full bg-zinc-800/80 overflow-hidden">
            <div
              className="h-full rounded-full bg-gradient-to-r from-primary via-primary to-secondary transition-all duration-200"
              style={{ width: `${Math.min(percent, 100)}%` }}
            />
          </div>
        </div>

        {/* Boot status */}
        <div className="mt-5 font-mono text-[11px] leading-relaxed h-16 overflow-hidden text-zinc-400 flex flex-col items-start">
          <p className="whitespace-pre text-left">
            {logCount < BOOT_LOG.length ? (
              <>
                <span className="text-zinc-500">$</span> <span className="text-zinc-300">{BOOT_LOG[logCount - 1]?.split('....')[0]}....</span>
                <span className="text-primary animate-pulse">▌</span>
              </>
            ) : (
              <>
                <span className="text-zinc-500">$</span>{' '}
                <span className="text-secondary">READY · ALL SYSTEMS NOMINAL</span>
              </>
            )}
            <br />
            <span className="text-zinc-600">agent-network · 7 nodes online · 0 threats detected</span>
          </p>
        </div>
      </div>

      {/* Bottom status ticker */}
      <div className="absolute bottom-0 left-0 right-0 z-40 border-t border-primary/10 bg-background/80 backdrop-blur px-5 sm:px-8 py-3 flex items-center justify-between">
        <span className="text-[9px] font-mono tracking-[0.2em] text-zinc-500 uppercase flex items-center gap-2">
          <Cpu className="w-3 h-3 text-primary/70" />
          BTEAM-OS v3.1.4
        </span>
        <span className="hidden sm:block text-[9px] font-mono tracking-[0.2em] text-zinc-600 uppercase">
          Threat Intel Feed · Updating
        </span>
        <span className="text-[9px] font-mono tracking-[0.2em] text-secondary/80 uppercase flex items-center gap-2">
          <span className="w-1.5 h-1.5 rounded-full bg-secondary animate-pulse-glow" />
          Online
        </span>
      </div>

      {/* Subtle scanline */}
      <div className="absolute inset-x-0 h-40 pointer-events-none z-20 opacity-40">
        <div className="absolute inset-x-0 h-px bg-gradient-to-r from-transparent via-primary/50 to-transparent animate-scan" />
      </div>
    </div>
  );
};

export default DashboardLoading;
