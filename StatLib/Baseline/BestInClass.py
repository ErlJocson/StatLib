import pandas as pd
import numpy as np 

class BestClass:
    def __init__(
            self, 
            df: pd.DataFrame, 
            metricCol: str,
            timeCol: str,
            agents: str,
            target: float = None
            ) -> None:
        self.df = df
        self.metric = metricCol
        self.time = timeCol
        self.agents = agents

        if target:
            self.target = target

    def performTransformation(self):
        pivotTable: pd.DataFrame = pd.pivot_table(self.df, index=self.agents, values=self.metric, columns=self.time, aggfunc='mean')
        row_std = np.nanstd(pivotTable, axis=1)

