#!/bin/bash
set -e

echo ">> Actualizando paquetes e instalando dependencias"
sudo apt-get update -y
sudo apt-get install -y python3-pip python3-venv

echo ">> Creando entorno virtual para Jupyter (usuario vagrant)"
sudo -u vagrant bash -lc '
  set -e
  if [ ! -d "$HOME/jvenv" ]; then
    python3 -m venv $HOME/jvenv
  fi
  source $HOME/jvenv/bin/activate
  pip install --upgrade pip
  # Paquetes base (puedes sumar numpy/pandas/matplotlib si quieres)
  pip install jupyter
'

echo ">> (Opcional) Paquetes útiles extra"
sudo -u vagrant bash -lc '
  source $HOME/jvenv/bin/activate
  pip install numpy pandas matplotlib
'

echo ">> Creando servicio systemd para Jupyter"
sudo bash -c 'cat > /etc/systemd/system/jupyter.service <<EOF
[Unit]
Description=Jupyter Notebook (venv en /home/vagrant/jvenv)
After=network.target

[Service]
Type=simple
User=vagrant
WorkingDirectory=/home/vagrant
ExecStart=/home/vagrant/jvenv/bin/jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --NotebookApp.token=
Restart=always

[Install]
WantedBy=multi-user.target
EOF'

echo ">> Habilitando y arrancando servicio"
sudo systemctl daemon-reload
sudo systemctl enable --now jupyter

echo ">> Listo. Jupyter en http://192.168.90.3:8888 (o via port-forward en http://localhost:8888)"
