pyinstaller --onefile --icon=assets/logo05022025.icns \
  --add-data "checkpoints/v7gpt-1.3.pth:checkpoints" \
  --add-data "checkpoints/db.json:checkpoints" \
  --add-data "checkpoints/dict.json:checkpoints" \
  --add-data "checkpoints/enum.json:checkpoints" \
  --add-data "checkpoints/renum_crt.json:checkpoints" \
  --add-data "checkpoints/renum.json:checkpoints" \
  --name v7 \
  main.py
