# Landing-page film

`ds3_014-intro.mp4` is a presentation excerpt of the historical `ds3_014`
simulation, with the fields combined in one view. It is not a new simulation or
an evaluation rollout. The original research animations, including plots, remain
in `../blobs/p7_world_ds3_014.gif` and `../blobs/p7_world_ds3_014_long.gif`.

The user supplied the source recording on 2026-09-15:
`Screen Recording 2026-08-24 at 11.06.59 AM (1).mov`, SHA-256
`3a25fc29801eea1907df4d83c9b5157448dbe08d1dc72c73715a706a8fe91281`.
The recording is retained locally. The web export removes the title, timestamp,
and border, preserves playback order and speed, and has no audio. Its restart
is an ordinary replay, not a claim of periodic dynamics.

Export with FFmpeg using `crop=418:418:18:29,fps=30`, H.264, `yuv420p`, CRF 19,
the slow preset, `+faststart`, and no metadata. `ds3_014-intro.jpg` is the frame
at five seconds, used as the video's loading poster. These are static media
inputs preserved by `scripts/build_docs.py`.
