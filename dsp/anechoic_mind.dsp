declare name        "Anechoic Mind";
declare version     "0.1.0";
declare author      "Axiom Rasa";
declare license     "Proprietary - Axiom Rasa";
declare description "Phenomenological Isolation and Inner Speech Processor";

import("stdfaust.lib");

// --- Master Axiom Shell & Macro GUI Parameters ---
isolation   = hslider("[0] Isolation Depth [unit:%]", 0.0, 0.0, 1.0, 0.001) : si.smoo;
cranial_res = hslider("[1] Cranial Resonance", 0.5, 0.1, 0.95, 0.001) : si.smoo;
body_level  = hslider("[2] Internal Body Noise", 0.4, 0.0, 1.0, 0.001) : si.smoo;
dry_wet     = hslider("[3] Dry/Wet Mix [unit:%]", 1.0, 0.0, 1.0, 0.001) : si.smoo;
master_gain = hslider("[4] Output Gain [unit:dB]", 0.0, -60.0, 12.0, 0.1) : ba.db2linear : si.smoo;

// --- 1. Outer World Attenuation (Focus to Fringe) ---
outer_cutoff = 150.0 + (16000.0 - 150.0) * pow(1.0 - isolation, 3.0);
outer_gain   = 1.0 - (isolation * 0.8);

muffle(x) = x : fi.lowpass(2, outer_cutoff);

// --- 2. Bone Conduction & Cranial Comb Filter ---
comb_del_sec  = 0.002 + (1.0 - cranial_res) * 0.005;
comb_samples  = max(1.0, comb_del_sec * ma.SR);

cranial_space(x) = x : (+ ~ (de.fdelay(4096, comb_samples) : fi.lowpass(1, 1500.0) : *(cranial_res * 0.85)));

process_channel(x) = (muffle(x) * (1.0 - isolation) + (muffle(x) : cranial_space) * isolation) * outer_gain;

// --- 3. Anechoic Bodily Interior (Bloodstream & Nervous System) ---
body_curve  = pow(isolation, 2.0) * body_level;
pulse_lfo   = os.osc(1.1) * 0.5 + 0.5;
blood_flow  = no.pink_noise : fi.resonbp(65.0 + pulse_lfo * 15.0, 3.0, 1.0) * (body_curve * 0.4);
nerve_whine = os.osc(3840.0 + no.lfnoise(2.0) * 8.0) * (body_curve * 0.012);

internal_noise = blood_flow + nerve_whine;

// --- 4. Spatial Collapse & Axiom Shell Output ---
width = 1.0 - isolation;

engine(l, r) = out_l, out_r
with {
    proc_l = process_channel(l);
    proc_r = process_channel(r);
    mono   = (proc_l + proc_r) * 0.5;
    
    // Stereo field narrows toward center of head as isolation increases
    collapsed_l = proc_l * width + mono * (1.0 - width);
    collapsed_r = proc_r * width + mono * (1.0 - width);
    
    wet_l = collapsed_l + internal_noise;
    wet_r = collapsed_r + internal_noise;
    
    // Master Axiom Shell: Dry/Wet Blend & Speaker Protection Limiter
    mix_l = l * (1.0 - dry_wet) + wet_l * dry_wet;
    mix_r = r * (1.0 - dry_wet) + wet_r * dry_wet;
    
    out_l = mix_l * master_gain : ma.tanh;
    out_r = mix_r * master_gain : ma.tanh;
};

process(l, r) = engine(l, r);
