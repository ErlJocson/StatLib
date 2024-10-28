import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

class ControlCharts:
    """
    Parameters
    ----------
    df : Pandas Dataframe
        This is the pandas dataframe. This dataframe must 
        included the column where you want to perform control charts
    arr : String
        This is the name of the column where you want to perform control charts
    ucl : Float or Int
        Default to ``None``. 
    lcl : Float or Int
        Default to ``None``.
    target : Float or Int
        Default to ``None``. Metric Target
    stages : String
        Name of the column where stages is set.
    tests : Dictionary
        Dictionary of tests to execute.
    """
    def __init__(
            self,
            df: pd.DataFrame,
            arr: str,
            ucl: bool = None,
            lcl: bool = None,
            target: float = None,
            stages: str = None,
            tests: dict = {
                "Test 1": True,
                "Test 2": True,
                "Test 3": True,
                "Test 4": True,
                "Test 5": True,
                "Test 6": True,
                "Test 7": True,
                "Test 8": True
            }
    ) -> None:
        self.arr: np.array = np.array(df[arr])
        self.mean: float = np.mean(self.arr)
        self.standard_deviation: float = self.get_moving_standard_deviation()
        self.list_fail: np.array = np.zeros(len(self.arr), dtype=int)
        self.tests = tests

        if target:
            self.target: float = target
        
        if stages:
            self.stages: np.array = np.array(df[stages])
        
        if ucl:
            self.ucl:float = ucl

        else:
            self.ucl:float = self.mean + (3 * self.standard_deviation)

        if lcl:
            self.lcl:float = lcl

        else:
            self.lcl:float = self.mean - (3 * self.standard_deviation)

        self.run_tests()

    def get_moving_standard_deviation(self) -> list:
        differences = np.abs(np.diff(self.arr))
        return np.mean(differences) / 1.128

    def run_tests(self) -> None:
        """
        This function will run required tests
        """
        if self.tests['Test 8']:
            self.test_8()
    
        if self.tests['Test 7']:
            self.test_7()
    
        if self.tests['Test 6']:
            self.test_6()
    
        if self.tests['Test 5']:
            self.test_5()
    
        if self.tests['Test 4']:
            self.test_4()
    
        if self.tests['Test 3']:
            self.test_3()
    
        if self.tests['Test 2']:
            self.test_2()
    
        if self.tests['Test 1']:
            self.test_1()
        
    def test_1(self) -> None:
        """
            One point more than 3 standard deviation from the center line
        """
        for i in range(len(self.arr)):
            if self.arr[i] > self.ucl or self.arr[i] < self.lcl:
                self.list_fail[i] = "1"

    def test_2(self) -> None:  
        """
            9 points in a row is on the same side of the center line (mean)
        """
        for i in range(len(self.arr) - 9):
            if all(self.arr[j] < self.mean for j in range(i, i+8)):
                self.list_fail[i + 8] = "2"

            elif all(self.arr[j] > self.mean for j in range(i, i+8)):
                self.list_fail[i + 8] = "2"
    
    def test_3(self) -> None:
        """
            Six points in a row, all increasing or all decreasing
        """
        for i in range(len(self.arr) - 6):
            if all(self.arr[j] > self.arr[j+1] for j in range(i, i + 6)):
                self.list_fail[i+6] = "3"
            elif all(self.arr[j] < self.arr[j+1] for j in range(i, i + 6)):
                self.list_fail[i+6] = "3"
    
    def test_4(self) -> None:
        """
            Fourteen points in a row is alternating up and down
        """
        state: bool = None
        counter: int = 0
        failed_tests: list = []

        for i in range(len(self.arr) - 1):
            if counter == 14:
                for j in failed_tests:
                    self.list_fail[j] = "4"
                counter = 0

            if not state:
                state = "upwards" if self.arr[i] < self.arr[i+1] else "downwards"

            elif state == "upwards" and self.arr[i] > self.arr[i+1]:
                state = 'downwards'
                counter += 1
                failed_tests.append(i)

            elif state == 'downwards' and self.arr[i] < self.arr[i+1]:
                state = 'upwards'
                counter += 1   
                failed_tests.append(i)

            else:
                counter = 0
                state = None
                failed_tests = []

    # TODO: This needs to be refined and tested but this is working already
    def test_5(self) -> None:
        """
            Two out of three points are more than 2 sigma from the center line
        """
        upper_threshold = self.mean + 2 * self.standard_deviation
        lower_threshold = self.mean - 2 * self.standard_deviation
    
        for i in range(len(self.arr) - 2):
            num_above = sum(1 for j in range(i, i + 3) if self.arr[j] > upper_threshold)
            num_below = sum(1 for j in range(i, i + 3) if self.arr[j] < lower_threshold)
    
            if num_above >= 2 or num_below >= 2:
                for j in range(i, i + 3):
                    self.list_fail[j] = "5" if (self.arr[j] > upper_threshold or self.arr[j] < lower_threshold) else self.list_fail[j]
    
    # TODO: This test needs to be validated but this test is already working
    def test_6(self) -> None:
        """
            Four out of five points more than 1sigma from center line (same side)
        """
        one_sigma_above: float = self.mean + self.standard_deviation
        one_sigma_below: float = self.mean - self.standard_deviation

        for i in range(len(self.arr) - 4):
            num_above = sum(1 for j in range(i, i + 5) if self.arr[j] > one_sigma_above)
            num_below = sum(1 for j in range(i, i + 5) if self.arr[j] < one_sigma_below)

            if num_above >= 4 or num_below >= 4:
                for j in range(i, i + 5):
                    self.list_fail[j] = "6" if (self.arr[j] > one_sigma_above or self.arr[j] < one_sigma_below) else self.list_fail[j]

    # TODO: this test needs to validated
    def test_7(self) -> None:
        """
            Fifteen points in a row within 1 sigma of center line (either side)
        """
        for i in range(len(self.arr) - 15):
            if all(self.arr[j] < self.mean + self.standard_deviation or self.arr[j] > self.mean - self.standard_deviation for j in range(i, i + 14)):
                self.list_fail[i + 14] = "7"

    # TODO: this test needs to be validated
    def test_8(self) -> None:
        """
            Eight points in a row more than 1 sigma from center line (either side)
        """
        upper_threshold = self.mean + self.standard_deviation
        lower_threshold = self.mean - self.standard_deviation

        for i in range(len(self.arr) - 7):
            if sum(1 for j in range(i, i+8) if (self.arr[j] > upper_threshold or self.arr[j] < lower_threshold)) == 8:
                self.list_fail[i+7] = "8"

    def print_chart(self) -> None:
        plt.figure(figsize = (10, 5))
        new_df = self.return_dataframe_with_failed_tests()
        sns.scatterplot(x = 'Order Column', y = "Tested Column", hue = "Fail", data = new_df, marker="o", palette=['red', 'blue'])
        sns.despine()
        for i in range(len(new_df)):
            plt.annotate(new_df['Test Failed'][i], (new_df['Order Column'][i], new_df['Tested Column'][i]), xytext=(3, 3), textcoords='offset points')
        plt.axhline(y=self.ucl, color='green', linestyle='--', linewidth = 0.7)
        plt.axhline(y=self.lcl, color='green', linestyle='--', linewidth = 0.7)
        plt.axhline(y=self.mean, color='blue', linestyle='--', linewidth = 0.7)
        plt.show()

    def return_dataframe_with_failed_tests(self) -> None:
        return pd.DataFrame(
            {
                "Tested Column": self.arr,
                "Order Column": [i+1 for i in range(len(self.arr))],
                "Test Failed": self.list_fail,
                "Fail": ["No" if i == 0 else "Yes" for i in self.list_fail]
            }
        )