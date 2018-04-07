#!/usr/bin/python3
import csv
from datetime import datetime
from decimal import Decimal

with open("./resources/trades/msltrades.csv", 'r') as f:
    position = {}
    trades = []
    reader = csv.reader(f)
    for row in reader:
        trade = (
        datetime.strptime(row[0], '%d-%b-%Y'), row[1], row[3], row[4], row[5], Decimal(row[6]), Decimal(row[14]))
        trades.append(trade)

    trades.sort(key=lambda t: t[0])
    # print(trades)
    for trade in trades:
        if trade[1] in position:
            if position[trade[1]]["open_side"] == trade[2]:
                # Add to Existing position
                position[trade[1]]["open_value"] += trade[5]
                position[trade[1]]["open_charges"] += trade[6]
                trade_value = position[trade[1]]["open_value"] if trade[2] == "Sell" else -position[trade[1]][
                    "open_value"]
                pnl = trade_value - position[trade[1]]["open_charges"]
                position[trade[1]]["pnl"] = pnl;
                continue
            else:
                # Closing position
                position[trade[1]]["close_date"] = trade[0]
                position[trade[1]]["close_side"] = trade[2]
                position[trade[1]]["close_value"] += trade[5]
                position[trade[1]]["close_charges"] += trade[6]
                if position[trade[1]]["close_value"] != 0:
                    if trade[2] == "Sell":
                        position[trade[1]]["pnl"] = position[trade[1]]["close_value"] - position[trade[1]][
                            "open_value"] - (position[trade[1]]["open_charges"] + position[trade[1]]["close_charges"])
                    elif trade[2] == "Buy":
                        position[trade[1]]["pnl"] = position[trade[1]]["open_value"] - position[trade[1]][
                            "close_value"] - (position[trade[1]]["open_charges"] + position[trade[1]]["close_charges"])
                    else:
                        print("UNKNOWN SIDE")
        else:
            position[trade[1]] = {"open_date": trade[0], "open_side": trade[2], "open_value": trade[5],
                                  "open_charges": trade[6],
                                  "close_date": datetime.now(), "close_side": "Close OUT", "close_value": 0,
                                  "close_charges": 0}
            pnl = 0
            if trade[2] == "Sell":
                pnl = trade[5] - trade[6]
            elif trade[2] == "Buy":
                pnl = -trade[5] - trade[6]
            else:
                print("UNKNOWN SIDE")
            position[trade[1]]["pnl"] = pnl;

    # print(position)
    net_pnl = 0
    for key in position:
        pnl = position[key]["pnl"]
        net_pnl += pnl
        print(key + "," + position[key]["open_date"].strftime('%d/%m/%Y') + ",", str(position[key]["open_value"]) + ",",
              str(position[key]["open_charges"]) + ",", position[key]["close_date"].strftime('%d/%m/%Y') + ","
              , str(position[key]["close_value"]) + ",", str(position[key]["close_charges"]) + ",", pnl)
    print(net_pnl)
