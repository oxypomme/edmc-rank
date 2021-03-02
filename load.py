# import sys
from typing import Optional, Tuple, Dict, Any, List
import tkinter as tk

import logging
import os

from config import appname
from theme import theme

from ranks import explorerRanks, merchantRanks, combatRanks

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

def calcNeed(pRank: Tuple[int, int], ranks: List[Tuple[int,str]]) -> Tuple[int, str]:
    if pRank[0] != 8:
        maxTodo = ranks[pRank[0] + 1][1] - ranks[pRank[0]][1]
        crTodo = maxTodo - (maxTodo * (pRank[1]/100))
    else:
        crTodo = 0

    if crTodo >= 1000000000:
        return (crTodo/1000000000, "BCr")
    elif crTodo >= 1000000:
        return (crTodo/1000000, "MCr")
    elif crTodo >= 1000:
        return (crTodo/1000, "kCr")
    return (crTodo, "Cr")

def drawRank(pRank: Tuple[int, int], ranks: List[Tuple[int,str]], labels: Tuple[tk.Label, tk.Label], name: str) -> None:
    # Show rank with percentage
    labels[0]["text"] = f"{name}: {ranks[pRank[0]][0]} ({pRank[0] + 1}) - {str(pRank[1])} %"
    # If not elite
    if pRank[0] != 8:
        need = calcNeed(pRank, ranks)
        # Show credits to farm
        # ? Maybe {:.3f}
        labels[1]["text"] = "   {:.2f}".format(need[0]) + f" {need[1]} to {ranks[pRank[0] + 1][0]} ({pRank[0] + 2})"
    else:
        # Remove label
        labels[1].grid_remove()

explorerEvents = ["StartUp", "Undocked", "SellExplorationData", "MissionCompleted"]
merchantEvents = ["StartUp", "Undocked", "MarketSell", "MissionCompleted"]
combatEvents = ["StartUp", "Undocked", "Docked", "Bounty", "MissionCompleted", "StartJump"]

def journal_entry(
    cmdr: str, is_beta: bool, system: str, station: str, entry: Dict[str, Any], state: Dict[str, Any]
) -> None:
    #logger.info(entry['event'])
    if entry["event"] in explorerEvents:
        global lblExplorer
        global statusExplorer
        drawRank(state["Rank"]["Explore"], explorerRanks, (lblExplorer, statusExplorer), "Explorer")

    if entry["event"] in merchantEvents:
        global lblMerchant
        global statusMerchant
        drawRank(state["Rank"]["Trade"], merchantRanks, (lblMerchant, statusMerchant), "Trader")

    if entry["event"] in combatEvents:
        global lblCombat
        lblCombat["text"] = "Combat: " + combatRanks[state["Rank"]["Combat"][0]] + " (" + str(state["Rank"]["Combat"][0] + 1) + ") - " + str(state["Rank"]["Combat"][1]) + "%"