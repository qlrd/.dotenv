killall waybar
waybar &

hyprctl reload

killall hyprpaper
pkill -f "random-wallpaper.sh"
sleep 1

hyprpaper &
sh ~/.config/hypr/scripts/random-wallpaper.sh &
