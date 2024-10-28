import numpy as np
import pandas as pd

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
        if self.tests['Test 1']:
            self.test_1()

        if self.tests['Test 2']:
            self.test_2()

        if self.tests['Test 3']:
            self.test_3()

        if self.tests['Test 4']:
            self.test_4()

        if self.tests['Test 5']:
            self.test_5()

        if self.tests['Test 6']:
            self.test_6()

        if self.tests['Test 7']:
            self.test_7()

        if self.tests['Test 8']:
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
    
    # TODO: This test needs to be tested
    def test_4(self) -> None:
        """
            Fourteen points in a row is alternating up and down
        """
        state: bool = None
        counter: int = 0

        for i in range(len(self.arr) - 1):
            if not state:
                state = "upwards" if self.arr[i] < self.arr[i+1] else "downwards"

            elif state == "upwards" and self.arr[i] > self.arr[i+1]:
                state = 'downwards'
                counter += 1

            elif state == 'downwards' and self.arr[i] < self.arr[i+1]:
                state = 'upwards'
                counter += 1

            else:
                counter = 0
                state = None

            if counter == 14:
                if all(self.arr[j] for j in range(i, i+14)):
                    self.list_fail = 4
                    counter = 0
                    state = None

    # TODO: This needs to be refined and tested
    def test_5(self) -> None:
        """
            Two out of three points are more than 2 sigma from the center line
        """
        two_sigma_above: float = self.mean + (2 * self.standard_deviation)
        two_sigma_below: float = self.mean - (2 * self.standard_deviation)
        counter_two_sigma_above: int = 0
        counter_two_sigma_below: int = 0
        
        for i in range(len(self.arr) - 2):
            if self.arr[i] > two_sigma_above:
                counter_two_sigma_above += 1
                
            if self.arr[i+1] > two_sigma_above:
                counter_two_sigma_above += 1
                
            if self.arr[i+2] > two_sigma_above:
                counter_two_sigma_above += 1
                
            if counter_two_sigma_above > 1:
                self.list_fail[i] = 5 if self.arr[i] > two_sigma_above else 0
                self.list_fail[i + 1] = 5 if self.arr[i + 1] > two_sigma_above else 0
                self.list_fail[i + 2] = 5 if self.arr[i + 2] > two_sigma_above else 0
                
            counter_two_sigma_above = 0
            
            if self.arr[i] < two_sigma_below:
                counter_two_sigma_below += 1
                
            if self.arr[i+1] < two_sigma_below:
                counter_two_sigma_below += 1
                
            if self.arr[i+2] < two_sigma_below:
                counter_two_sigma_below += 1
                
            if counter_two_sigma_below > 1:
                self.list_fail[i] = 5 if self.arr[i] > two_sigma_below else 0
                self.list_fail[i + 1] = 5 if self.arr[i + 1] > two_sigma_below else 0
                self.list_fail[i + 2] = 5 if self.arr[i + 2] > two_sigma_below else 0
                
            counter_two_sigma_below = 0
    
    # TODO: This test needs to be redefined and tested
    def test_6(self) -> None:
        """
            Four out of five points more than 1sigma from center line (same side)
        """
        counter_one_sigma_below: int = 0
        counter_one_sigma_above: int = 0
        one_sigma_above: float = None
        one_sigma_below: float = None

        for i in range(len(self.arr) - 5):
            if any(self.arr[j] > one_sigma_above for j in range(i, i+5)):
                counter_one_sigma_above += 1
            
            if any(self.arr[j] < one_sigma_below for j in range(i, i+5)):
                counter_one_sigma_below += 1

            if counter_one_sigma_below >= 4:
                self.list_fail[i] = 6 if self.arr[i] < one_sigma_below else 0
                self.list_fail[i + 1] = 6 if self.arr[i + 1] < one_sigma_below else 0
                self.list_fail[i + 2] = 6 if self.arr[i + 2] < one_sigma_below else 0
                self.list_fail[i + 3] = 6 if self.arr[i + 3] < one_sigma_below else 0
                self.list_fail[i + 4] = 6 if self.arr[i + 4] < one_sigma_below else 0

            if counter_one_sigma_above >= 4:
                self.list_fail[i] = 6 if self.arr[i] > one_sigma_above else 0
                self.list_fail[i + 1] = 6 if self.arr[i + 1] > one_sigma_above else 0
                self.list_fail[i + 2] = 6 if self.arr[i + 2] > one_sigma_above else 0
                self.list_fail[i + 3] = 6 if self.arr[i + 3] > one_sigma_above else 0
                self.list_fail[i + 4] = 6 if self.arr[i + 4] > one_sigma_above else 0

            counter_one_sigma_below = 0
            counter_one_sigma_above = 0

    # TODO: this test needs to validated
    def test_7(self) -> None:
        """
            Fifteen points in a row within 1 sigma of center line (either side)
        """
        
        for i in range(len(self.arr) - 15):
            if all(self.arr[j] < self.mean + self.standard_deviation and self.arr[j] > self.mean - self.standard_deviation for j in range(i, i + 15)):
                self.list_fail[i + 14] = 7

    # TODO: this test needs to be validated
    def test_8(self) -> None:
        """
            Eight points in a row more than 1 sigma from center line (either side)
        """
        for i in range(len(self.arr) - 8):
            if all(self.arr[j] > self.mean + self.standard_deviation and self.arr[j] < self.mean - self.standard_deviation for j in range(i, i+15)):
                self.list_fail[i+7] = 8

    def print_chart(self) -> None:
        pass

    def return_dataframe_with_failed_tests(self) -> None:
        pass