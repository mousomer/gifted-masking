# E06 diagnostic smoke checkpoint

1. Run `frontiers_m4_path_diagnostics_v1_smoke` executed only the approved baseline smoke: 320 packed rows and 345,600 learner-steps.
2. The local diagnostic kernel replays maintained M4 softmax, acceptance draw, objective reward, selected-Q update, then post-reward receptivity update; parity is tested.
3. Real final-window action/outcome/reward counts, reset/continuity, strict raw validation, and raw-to-derived reconstruction passed.
4. Loop/transition outputs are diagnostic only (`decision_eligible=false`); no C8/C9 decision or hysteresis claim.
5. Phase-separated resources: wall=0.932s; raw=817314 bytes; RSS=79.859 MiB. Core projection={"learner_steps":913000000,"limits":{"raw_mib":400,"rss_mib":2048,"seconds":600,"total_mib":500},"method":"phase_separated_vectorized_n400_segment_benchmark_v1","n400_probe_seconds":{"500":0.038067542016506195,"1000":0.07654045801609755},"peak_rss_mib":119.625,"projected_components_seconds":{"derived":0.6253095902502537,"figure":0.5326056249905378,"serialization":5.740847449487774,"simulation":174.64785649906844,"startup":0.0},"raw_mib":126.6608476638794,"rows":52000,"seconds":181.546619163797,"segment_counts":{"500":275,"1000":2145},"smoke_phase_seconds":{"derived":0.06253095902502537,"figure":0.5326056249905378,"serialization":0.03532829199684784,"simulation":0.30118508398300037,"startup":0.0},"total_mib":140.82932472229004,"within_limits":true}. Qualification projection={"learner_steps":660000000,"method":"separate_non_authorizing_projection","peak_rss_mib":119.7890625,"raw_mib":73.07356595993042,"refused":true,"rows":30000,"seconds":579.3996666380473,"total_mib":81.24768733978271}.
6. Warnings: none.
7. Status: `pending_user_full_verification`. No standard or qualification run occurred.
