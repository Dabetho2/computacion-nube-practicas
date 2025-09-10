#!/bin/bash
set -e

echo "1) Configurando /etc/resolv.conf con DNS de Google"
# OJO: usamos 'tee' con sudo para que la redirección tenga permisos de root.
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf >/dev/null

echo "2) Instalando vsftpd"
sudo apt-get update -y
sudo apt-get install -y vsftpd

echo "3) Habilitando escritura en vsftpd"
# Cambia '#write_enable=YES' por 'write_enable=YES' si está comentado
sudo sed -i 's/#write_enable=YES/write_enable=YES/' /etc/vsftpd.conf

echo "4) Activando IP forwarding"
echo "net.ipv4.ip_forward = 1" | sudo tee -a /etc/sysctl.conf >/dev/null

echo "5) Aplicando cambios"
sudo systemctl restart vsftpd || true
sudo sysctl -p || true

echo "Aprovisionamiento Shell completado."
