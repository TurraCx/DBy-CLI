from modules import DanishBytes
from colorama import Fore
from sys import platform
import subprocess
import json
import sys
import os

def clear():
    if platform == "linux" or platform == "linux2":
        os.system('clear')
    elif platform == "darwin":
        os.system('clear')
    elif platform == "win32":
        os.system('cls')
    print(
        f"{Fore.LIGHTGREEN_EX} ____          _     _   _____     _           \n"+
        "|    \ ___ ___|_|___| |_| __  |_ _| |_ ___ ___ \n"+
        "|  |  | .'|   | |_ -|   | __ -| | |  _| -_|_ -|\n"+
        "|____/|__,|_|_|_|___|_|_|_____|_  |_| |___|___|\n"+
        f"                              |___|{Fore.RESET}\n"
    )

def question(question):
    output = f"{question}"
    if "(" in question:
        output = f"{question.split('(')[0]} {Fore.LIGHTBLACK_EX}({question.split('(')[1]}{Fore.RESET}"
    return input(f"[{Fore.LIGHTCYAN_EX}?{Fore.RESET}] {output}\n[{Fore.LIGHTYELLOW_EX}>{Fore.RESET}] ")

def getch_question(question):
    output = f"{question}"
    if "(" in question:
        output += f" ({question.split('(')[1]}"
    print(f"[{Fore.LIGHTCYAN_EX}?{Fore.RESET}] {output}\n[{Fore.LIGHTYELLOW_EX}>{Fore.RESET}]", end=" ")
    import sys
    if sys.platform[:3] == 'win':
        import msvcrt

        def getkey():
            key = msvcrt.getch()
            return key
    elif sys.platform[:3] == 'lin':
        import termios
        import sys
        import os

        def getkey():
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            new = termios.tcgetattr(fd)
            new[3] = new[3] & ~termios.ICANON & ~termios.ECHO
            new[6][termios.VMIN] = 1
            new[6][termios.VTIME] = 0
            termios.tcsetattr(fd, termios.TCSANOW, new)
            try:
                c = os.read(fd, 1)
            finally:
                termios.tcsetattr(fd, termios.TCSAFLUSH, old)
            return c
    else:
        def getkey():
            print("Not your system, bud.")
    return getkey()

def calc(size):
    if 1024 <= size < 1024*1024:
        return f"{round(size/1024, 2)} KB"
    elif 1024*1024 <= size < 1024*1024*1024:
        return f"{round(size/1024/1024, 2)} MB"
    elif 1024*1024*1024 <= size < 1024*1024*1024*1024:
        return f"{round(size/1024/1024/1024, 2)} GB"

def open_magnet(magnet):
    if sys.platform.startswith('linux'):
        subprocess.Popen(['xdg-open', magnet],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif sys.platform.startswith('win32'):
        os.startfile(magnet)
    elif sys.platform.startswith('cygwin'):
        os.startfile(magnet)
    elif sys.platform.startswith('darwin'):
        subprocess.Popen(['open', magnet],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        subprocess.Popen(['xdg-open', magnet],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def main():
    clear()
    d = DanishBytes.DanishBytes()
    try:
        config = json.load(open("config.json", "r+"))
    except Exception:
        config = {}
        config['api_key'] = question("Hvad er din API nøgle? (Tryk på enter for at jeg selv henter din api key via login vindue)")
    if 'api_key' not in config or config['api_key'] == None or config['api_key'] == '':
        if 'db_session' not in config or config['db_session'] == '':
            config['db_session'], username = d.authenticate()
            d.set_session(config['db_session'])
        config['api_key'] = d.get_api()
    d.set_api(config['api_key'])
    json.dump(config, open("config.json", "w+"), indent=2, sort_keys=True)
    search = question("Hvilken film skal jeg prøve at finde for dig?")
    movies = d.find_movie(search)
    clear()
    if movies['resultsCountTotal'] > 0:
        i = 1
        for torrent in movies['torrents']:
            print(f"[{Fore.LIGHTGREEN_EX}{i}{Fore.RESET}] {torrent['name']} - {calc(torrent['size'])} | S: {torrent['seeders']} | L: {torrent['leechers']}")
            i += 1
        picked = int(getch_question("Hvilken film skal jeg begynde at hente?"))
        print(movies['torrents'][picked-1])
        print(f"\n[{Fore.LIGHTGREEN_EX}1{Fore.RESET}] Download .torrent fil")
        print(f"[{Fore.LIGHTGREEN_EX}2{Fore.RESET}] Åben magnet link")
        dl_as = int(getch_question("Hvordan skal jeg håndtere filmen?"))
        if dl_as == 1:
            os.system(f"start https://danishbytes.club/torrent/download/{movies['torrents'][picked-1]['id']}.{movies['rss_key']}")
        elif dl_as == 2:
            torrent = d.get_torrent(movies['torrents'][picked-1]['id'])
            magnet = f"magnet:?dn={movies['torrents'][picked-1]['name']}&xt=urn:btih:{movies['torrents'][picked-1]['info_hash']}&as=https://danishbytes.club/torrent/download/{movies['torrents'][picked-1]['id']}.{movies['rss_key']}&xl={movies['torrents'][picked-1]['size']}&tr=https://danishbytes.club/announce/e064ba0c35d252338572fd7720448cc5&tr=https://danishbytes.org/announce/e064ba0c35d252338572fd7720448cc5&tr=https://danishbytes2.org/announce/e064ba0c35d252338572fd7720448cc5&tr=https://danishbytes.art/announce/e064ba0c35d252338572fd7720448cc5"
            open_magnet(magnet)
            print("Burde være åbnet i din Bit klient nu.")
        return
    print(f"[{Fore.BLUE}i{Fore.RESET}] Ingen film for {search} fundet, prøv med noget andet?")
    return


if __name__ == '__main__':
    main()
    