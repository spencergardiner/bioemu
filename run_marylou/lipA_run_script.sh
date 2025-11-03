# mamba activate bioemu
python -m bioemu.sample \
--sequence /home/ssgardin/nobackup/autodelete/bioemu/inputs/lipA_combined.a3m \
--num_samples 100 \
--output_dir /home/ssgardin/nobackup/autodelete/bioemu/outputs/lipA_100_2 \
--ckpt_path /home/ssgardin/.cache/huggingface/hub/models--microsoft--bioemu/snapshots/944333124e83f461bd644e62aa620b33957149cd/checkpoints/bioemu-v1.1/checkpoint.ckpt \
--model_config_path /home/ssgardin/.cache/huggingface/hub/models--microsoft--bioemu/snapshots/944333124e83f461bd644e62aa620b33957149cd/checkpoints/bioemu-v1.1/config.yaml \
