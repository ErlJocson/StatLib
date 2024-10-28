import numpy as np
import pandas as pd

class ControlCharts:    
    def __init__(
            self,
            df: pd.DataFrame,
            arr: str,
            ucl: bool = None,
            lcl: bool = None,
            target: float = None,
            stages: str = None,
            ):
        
        self.arr: np.array = np.array(df[arr])
        self.mean: float = np.mean(self.arr)
        self.standard_deviation: float = self.get_moving_standard_deviation()
        self.list_fail: np.array = np.zeros(len(self.arr), dtype=int)

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
        self.test_1()
        self.test_2()
        self.test_3()
        self.test_4()
        self.test_5()
        self.test_6()
        self.test_7()
        self.test_8()
    
    def test_1(self) -> None:
        """
            One point more than 3 standard deviation from the center line
        """
        for i in range(len(self.arr)):
            if self.arr[i] > self.ucl or self.arr[i] < self.lcl:
                self.list_fail[i] = 1
    
    def test_2(self) -> None:  
        """
            9 points in a row is on the same side of the center line (mean)
        """
        for i in range(len(self.arr) - 9):
            if all(self.arr[j] < self.mean for j in range(i, i+8)):
                self.list_fail[i + 8] = 2

            elif all(self.arr[j] > self.mean for j in range(i, i+8)):
                self.list_fail[i + 8] = 2
    
    def test_3(self) -> None:
        """
            Six points in a row, all increasing or all decreasing
        """
        for i in range(len(self.arr) - 6):
            if all(self.arr[j] > self.arr[j+1] for j in range(i, i + 6)):
                self.list_fail[i+6] = 3
            elif all(self.arr[j] < self.arr[j+1] for j in range(i, i + 6)):
                self.list_fail[i+6] = 3
    
    def test_4(self) -> None:
        """
            Fourteen points in a row is alternating up and down
        """

    # TODO: This needs to be refined
    def test_5(self) -> None:
        """
            Two out of three points are more than 2 sigma from the center line
        """
        two_sigma_above: float = self.mean + (2 * self.standard_deviation)
        two_sigma_below: float = self.mean - (2 * self.standard_deviation)
        counter: int = 0
        
        for i in range(len(self.arr) - 2):
            if self.arr[i] > two_sigma_above:
                counter += 1
                
            if self.arr[i+1] > two_sigma_above:
                counter += 1
                
            if self.arr[i+2] > two_sigma_above:
                counter += 1
                
            if counter > 1:
                self.list_fail[i] = 5
                self.list_fail[i + 1] = 5
                self.list_fail[i + 2] = 5
                
            counter = 0
            
            if self.arr[i] < two_sigma_below:
                counter += 1
                
            if self.arr[i+1] < two_sigma_below:
                counter += 1
                
            if self.arr[i+2] < two_sigma_below:
                counter += 1
                
            if counter > 1:
                self.list_fail[i] = 5
                self.list_fail[i + 1] = 5
                self.list_fail[i + 2] = 5
                
            counter = 0
            
    def test_6(self) -> None:
        pass

    def test_7(self) -> None:
        pass

    def test_8(self) -> None:
        pass

    def print_chart(self) -> None:
        pass

    def return_dataframe_with_failed_tests(self) -> None:
        pass