#!/bin/bash
set -e

log() { echo -e "==> $*"; }

log "1) Instalando snapd y LXD"
sudo apt-get update -y
sudo apt-get install -y snapd
sudo snap install core || true
sudo snap install lxd

log "2) Inicializando LXD (no interactivo)"
sudo lxd init --auto

log "2.1) Asegurando remotos 'ubuntu' e 'images'"
if ! lxc remote list | grep -qE '^\|\s+ubuntu\s+\|'; then
  sudo lxc remote add ubuntu https://cloud-images.ubuntu.com/releases --protocol=simplestreams --public
fi
if ! lxc remote list | grep -qE '^\|\s+images\s+\|'; then
  sudo lxc remote add images https://images.lxd.canonical.com --protocol=simplestreams --public
fi

log "3) Creando contenedor 'web1' (con fallback de imágenes)"
if ! lxc info web1 >/dev/null 2>&1; then
  IMAGES=("ubuntu:jammy" "ubuntu:22.04" "images:ubuntu/jammy" "images:ubuntu/22.04" "images:ubuntu/jammy/amd64" "images:ubuntu/22.04/amd64")
  CREATED=0
  for IMG in "${IMAGES[@]}"; do
    log "   - Intentando imagen: $IMG"
    if sudo lxc launch "$IMG" web1 < /dev/null; then
      CREATED=1
      break
    fi
  done
  if [ "$CREATED" -ne 1 ]; then
    echo "ERROR: no se pudo lanzar 'web1' desde ninguno de los remotos/alias probados."
    sudo lxc remote list || true
    exit 1
  fi
fi

log "4) Esperando a que 'web1' esté RUNNING con IP"
for i in {1..30}; do
  STATUS=$(lxc info web1 2>/dev/null | awk -F': ' '/^Status:/{print $2}')
  if echo "$STATUS" | grep -q '^Running'; then break; fi
  sleep 2
done
sudo lxc list

if ! lxc info web1 | grep -q '^Status: RUNNING'; then
  echo "ERROR: 'web1' no está RUNNING tras el tiempo de espera."
  exit 1
fi

log "5) Instalando nginx y sitio personalizado dentro del contenedor"
sudo lxc exec web1 -- bash -lc "apt-get update -y && apt-get install -y nginx"
sudo lxc exec web1 -- bash -lc "bash -c 'cat > /var/www/html/index.html <<EOF
<!doctype html>
<html lang=\"es\">
<head><meta charset=\"utf-8\"><title>Sitio LXD - OK</title></head>
<body style=\"font-family:system-ui; padding:2rem;\">
  <h1>¡LXD funcionando en contenedor!</h1>
  <p>Servido por <b>nginx</b> dentro de un contenedor LXD (<code>web1</code>).</p>
  <p>Práctica 5 - Nota extra</p>
</body>
</html>
EOF'"
sudo lxc exec web1 -- systemctl restart nginx

log "6) Publicando puerto del contenedor en la VM (8080 -> 80)"
sudo lxc config device remove web1 web80 || true
sudo lxc config device add web1 web80 proxy listen=tcp:0.0.0.0:8080 connect=tcp:127.0.0.1:80

log "7) Evidencias"
echo "[VM] Escucha en 0.0.0.0:8080:"; ss -ltnp | grep 8080 || true
echo "[LXD] Contenedores:"; sudo lxc list
echo "Abre desde tu host:  http://192.168.90.4:8080"
