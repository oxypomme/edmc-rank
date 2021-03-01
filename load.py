# edmc-ranks v1

# import sys
from typing import Optional, Tuple, Dict, Any, List
import tkinter as tk

import logging
import os

from config import appname
from theme import theme

# This could also be returned from plugin_start3()
plugin_name = os.path.basename(os.path.dirname(__file__))

# A Logger is used per 'found' plugin to make it easy to include the plugin's
# folder name in the logging output format.
# NB: plugin_name here *must* be the plugin's folder name as per the preceding
#     code, else the logger won't be properly set up.
logger = logging.getLogger(f'{appname}.{plugin_name}')

# If the Logger has handlers then it was already set up by the core code, else
# it needs setting up here.
if not logger.hasHandlers():
    level = logging.INFO  # So logger.info(...) is equivalent to print()

    logger.setLevel(level)
    logger_channel = logging.StreamHandler()
    logger_formatter = logging.Formatter(f'%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d:%(funcName)s: %(message)s')
    logger_formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
    logger_formatter.default_msec_format = '%s.%03d'
    logger_channel.setFormatter(logger_formatter)
    logger.addHandler(logger_channel)

lblExplorer: Optional[tk.Label]
statusExplorer: Optional[tk.Label]
lblMerchant: Optional[tk.Label]
statusMerchant: Optional[tk.Label]
lblCombat: Optional[tk.Label]

def plugin_start3(plugin_dir: str) -> str:
    """
    Load this plugin into EDMC
    """
    return "edmc-rank"


def plugin_app(parent: tk.Frame) -> Tuple[tk.Label, tk.Label]:
    """
    Create a pair of TK widgets for the EDMC main window
    """
    frame = tk.Frame(parent)
    frame.columnconfigure(1, weight=1)

    global lblExplorer
    lblExplorer = tk.Label(frame, text="Explorer:")
    lblExplorer.grid(row=0, column=1, sticky=tk.W)
    global statusExplorer
    statusExplorer = tk.Label(frame, text="   ? Cr")
    statusExplorer.grid(row=1, column=1, sticky=tk.W)

    global lblMerchant
    lblMerchant = tk.Label(frame, text="Trader:")
    lblMerchant.grid(row=2, column=1, sticky=tk.W)
    global statusMerchant
    statusMerchant = tk.Label(frame, text="   ? Cr")
    statusMerchant.grid(row=3, column=1, sticky=tk.W)

    global lblCombat
    lblCombat = tk.Label(frame, text="Combat:")
    lblCombat.grid(row=4, column=1, sticky=tk.W)

    return frame

merchantRanks = [
    ("Penniless", 0),
    ("M. Pennilesss", 5000),
    ("Peddler", 100000),
    ("Dealer", 800000),
    ("Merchant", 3700000),
    ("Broker", 30000000),
    ("Entrepreneur", 140000000),
    ("Tycoon", 390000000),
    ("Elite", 1050000000)
]
explorerRanks = [
    ("Aimless", 0),
    ("M. Aimless", 40000),
    ("Scout", 270000),
    ("Surveyor", 1140000),
    ("Trailblazer", 4200000),
    ("Pathfinder", 10000000),
    ("Ranger", 35000000),
    ("Pioneer", 116000000),
    ("Elite", 320000000)
]
combatRanks = [
    "Harmless",
    "M. Harmless",
    "Novice",
    "Competent",
    "Expert",
    "Master",
    "Dangerous",
    "Deadly",
    "Elite"
]

def calcNeed(state: Dict[str, Any], categ: str, ranks: List[Tuple[str, int]]) -> Tuple[int, str]:
    if state["Rank"][categ][0] != 8:
        maxTodo = ranks[state["Rank"][categ][0] + 1][1] - ranks[state["Rank"][categ][0]][1]
        crTodo = maxTodo - (maxTodo * (state["Rank"][categ][1]/100))
    else:
        crTodo = 0
    if crTodo >= 1000000000:
        return (crTodo/1000000000, "BCr")
    elif crTodo >= 1000000:
        return (crTodo/1000000, "MCr")
    elif crTodo >= 1000:
        return (crTodo/1000, "kCr")
    else:
        return (crTodo, "Cr")

def journal_entry(
    cmdr: str, is_beta: bool, system: str, station: str, entry: Dict[str, Any], state: Dict[str, Any]
) -> None:
    logger.info(entry['event'])
    if entry['event'] == 'StartUp' or entry["event"] == "FSDJump" or entry["event"] == "Location":
        need = calcNeed(state, "Explore", explorerRanks)
        global lblExplorer
        lblExplorer["text"] = "Explorer: " + explorerRanks[state["Rank"]["Explore"][0]][0] + " - " + str(state["Rank"]["Explore"][1]) + "%"
        global statusExplorer
        if state["Rank"]["Explore"][0] != 8:
            statusExplorer["text"] = ("   {:.2f}".format(need[0]) + " " + need[1] + " to " + explorerRanks[state["Rank"]["Explore"][0] + 1][0])
        else:
            statusExplorer.grid_remove()

        need = calcNeed(state, "Trade", merchantRanks)
        global lblMerchant
        lblMerchant["text"] = "Trader: " + merchantRanks[state["Rank"]["Trade"][0]][0] + " - " + str(state["Rank"]["Trade"][1]) + "%"
        global statusMerchant
        if state["Rank"]["Trade"][0] != 8:
            statusMerchant["text"] = ("   {:.2f}".format(need[0]) + " " + need[1] + " to " + merchantRanks[state["Rank"]["Trade"][0] + 1][0])
        else:
            statusMerchant.grid_remove()

        global lblCombat
        lblCombat["text"] = "Combat: " + combatRanks[state["Rank"]["Combat"][0]] + " - " + str(state["Rank"]["Combat"][1]) + "%"