# import sys
from typing import Optional, Tuple, Dict, Any, List
import tkinter as tk

import logging
import os

from config import appname, config
from theme import theme
import myNotebook as nb

from ranks import explorerRanks, merchantRanks, combatRanks, empireRanks, fedRanks

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


showExplorer: Optional[tk.IntVar] = None
showMerchant: Optional[tk.IntVar] = None
showCombat: Optional[tk.IntVar] = None
showEmpire: Optional[tk.IntVar] = None
showFederation: Optional[tk.IntVar] = None

lblExplorer: Optional[tk.Label]
statusExplorer: Optional[tk.Label]
lblMerchant: Optional[tk.Label]
statusMerchant: Optional[tk.Label]
lblCombat: Optional[tk.Label]
lblEmpire: Optional[tk.Label]
lblFederation: Optional[tk.Label]

def plugin_start3(plugin_dir: str) -> str:
    """
    Load this plugin into EDMC
    """
    global showExplorer
    showExplorer = tk.IntVar(value=config.get_int("showExplorer"))
    global showMerchant
    showMerchant = tk.IntVar(value=config.get_int("showMerchant"))
    global showCombat
    showCombat = tk.IntVar(value=config.get_int("showCombat"))
    global showEmpire
    showEmpire = tk.IntVar(value=config.get_int("showEmpire"))
    global showFederation
    showFederation = tk.IntVar(value=config.get_int("showFederation"))
    return "edmc-rank"

def plugin_prefs(parent, cmdr, is_beta):
    frame = nb.Frame(parent)
    frame.columnconfigure(2, weight=1)

    nb.Label(frame, text="Show :").grid(row = 0, column=0, sticky=tk.W)
    global showExplorer
    nb.Checkbutton(frame, text="Explorer", variable=showExplorer).grid(row=1, column=1, sticky=tk.W)
    global showMerchant
    nb.Checkbutton(frame, text="Trader", variable=showMerchant).grid(row=2, column=1, sticky=tk.W)
    global showCombat
    nb.Checkbutton(frame, text="Combat", variable=showCombat).grid(row=3, column=1, sticky=tk.W)
    global showEmpire
    nb.Checkbutton(frame, text="Empire", variable=showEmpire).grid(row=4, column=1, sticky=tk.W)
    global showFederation
    nb.Checkbutton(frame, text="Federation", variable=showFederation).grid(row=5, column=1, sticky=tk.W)

    return frame

def prefs_changed(cmdr, is_beta):
    global showExplorer
    config.set("showExplorer", showExplorer.get())
    global showMerchant
    config.set("showMerchant", showMerchant.get())
    global showCombat
    config.set("showCombat", showCombat.get())
    global showEmpire
    config.set("showEmpire", showEmpire.get())
    global showFederation
    config.set("showFederation", showFederation.get())
    display()

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

    global lblEmpire
    lblEmpire = tk.Label(frame, text="Empire:")
    lblEmpire.grid(row=6, column=1, sticky=tk.W)

    global lblFederation
    lblFederation = tk.Label(frame, text="Federation:")
    lblFederation.grid(row=7, column=1, sticky=tk.W)
    display()

    return frame

def display():
    global lblExplorer
    global statusExplorer
    if (config.get_int("showExplorer") != 1):
        lblExplorer.grid_remove()
        statusExplorer.grid_remove()
    else:
        lblExplorer.grid(row=0, column=1, sticky=tk.W)
        statusExplorer.grid(row=1, column=1, sticky=tk.W)

    global lblMerchant
    global statusMerchant
    if (config.get_int("showMerchant") != 1):
        lblMerchant.grid_remove()
        statusMerchant.grid_remove()
    else:
        lblMerchant.grid(row=2, column=1, sticky=tk.W)
        statusMerchant.grid(row=3, column=1, sticky=tk.W)

    global lblCombat
    if (config.get_int("showCombat") != 1):
        lblCombat.grid_remove()
    else:
        lblCombat.grid(row=4, column=1, sticky=tk.W)

    global lblEmpire
    if (config.get_int("showEmpire") != 1):
        lblEmpire.grid_remove()
    else:
        lblEmpire.grid(row=6, column=1, sticky=tk.W)

    global lblFederation
    if (config.get_int("showFederation") != 1):
        lblFederation.grid_remove()
    else:
        lblFederation.grid(row=7, column=1, sticky=tk.W)


def calcNeed(pRank: Tuple[int, int], ranks: List[Tuple[int,str]]) -> Tuple[int, str]:
    if pRank[0] != len(ranks) - 1:
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

def drawRankTodo(pRank: Tuple[int, int], ranks: List[Tuple[int,str]], labels: Tuple[tk.Label, tk.Label], name: str) -> None:
    # Show rank with percentage
    labels[0]["text"] = f"{name}: {ranks[pRank[0]][0]} ({pRank[0] + 1}) - {str(pRank[1])} %"
    # If not elite
    if pRank[0] != len(ranks) - 1:
        need = calcNeed(pRank, ranks)
        # Show credits to farm
        # ? Maybe {:.3f}
        labels[1]["text"] = "   {:.2f}".format(need[0]) + f" {need[1]} to {ranks[pRank[0] + 1][0]} ({pRank[0] + 2})"
    else:
        # Remove label
        labels[1].grid_remove()

def drawRank(pRank: Tuple[int, int], ranks: List[str], label: tk.Label, name: str, offset = 0) -> None:
    # Show rank with percentage
    label["text"] = f"{name}: {ranks[pRank[0]]} ({pRank[0] + offset}) - {str(pRank[1])} %"

explorerEvents = ["StartUp", "Undocked", "SellExplorationData", "MissionCompleted"]
merchantEvents = ["StartUp", "Undocked", "MarketSell", "MissionCompleted"]
combatEvents = ["StartUp", "Undocked", "Docked", "Bounty", "MissionCompleted", "StartJump"]
factionEvents = ["StartUp", "Undocked", "Docked", "MissionCompleted"]

def journal_entry(
    cmdr: str, is_beta: bool, system: str, station: str, entry: Dict[str, Any], state: Dict[str, Any]
) -> None:
    try:
        logger.debug(state["Rank"])
        if entry["event"] in explorerEvents:
            global lblExplorer
            global statusExplorer
            drawRankTodo(state["Rank"]["Explore"], explorerRanks, (lblExplorer, statusExplorer), "Explorer")
            logger.info("Explorer rank updated ! From " + entry["event"])

        if entry["event"] in merchantEvents:
            global lblMerchant
            global statusMerchant
            drawRankTodo(state["Rank"]["Trade"], merchantRanks, (lblMerchant, statusMerchant), "Trader")
            logger.info("Trader rank updated ! From " + entry["event"])

        if entry["event"] in combatEvents:
            global lblCombat
            drawRank(state["Rank"]["Combat"], combatRanks, lblCombat, "Combat", 1)
            logger.info("Combat rank updated ! From " + entry["event"])

        if entry["event"] in factionEvents:
            global lblEmpire
            drawRank(state["Rank"]["Empire"], empireRanks, lblEmpire, "Empire")
            global lblFederation
            drawRank(state["Rank"]["Federation"], fedRanks, lblFederation, "Federation")

            logger.info("Faction rank updated ! From " + entry["event"])
    except KeyError as err:
        logger.info("Can't get ranks ! " + repr(err))
