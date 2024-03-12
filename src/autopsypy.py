# Copyright (C) 2023, 2024 Rafael Laboissière
#
# This file is part of autopsypy
#
# autopsypy is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# autopsypy is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with Foobar. If not, see <https://www.gnu.org/licenses/>.

import csv
import inspect
import itertools
import math
import os.path as op

import pandas as pd


class AutoPsyPy(dict):
    """Documentation for AutoPsyPy"""

    def __init__(
        self,
        conditions="conditions.csv",
        sessions="sessions.csv",
        csv_delimiter=";",
        desired_group_size=math.inf,
    ):
        super().__init__()

        for v in ["expInfo", "core", "event", "visual", "win"]:
            self.get_psychopy_var(v)

        self.check_expinfo_sanity()

        self.participant = self.var.expInfo["participant"]
        self.datetime = self.var.expInfo["date"]

        self.conditions_filename = conditions
        self.conditions, dummy = self.read_csv(conditions)
        if not isinstance(self.conditions, pd.DataFrame):
            self.error(f"File {conditions} not found")
        nb_conditions = self.conditions.shape[0]

        self.factors = set(self.var.expInfo.keys())
        for field in ["participant", "date", "expName", "psychopyVersion", "frameRate"]:
            self.factors.remove(field)

        self.sessions_filename = sessions
        self.sessions, self.delimiter = self.read_csv(self.sessions_filename)
        if not isinstance(self.sessions, pd.DataFrame):
            columns = (
                ["participant", "datetime"] + list(self.factors) + ["condition", "keep"]
            )
            self.sessions = pd.DataFrame(columns=columns)
            self.delimiter = csv_delimiter

        colnames = set(self.sessions.columns)
        for field in ["participant", "datetime", "condition", "keep"]:
            colnames.remove(field)
        if colnames != self.factors:
            self.error(
                "Mismatch between the fields in the Experiment info and the "
                + "column names in file {self.sessions_filename}"
            )

        self.info = {x: self.var.expInfo[x] for x in self.factors}

        df = self.sessions
        df = df[df["keep"] == "yes"]
        for f in self.factors:
            df = df[df[f] == self.info[f]]
        cnd = df["condition"]

        rep = [0] * nb_conditions
        for i in range(len(cnd)):
            rep[int(cnd.iloc[i]) - 1] += 1
        self.chosen_condition = [i for i, x in enumerate(rep) if x == min(rep)][0] + 1

        for c in self.conditions.columns:
            self[c] = self.conditions[c][self.chosen_condition - 1]

        self.desired_group_size = desired_group_size

    def __getitem__(self, key):
        try:
            value = super().__getitem__(key)
        except KeyError:
            self.error(
                f"There is no column '{key}' in file '{self.conditions_filename}'"
            )
        return value

    def read_csv(self, filename):
        if op.exists(filename) and op.isfile(filename):
            sniffer = csv.Sniffer()
            with open(filename, "r") as fid:
                delimiter = sniffer.sniff(fid.read()).delimiter
            df = pd.read_csv(filename, sep=delimiter, dtype=str)
            try:
                df.to_csv(filename, sep=delimiter, index=False)
            except PermissionError:
                self.error(
                    f"""File {filename} exists but it is not possible to overwrite it.
Check its permission modes or whether it is locked by another program."""
                )
            return df, delimiter
        return None, None

    def get_psychopy_var(self, name):
        if not hasattr(self, "var"):
            self.var = lambda: None
        setattr(self.var, name, inspect.currentframe().f_back.f_back.f_locals[name])

    def check_expinfo_sanity(self):
        if "participant" not in self.var.expInfo:
            self.error("The Experiment info must have the field 'participant'")
        for cnd in ["condition", "keep"]:
            if cnd in self.var.expInfo:
                self.error(f"The Experiment info must not have the field '{cnd}'")

    def show_message(self, msg):
        self.var.win.winHandle.set_fullscreen(False)
        self.var.win.winHandle.set_visible(False)
        win_tmp = self.var.visual.Window(
            fullscr=True, size=[2000, 2000], allowGUI=True, color="black"
        )
        msg = f"{msg}\n\n(type any key to exit)"
        msg = self.var.visual.TextStim(win_tmp, msg, color="white", height=0.05)
        msg.draw()
        win_tmp.flip()
        self.var.event.waitKeys()
        win_tmp.close()
        self.var.win.winHandle.set_visible(True)
        self.var.win.winHandle.set_fullscreen(True)

    def error(self, msg):
        self.show_message(msg)
        self.var.core.quit()

    def show_info(self):
        msg = "\n".join(
            [
                f"participant: {self.participant}",
                "\n".join([f"{x}: {self.info[x]}" for x in self.info.keys()]),
                f"condition: {self.chosen_condition}",
                f"\n\ngroups [{'/'.join(self.info.keys())} = N]:",
            ]
        )
        s = []
        df = self.sessions
        df_yes = df[df["keep"] == "yes"]
        for f in self.info.keys():
            s.append(df_yes[f].unique())
        comb = itertools.product(*s)
        k = list(self.info.keys())
        for c in comb:
            df = df_yes
            for j in range(len(k)):
                df = df[df[k[j]] == c[j]]
            msg += f"\n{'/'.join(c)} = {df.shape[0]}"
        if self.desired_group_size < math.inf:
            msg += f"\n\nthe desired group size is {self.desired_group_size}"
        self.show_message(msg)

    def save_session(self):
        idx = len(self.sessions)
        self.sessions.loc[idx] = None
        self.sessions["participant"][idx] = self.participant
        self.sessions["datetime"][idx] = self.datetime
        self.sessions["condition"][idx] = self.chosen_condition
        self.sessions["condition"] = self.sessions["condition"].astype(int)
        self.sessions["keep"][idx] = "yes"
        for f in self.factors:
            self.sessions[f][idx] = self.info[f]
        self.sessions.to_csv(self.sessions_filename, sep=self.delimiter, index=False)

    def finish(self):
        self.save_session()
        self.show_info()
